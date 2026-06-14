from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from .models import Role, TeamMember
from .services import module_enabled


MODULE_CODES = {
    "supporters": "supporter-registry",
    "wards": "ward-intelligence",
    "calls": "relationship-calls",
    "influencers": "relationship-calls",
    "messages": "messaging",
    "events": "events-tasks",
    "tasks": "events-tasks",
    "issues": "ward-intelligence",
    "polling": "polling-war-room",
    "ai": "ai-assistant",
    "constituency": "constituency-management",
}


ROLE_CAPABILITIES = {
    Role.CANDIDATE: {"view_all", "manage_team", "send_messages", "approve_ai", "view_reports", "manage_subscription"},
    Role.CAMPAIGN_MANAGER: {"view_all", "manage_team", "assign_tasks", "send_messages", "manage_events", "manage_polling", "view_reports"},
    Role.IT_ADMIN: {"view_all", "manage_team", "import_data", "export_data", "manage_subscription", "configure_settings"},
    Role.DISTRICT_COORDINATOR: {"view_assigned", "submit_reports", "assign_tasks", "send_messages"},
    Role.LLG_COORDINATOR: {"view_assigned", "submit_reports", "assign_tasks"},
    Role.WARD_COORDINATOR: {"view_assigned", "register_supporters", "submit_reports"},
    Role.VILLAGE_COORDINATOR: {"view_assigned", "register_supporters", "submit_reports"},
    Role.VOLUNTEER: {"view_assigned", "submit_reports"},
    Role.SCRUTINEER: {"view_polling", "submit_polling"},
}


# ── Role hierarchy ──────────────────────────────────────────────────────────
# Lower number = more senior. Used for "who can create whom" and "who approves".
# IT_ADMIN sits at the campaign-manager tier (off the field chain but senior).
ROLE_LEVEL = {
    Role.CANDIDATE: 0,
    Role.CAMPAIGN_MANAGER: 1,
    Role.IT_ADMIN: 1,
    Role.DISTRICT_COORDINATOR: 2,
    Role.LLG_COORDINATOR: 3,
    Role.WARD_COORDINATOR: 4,
    Role.VILLAGE_COORDINATOR: 5,  # "Area Coordinator"
    Role.VOLUNTEER: 6,
    Role.SCRUTINEER: 6,
}

# The geographic level each role is scoped to when reading data.
ROLE_SCOPE = {
    Role.DISTRICT_COORDINATOR: "district",
    Role.LLG_COORDINATOR: "llg",
    Role.WARD_COORDINATOR: "ward",
    Role.VILLAGE_COORDINATOR: "village",
    Role.VOLUNTEER: "village",
    Role.SCRUTINEER: "ward",
}

# Roles that are senior/admin and always see the whole campaign.
VIEW_ALL_ROLES = {Role.CANDIDATE, Role.CAMPAIGN_MANAGER, Role.IT_ADMIN}

# Roles a coordinator may NOT create even though they are numerically below —
# the senior/admin tier is reserved for the candidate and existing managers.
_NON_DELEGATABLE = {Role.CANDIDATE}


def role_level(role):
    return ROLE_LEVEL.get(role, 99)


def creatable_roles(member, candidate):
    """Roles `member` is allowed to create (strictly junior to their own),
    valid for this candidate's type."""
    from .services import role_choices_for_candidate

    if member is None:  # superuser / candidate-owner context
        return role_choices_for_candidate(candidate)
    my_level = role_level(member.role)
    allowed = []
    for value, label in role_choices_for_candidate(candidate):
        if value in _NON_DELEGATABLE:
            continue
        if role_level(value) > my_level:
            allowed.append((value, label))
    return allowed


def member_for_user(user, candidate):
    """The active TeamMember for this user (may be pending/inactive-aware caller)."""
    return team_member_for_user(user, candidate)


def required_approver_level(creator_member):
    """The most-junior role level allowed to approve something this creator made:
    one tier above the creator."""
    if creator_member is None:
        return 0
    return max(role_level(creator_member.role) - 1, 0)


def can_approve_member(approver_member, pending_member):
    """True when approver is senior enough AND geographically contains the
    pending member. Superuser/candidate-owner handled by callers via view_all."""
    if approver_member is None:
        return True
    creator = pending_member.created_by_member
    needed = required_approver_level(creator) if creator else role_level(pending_member.role) - 1
    if role_level(approver_member.role) > needed:
        return False  # approver is too junior
    return _geo_contains(approver_member, pending_member)


def _geo_contains(senior, member):
    """True if `senior`'s geographic assignment contains `member`'s location."""
    if senior.role in VIEW_ALL_ROLES:
        return True
    if senior.district_id and member.district_id != senior.district_id:
        return False
    if senior.llg_id and member.llg_id != senior.llg_id:
        return False
    if senior.ward_id and member.ward_id != senior.ward_id:
        return False
    if senior.village_id and member.village_id != senior.village_id:
        return False
    return True


def team_member_for_user(user, candidate):
    if not user.is_authenticated or not candidate:
        return None
    return TeamMember.objects.filter(user=user, candidate=candidate, is_active=True).first()


def user_role_for_candidate(user, candidate):
    if user.is_superuser:
        return "SYSTEM_SUPER_ADMIN"
    member = team_member_for_user(user, candidate)
    return member.role if member else None


def has_capability(user, candidate, capability):
    if user.is_superuser:
        return True
    member = team_member_for_user(user, candidate)
    if not member:
        return False
    return capability in ROLE_CAPABILITIES.get(member.role, set())


def can_access_module(user, candidate, module_code):
    if user.is_superuser:
        return True
    if not candidate or candidate.status in {"SUSPENDED", "ARCHIVED"}:
        return False
    if module_code == "core-crm":
        return True
    return module_enabled(candidate, module_code)


def can_access_geography(user, candidate, province=None, district=None, llg=None, ward=None, village=None):
    if user.is_superuser or has_capability(user, candidate, "view_all"):
        return True
    member = team_member_for_user(user, candidate)
    if not member:
        return False
    if province and member.province_id and province.id != member.province_id:
        return False
    if member.district_id and district and district.id != member.district_id:
        return False
    if member.llg_id and llg and llg.id != member.llg_id:
        return False
    if member.ward_id and ward and ward.id != member.ward_id:
        return False
    if member.village_id and village and village.id != member.village_id:
        return False
    return True


# ── Geographic queryset scoping (upward aggregation) ────────────────────────
_SCOPE_DEPTH = {"district": 1, "llg": 2, "ward": 3, "village": 4}


def _apply_geo_scope(qs, member, scope):
    """Filter a queryset to the tightest geographic containment the model
    supports at or above the member's scope level. Most-specific path wins so a
    ward coordinator gets ward-level data even on models that also expose llg."""
    if not scope:
        return qs
    fields = {f.name for f in qs.model._meta.get_fields()}
    depth = _SCOPE_DEPTH.get(scope, 0)
    candidates = []
    if depth >= 4 and member.village_id and "village" in fields:
        candidates.append({"village_id": member.village_id})
    if depth >= 3 and member.ward_id and "ward" in fields:
        candidates.append({"ward_id": member.ward_id})
    if depth >= 2 and member.llg_id:
        if "llg" in fields:
            candidates.append({"llg_id": member.llg_id})
        elif "ward" in fields:
            candidates.append({"ward__llg_id": member.llg_id})
    if depth >= 1 and member.district_id:
        if "district" in fields:
            candidates.append({"district_id": member.district_id})
        elif "ward" in fields:
            candidates.append({"ward__llg__district_id": member.district_id})
        elif "llg" in fields:
            candidates.append({"llg__district_id": member.district_id})
    if not candidates:
        return qs.none()
    return qs.filter(**candidates[0])


def scope_queryset(qs, user, candidate):
    """Restrict a candidate-scoped queryset to the logged-in member's geography.
    Senior/admin roles and superusers see everything, so data naturally rolls
    upward: each senior level's scope is a superset of its subordinates'."""
    if user.is_superuser:
        return qs
    member = team_member_for_user(user, candidate)
    if not member or member.role in VIEW_ALL_ROLES:
        return qs
    return _apply_geo_scope(qs, member, ROLE_SCOPE.get(member.role))


def pending_members_for(user, candidate):
    """Pending TeamMembers this user is allowed to approve."""
    from .models import ApprovalStatus

    qs = TeamMember.objects.filter(
        candidate=candidate, approval_status=ApprovalStatus.PENDING
    ).select_related("created_by_member", "district", "llg", "ward", "village")
    if user.is_superuser:
        return qs
    member = team_member_for_user(user, candidate)
    if not member:
        return qs.none()
    if member.role in VIEW_ALL_ROLES:
        return qs
    allowed_ids = [m.id for m in qs if can_approve_member(member, m)]
    return qs.filter(id__in=allowed_ids)


# ── Village (geography) creation & approval ─────────────────────────────────
def can_create_village(member):
    """Ward coordinators and more senior roles may request a new village."""
    if member is None:
        return True  # superuser / candidate-owner context
    return role_level(member.role) <= ROLE_LEVEL[Role.WARD_COORDINATOR]


def can_approve_village(approver_member, village):
    """LLG coordinators and above may approve a village within their branch."""
    if approver_member is None:
        return True
    if role_level(approver_member.role) > ROLE_LEVEL[Role.LLG_COORDINATOR]:
        return False  # ward/area/volunteer cannot approve geography
    if approver_member.role in VIEW_ALL_ROLES:
        return True
    ward = village.ward
    if approver_member.llg_id and ward.llg_id != approver_member.llg_id:
        return False
    if approver_member.district_id and ward.llg.district_id != approver_member.district_id:
        return False
    return True


def pending_villages_for(user, candidate):
    """Pending villages this user may approve (within their geographic branch)."""
    from .models import ApprovalStatus, Village

    qs = Village.objects.filter(approval_status=ApprovalStatus.PENDING).select_related(
        "ward", "ward__llg", "ward__llg__district", "created_by_member"
    )
    if user.is_superuser:
        return qs
    member = team_member_for_user(user, candidate)
    if not member:
        return qs.none()
    if member.role in VIEW_ALL_ROLES:
        # Limit to the candidate's geography even for campaign-wide roles.
        return qs.filter(ward__in=candidate.available_wards())
    allowed_ids = [v.id for v in qs if can_approve_village(member, v)]
    return qs.filter(id__in=allowed_ids)


def module_required(module_code):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            candidate = getattr(request, "campaign_candidate", None)
            if candidate is None:
                from .views import _active_candidate

                candidate = _active_candidate(request)
            if can_access_module(request.user, candidate, module_code):
                return view_func(request, *args, **kwargs)
            messages.warning(request, "This module is not enabled for the current subscription.")
            return redirect("subscription")

        return wrapper

    return decorator


def capability_required(capability):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            candidate = getattr(request, "campaign_candidate", None)
            if candidate is None:
                from .views import _active_candidate

                candidate = _active_candidate(request)
            if has_capability(request.user, candidate, capability):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied

        return wrapper

    return decorator
