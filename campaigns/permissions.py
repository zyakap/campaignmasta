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
