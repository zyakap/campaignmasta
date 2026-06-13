from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, Q, Sum
from django.utils import timezone

from .models import (
    AIWorkItem,
    CallLog,
    CampaignEvent,
    CampaignTask,
    Candidate,
    CandidateType,
    CommunityIssue,
    ConnectorSetting,
    FreeAIModel,
    IncludedUsageQuota,
    PlanAIModel,
    Influencer,
    Message,
    MessageRecipient,
    ModuleBundle,
    ReminderEscalation,
    SoftwareModule,
    Subscription,
    SubscriptionQuote,
    TenantModuleSubscription,
    TenantSettings,
    TenantUsageQuota,
    PollingIncident,
    PollingLocation,
    PromiseTracker,
    Role,
    SupportStatus,
    Supporter,
    TeamMember,
    UsageEvent,
    UsageRateCard,
    UsageService,
    UsageUnit,
    UsageWallet,
    WardProfile,
)


SENSITIVE_AI_RULES = [
    "Use AI for organization, summaries, reminders, and drafting only.",
    "Require human review before any AI-generated campaign message is sent.",
    "Do not generate intimidation, harassment, coercion, vote-buying, or misleading claims.",
    "Respect candidate and geography boundaries in every prompt and output.",
]


def resolve_active_candidate(request):
    """Authorization-aware resolution of the active candidate (tenant) for a request.

    Superusers may view any candidate (session selection, else the first). Other
    users are restricted to candidates they have an active TeamMember role in, so a
    session-stored candidate_id can never be used to reach another tenant's data.
    Returns None for anonymous users.
    """
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return None

    queryset = Candidate.objects.select_related("province", "district")
    session_id = request.session.get("candidate_id")

    if user.is_superuser:
        candidate = (queryset.filter(id=session_id).first() if session_id else None) or queryset.first()
    else:
        memberships = TeamMember.objects.filter(user=user, is_active=True)
        if session_id and memberships.filter(candidate_id=session_id).exists():
            candidate = queryset.filter(id=session_id).first()
        else:
            member = memberships.select_related("candidate").first()
            candidate = queryset.filter(id=member.candidate_id).first() if member else None

    if candidate and request.session.get("candidate_id") != candidate.id:
        request.session["candidate_id"] = candidate.id
    return candidate


def candidates_for_user(user):
    """Candidates a user may switch between: all for superusers, otherwise only
    those the user holds an active team role in. Prevents the candidate switcher
    from leaking other tenants' names."""
    if not user or not user.is_authenticated:
        return Candidate.objects.none()
    queryset = Candidate.objects.select_related("province", "district")
    if user.is_superuser:
        return queryset
    return queryset.filter(teammembers__user=user, teammembers__is_active=True).distinct()


def tenant_scope_filter(candidate):
    districts = candidate.available_districts()
    return Q(province=candidate.province) & (Q(district__in=districts) | Q(district__isnull=True))


def role_choices_for_candidate(candidate):
    roles = list(Role.choices)
    if candidate.candidate_type == CandidateType.DISTRICT_OPEN:
        roles = [role for role in roles if role[0] != Role.DISTRICT_COORDINATOR]
    return roles


def message_target_options(candidate):
    common = [
        "All Team",
        "Campaign Manager",
        "IT Administrator",
        "All LLG Coordinators",
        "Specific LLG",
        "All Ward Coordinators",
        "Specific Ward",
        "Village Coordinators",
        "Volunteers",
        "Influencers",
        "Supporters with consent",
    ]
    if candidate.candidate_type == CandidateType.PROVINCIAL:
        return ["All Province Team", "All District Coordinators", "Specific District"] + common
    return common


def usage_wallet_for_candidate(candidate, service, currency="PGK"):
    wallet, _ = UsageWallet.objects.get_or_create(
        candidate=candidate,
        service=service,
        currency=currency,
        defaults={"created_by": None, "updated_by": None},
    )
    return wallet


def usage_rate_for(service, unit, provider="", model_name="", currency="PGK"):
    candidates = UsageRateCard.objects.filter(service=service, unit=unit, currency=currency, is_active=True).order_by("-effective_from")
    exact = candidates.filter(provider=provider, model_name=model_name).first()
    if exact:
        return exact
    provider_default = candidates.filter(provider=provider, model_name="").first()
    if provider_default:
        return provider_default
    model_default = candidates.filter(provider="", model_name=model_name).first()
    if model_default:
        return model_default
    return candidates.filter(provider="", model_name="").first()


def free_ai_model(model_id):
    return FreeAIModel.objects.filter(model_id=model_id, is_active=True).first()


def get_plan_ai_model(candidate):
    """Return the free AI model configured for the candidate's subscription plan.

    Checks for a default PlanAIModel assignment first, then any assignment for the plan,
    then falls back to the first active FreeAIModel so new tenants always get something.
    """
    qs = PlanAIModel.objects.filter(plan=candidate.subscription_plan, ai_model__is_active=True).select_related("ai_model")
    assignment = qs.filter(is_default=True).first() or qs.first()
    if assignment:
        return assignment.ai_model
    return FreeAIModel.objects.filter(is_active=True).first()


def estimate_usage_charge(service, unit, quantity=1, provider="", model_name="", currency="PGK"):
    free_model = free_ai_model(model_name) if service == UsageService.AI else None
    if free_model:
        return Decimal("0.00"), None, free_model
    rate = usage_rate_for(service, unit, provider=provider, model_name=model_name, currency=currency)
    if not rate:
        return Decimal("0.00"), None, None
    return Decimal(rate.calculate_charge(quantity)).quantize(Decimal("0.01")), rate, None


def active_tenant_quota(candidate, service, unit):
    today = timezone.localdate()
    return (
        TenantUsageQuota.objects.filter(
            candidate=candidate,
            service=service,
            unit=unit,
            is_active=True,
            included_quantity__gt=0,
        )
        .filter(Q(reset_period_end__isnull=True) | Q(reset_period_end__gte=today))
        .order_by("reset_period_end", "id")
        .first()
    )


def apply_included_quota(candidate, service, unit, quantity):
    quota = active_tenant_quota(candidate, service, unit)
    if not quota:
        return None, 0
    return quota, quota.consume(quantity)


def record_metered_usage(candidate, service, action, unit, quantity=1, connector=None, provider="", model_name="", reference="", metadata=None, user=None, currency="PGK"):
    metadata = metadata or {}
    wallet = usage_wallet_for_candidate(candidate, service, currency=currency)
    quota, included_quantity = apply_included_quota(candidate, service, unit, quantity)
    billable_quantity = max(quantity - included_quantity, 0)
    charge, rate, free_model = estimate_usage_charge(service, unit, billable_quantity, provider=provider, model_name=model_name, currency=currency)
    provider_cost = Decimal("0.00")
    markup_amount = Decimal("0.00")
    if rate and not rate.is_free:
        provider_cost = (rate.provider_cost_per_unit * billable_quantity).quantize(Decimal("0.0001"))
        markup_amount = max(charge - provider_cost, Decimal("0.00")).quantize(Decimal("0.0001"))
    balance_before = wallet.balance

    if billable_quantity == 0 and included_quantity:
        status = UsageEvent.Status.INCLUDED_QUOTA
        balance_after = balance_before
    elif free_model or (rate and rate.is_free):
        status = UsageEvent.Status.FREE
        balance_after = balance_before
    elif not rate:
        status = UsageEvent.Status.BLOCKED_NO_CREDIT
        balance_after = balance_before
        metadata = {**metadata, "billing_error": "No active usage rate card configured for this service/unit."}
    elif not wallet.can_spend(charge):
        status = UsageEvent.Status.BLOCKED_NO_CREDIT
        balance_after = balance_before
    else:
        status = UsageEvent.Status.ALLOWED
        wallet.balance = wallet.balance - charge
        wallet.save(update_fields=["balance", "updated_at"])
        balance_after = wallet.balance

    event = UsageEvent.objects.create(
        candidate=candidate,
        service=service,
        connector=connector,
        wallet=wallet,
        quota=quota,
        rate_card=rate,
        free_ai_model=free_model,
        action=action,
        unit=unit,
        quantity=quantity,
        included_quantity_applied=included_quantity,
        billable_quantity=billable_quantity,
        provider_cost=provider_cost,
        markup_amount=markup_amount,
        customer_charge=charge,
        balance_before=balance_before,
        balance_after=balance_after,
        status=status,
        reference=reference,
        metadata=metadata,
        created_by=user,
        updated_by=user,
    )
    return event


def require_usage_credit(candidate, service, action, unit, quantity=1, connector=None, provider="", model_name="", reference="", metadata=None, user=None, currency="PGK"):
    event = record_metered_usage(
        candidate,
        service,
        action,
        unit,
        quantity=quantity,
        connector=connector,
        provider=provider,
        model_name=model_name,
        reference=reference,
        metadata=metadata,
        user=user,
        currency=currency,
    )
    if event.status == UsageEvent.Status.BLOCKED_NO_CREDIT:
        raise ValueError(f"Insufficient prepaid {event.get_service_display()} credit. Please top up before using this service.")
    return event


def quota_period_end(start_date, billing_cycle):
    if billing_cycle == "MONTHLY":
        return start_date + timedelta(days=30)
    if billing_cycle == "QUARTERLY":
        return start_date + timedelta(days=91)
    if billing_cycle == "ANNUAL":
        return start_date + timedelta(days=365)
    if billing_cycle == "CAMPAIGN_PERIOD":
        return start_date + timedelta(days=365)
    return None


def create_tenant_quota_from_template(candidate, subscription, quota_template, user=None):
    start = subscription.start_date or timezone.localdate()
    return TenantUsageQuota.objects.create(
        candidate=candidate,
        subscription=subscription,
        source_module=quota_template.module,
        source_bundle=quota_template.bundle,
        service=quota_template.service,
        unit=quota_template.unit,
        included_quantity=quota_template.quantity,
        reset_period_start=start,
        reset_period_end=quota_period_end(start, subscription.billing_cycle),
        notes=quota_template.description,
        created_by=user,
        updated_by=user,
    )


def provision_included_quotas(candidate, subscription, modules=None, bundles=None, user=None):
    modules = modules or []
    bundles = bundles or []
    for module in modules:
        for quota in module.included_usage_quotas.filter(is_active=True, billing_cycle=subscription.billing_cycle):
            create_tenant_quota_from_template(candidate, subscription, quota, user=user)
    for bundle in bundles:
        for quota in bundle.included_usage_quotas.filter(is_active=True, billing_cycle=subscription.billing_cycle):
            create_tenant_quota_from_template(candidate, subscription, quota, user=user)


def enabled_module_codes(candidate):
    return set(
        TenantModuleSubscription.objects.filter(candidate=candidate, is_enabled=True, module__is_active=True)
        .filter(Q(end_date__isnull=True) | Q(end_date__gte=timezone.localdate()))
        .values_list("module__code", flat=True)
    )


def module_enabled(candidate, code):
    return code in enabled_module_codes(candidate)


def module_catalog_for_candidate(candidate):
    enabled = enabled_module_codes(candidate)
    modules = SoftwareModule.objects.filter(is_active=True).prefetch_related("prices").order_by("sort_order", "name")
    return [{"module": module, "enabled": module.code in enabled, "prices": module.prices.filter(is_active=True)} for module in modules]


def bundle_catalog():
    return ModuleBundle.objects.filter(is_active=True).prefetch_related("modules").order_by("sort_order", "name")


def apply_bundle_to_tenant(candidate, bundle, subscription=None, user=None):
    entitlements = []
    for module in bundle.modules.filter(is_active=True):
        entitlement, _ = TenantModuleSubscription.objects.update_or_create(
            candidate=candidate,
            module=module,
            defaults={
                "subscription": subscription,
                "bundle": bundle,
                "source": TenantModuleSubscription.Source.FULL_PACKAGE if bundle.is_full_package else TenantModuleSubscription.Source.BUNDLE,
                "is_enabled": True,
                "price_locked": 0,
                "created_by": user,
                "updated_by": user,
            },
        )
        entitlements.append(entitlement)
    return entitlements


def quote_from_selection(candidate, module_codes=None, bundle_codes=None, billing_cycle="MONTHLY", currency="PGK", user=None):
    quote = SubscriptionQuote.objects.create(
        candidate=candidate,
        billing_cycle=billing_cycle,
        currency=currency,
        created_by=user,
        updated_by=user,
    )
    if module_codes:
        quote.modules.set(SoftwareModule.objects.filter(code__in=module_codes, is_active=True))
    if bundle_codes:
        quote.bundles.set(ModuleBundle.objects.filter(code__in=bundle_codes, is_active=True))
    quote.recalculate()
    quote.save(update_fields=["subtotal", "discount_amount", "total", "updated_at"])
    return quote


def accept_quote(quote, user=None):
    quote.recalculate()
    quote.accepted_at = timezone.now()
    quote.updated_by = user
    quote.save(update_fields=["subtotal", "discount_amount", "total", "accepted_at", "updated_by", "updated_at"])
    subscription = Subscription.objects.create(
        candidate=quote.candidate,
        plan=Candidate.Plan.FULL_PACKAGE if quote.bundles.filter(is_full_package=True).exists() else Candidate.Plan.PROFESSIONAL,
        billing_cycle=quote.billing_cycle,
        status=Subscription.Status.ACTIVE,
        amount=quote.total,
        payment_method="Manual invoice",
        invoice_number=f"CM-Q{quote.id}",
        created_by=user,
        updated_by=user,
    )
    module_ids_from_bundles = set()
    accepted_bundles = list(quote.bundles.filter(is_active=True))
    for bundle in quote.bundles.filter(is_active=True):
        module_ids_from_bundles.update(bundle.modules.values_list("id", flat=True))
        apply_bundle_to_tenant(quote.candidate, bundle, subscription=subscription, user=user)
    accepted_modules = list(quote.modules.filter(is_active=True).exclude(id__in=module_ids_from_bundles))
    for module in accepted_modules:
        price = module.prices.filter(billing_cycle=quote.billing_cycle, currency=quote.currency, is_active=True).first()
        TenantModuleSubscription.objects.update_or_create(
            candidate=quote.candidate,
            module=module,
            defaults={
                "subscription": subscription,
                "bundle": None,
                "source": TenantModuleSubscription.Source.INDIVIDUAL,
                "is_enabled": True,
                "price_locked": price.price if price else 0,
                "created_by": user,
                "updated_by": user,
            },
        )
    provision_included_quotas(quote.candidate, subscription, modules=accepted_modules, bundles=accepted_bundles, user=user)
    return subscription


def provision_team_member_login(member, username, password=None, user=None):
    """Create or update the mobile-app login account linked to a team member.

    Returns the linked user (or None when no username supplied). A DRF auth token
    is ensured so the team member can immediately authenticate against the API.
    """
    from django.contrib.auth import get_user_model
    from rest_framework.authtoken.models import Token

    username = (username or "").strip()
    if not username and not member.user_id:
        return None

    User = get_user_model()
    account = member.user
    if account is None:
        account, _ = User.objects.get_or_create(
            username=username,
            defaults={"email": member.email or "", "is_staff": False},
        )
    elif username and account.username != username:
        account.username = username
    if member.email and account.email != member.email:
        account.email = member.email
    if password:
        account.set_password(password)
    account.is_active = member.is_active
    account.save()
    if member.user_id != account.id:
        member.user = account
        member.save(update_fields=["user", "updated_at"])
    Token.objects.get_or_create(user=account)
    return account


def recipients_for_message(message):
    team = TeamMember.objects.filter(candidate=message.candidate, is_active=True)
    supporters = Supporter.objects.filter(candidate=message.candidate, consent_to_messages=True)
    influencers = Influencer.objects.filter(candidate=message.candidate)
    target = message.recipient_type
    group = message.recipient_group

    if target in ("All Team", "All Province Team"):
        return {"team": team, "supporters": Supporter.objects.none(), "influencers": Influencer.objects.none()}
    if target == "Campaign Manager":
        team = team.filter(role=Role.CAMPAIGN_MANAGER)
    elif target == "IT Administrator":
        team = team.filter(role=Role.IT_ADMIN)
    elif target == "All District Coordinators":
        team = team.filter(role=Role.DISTRICT_COORDINATOR)
    elif target == "All LLG Coordinators":
        team = team.filter(role=Role.LLG_COORDINATOR)
    elif target == "All Ward Coordinators":
        team = team.filter(role=Role.WARD_COORDINATOR)
    elif target == "Village Coordinators":
        team = team.filter(role=Role.VILLAGE_COORDINATOR)
    elif target == "Volunteers":
        team = team.filter(role=Role.VOLUNTEER)
    elif target == "Specific District" and group:
        team = team.filter(district__name__iexact=group)
    elif target == "Specific LLG" and group:
        team = team.filter(llg__name__iexact=group)
    elif target == "Specific Ward" and group:
        team = team.filter(ward__name__iexact=group)
    elif target == "Influencers":
        return {"team": TeamMember.objects.none(), "supporters": Supporter.objects.none(), "influencers": influencers}
    elif target == "Supporters with consent":
        return {"team": TeamMember.objects.none(), "supporters": supporters, "influencers": Influencer.objects.none()}

    return {"team": team, "supporters": Supporter.objects.none(), "influencers": Influencer.objects.none()}


def dispatch_message(message, user=None):
    recipients = recipients_for_message(message)
    recipient_count = sum(queryset.count() for queryset in recipients.values())
    paid_channel_services = {
        "SMS": UsageService.SMS,
        "WHATSAPP": UsageService.WHATSAPP,
        "EMAIL": UsageService.EMAIL,
    }
    if message.delivery_channel in paid_channel_services and recipient_count:
        connector = messaging_connector_for_channel(message.candidate, message.delivery_channel)
        require_usage_credit(
            message.candidate,
            paid_channel_services[message.delivery_channel],
            f"Send {message.delivery_channel} message",
            UsageUnit.MESSAGE if message.delivery_channel in {"SMS", "WHATSAPP"} else UsageUnit.EMAIL,
            quantity=recipient_count,
            connector=connector,
            provider=connector.provider if connector else "",
            reference=f"message:{message.id}",
            metadata={"subject": message.subject, "recipient_type": message.recipient_type},
            user=user,
        )
    MessageRecipient.objects.filter(message=message).delete()
    created = []
    for member in recipients["team"]:
        created.append(
            MessageRecipient(
                message=message,
                team_member=member,
                display_name=member.full_name,
                phone=member.phone,
                email=member.email,
                delivered_at=timezone.now() if message.delivery_channel == "IN_APP" else None,
            )
        )
    for supporter in recipients["supporters"]:
        created.append(
            MessageRecipient(
                message=message,
                supporter=supporter,
                display_name=supporter.full_name,
                phone=supporter.phone,
                delivered_at=timezone.now() if message.delivery_channel == "IN_APP" else None,
            )
        )
    for influencer in recipients["influencers"]:
        created.append(
            MessageRecipient(
                message=message,
                influencer=influencer,
                display_name=influencer.full_name,
                phone=influencer.phone,
                email=influencer.email,
                delivered_at=timezone.now() if message.delivery_channel == "IN_APP" else None,
            )
        )
    MessageRecipient.objects.bulk_create(created)
    message.status = "SENT"
    message.sent_at = timezone.now()
    message.updated_by = user
    message.save(update_fields=["status", "sent_at", "updated_by", "updated_at"])
    return len(created)


def call_checklist(candidate):
    today = timezone.localdate()
    try:
        settings_obj = TenantSettings.objects.get(candidate=candidate)
        coord_frequency = settings_obj.default_call_frequency_high
    except TenantSettings.DoesNotExist:
        coord_frequency = 7

    due = Influencer.objects.filter(candidate=candidate, next_contact_due_date__lte=today).order_by("next_contact_due_date", "-influence_level")
    coordinators = TeamMember.objects.filter(
        candidate=candidate,
        is_active=True,
        role__in=[Role.DISTRICT_COORDINATOR, Role.LLG_COORDINATOR, Role.WARD_COORDINATOR, Role.VILLAGE_COORDINATOR],
    )
    if candidate.candidate_type == CandidateType.DISTRICT_OPEN:
        coordinators = coordinators.exclude(role=Role.DISTRICT_COORDINATOR)
    cutoff = today - timedelta(days=coord_frequency)
    recently_called_ids = CallLog.objects.filter(
        candidate=candidate,
        call_datetime__date__gte=cutoff,
        called_team_member__isnull=False,
    ).values_list("called_team_member_id", flat=True)
    quiet_coordinators = coordinators.exclude(id__in=recently_called_ids)
    return {
        "overdue": due.filter(next_contact_due_date__lt=today),
        "due_today": due.filter(next_contact_due_date=today),
        "quiet_coordinators": quiet_coordinators,
    }


def check_and_escalate_coordinator_alerts(candidate, user=None):
    from .audit import create_escalation

    try:
        settings_obj = TenantSettings.objects.get(candidate=candidate)
        freq = settings_obj.default_call_frequency_high
    except TenantSettings.DoesNotExist:
        freq = 7

    today = timezone.localdate()
    cutoff = today - timedelta(days=freq)

    coordinator_roles = [Role.WARD_COORDINATOR, Role.LLG_COORDINATOR, Role.VILLAGE_COORDINATOR]
    if candidate.candidate_type == CandidateType.PROVINCIAL:
        coordinator_roles.append(Role.DISTRICT_COORDINATOR)

    coordinators = TeamMember.objects.filter(candidate=candidate, is_active=True, role__in=coordinator_roles)
    recently_called_ids = CallLog.objects.filter(
        candidate=candidate,
        call_datetime__date__gte=cutoff,
        called_team_member__isnull=False,
    ).values_list("called_team_member_id", flat=True)
    quiet = coordinators.exclude(id__in=recently_called_ids)

    for coordinator in quiet:
        if ReminderEscalation.objects.filter(candidate=candidate, owner=coordinator, status="OPEN").exists():
            continue

        escalated_to = None
        if coordinator.role == Role.WARD_COORDINATOR and coordinator.llg_id:
            escalated_to = TeamMember.objects.filter(
                candidate=candidate, role=Role.LLG_COORDINATOR, llg=coordinator.llg, is_active=True
            ).first()
        elif coordinator.role == Role.LLG_COORDINATOR:
            if candidate.candidate_type == CandidateType.PROVINCIAL and coordinator.district_id:
                escalated_to = TeamMember.objects.filter(
                    candidate=candidate, role=Role.DISTRICT_COORDINATOR, district=coordinator.district, is_active=True
                ).first()
            if not escalated_to:
                escalated_to = TeamMember.objects.filter(
                    candidate=candidate, role=Role.CAMPAIGN_MANAGER, is_active=True
                ).first()
        elif coordinator.role in (Role.DISTRICT_COORDINATOR, Role.VILLAGE_COORDINATOR):
            escalated_to = TeamMember.objects.filter(
                candidate=candidate, role=Role.CAMPAIGN_MANAGER, is_active=True
            ).first()

        create_escalation(
            candidate=candidate,
            title=f"{coordinator.get_role_display()} {coordinator.full_name} not contacted in {freq} days",
            owner=coordinator,
            escalated_to=escalated_to,
            reason=(
                f"{coordinator.full_name} ({coordinator.get_role_display()}) has not been called in the last {freq} days. "
                f"Follow up required to maintain relationship and campaign discipline."
            ),
            due_date=today,
            user=user,
        )


def dashboard_metrics(candidate):
    supporters = Supporter.objects.filter(candidate=candidate)
    wards = WardProfile.objects.filter(candidate=candidate)
    today = timezone.localdate()
    return {
        "supporter_count": supporters.count(),
        "strong_supporters": supporters.filter(support_status=SupportStatus.STRONG).count(),
        "undecided_contacts": supporters.filter(support_status=SupportStatus.UNDECIDED).count(),
        "consented_contacts": supporters.filter(consent_to_messages=True).count(),
        "strong_wards": wards.filter(support_strength="STRONG").count(),
        "weak_wards": wards.filter(support_strength="WEAK").count(),
        "wards_not_visited": wards.exclude(ward__campaignevent__candidate=candidate).count(),
        "pending_promises": PromiseTracker.objects.filter(candidate=candidate).exclude(status__in=["DELIVERED", "CANCELLED"]).count(),
        "open_issues": CommunityIssue.objects.filter(candidate=candidate).exclude(status="RESOLVED").count(),
        "polling_locations": PollingLocation.objects.filter(candidate=candidate).count(),
        "polling_incidents": PollingIncident.objects.filter(candidate=candidate).exclude(status="RESOLVED").count(),
        "overdue_tasks": CampaignTask.objects.filter(candidate=candidate, due_date__lt=today).exclude(status__in=["COMPLETED", "CANCELLED"]).count(),
        "message_ack_pending": Message.objects.filter(candidate=candidate, acknowledgement_required=True).exclude(status="SENT").count(),
    }


def usage_summary(candidate):
    wallets = UsageWallet.objects.filter(candidate=candidate).order_by("service")
    quotas = TenantUsageQuota.objects.filter(candidate=candidate, is_active=True).order_by("service", "unit")
    recent_events = UsageEvent.objects.filter(candidate=candidate)[:20]
    totals = (
        UsageEvent.objects.filter(candidate=candidate, status__in=[UsageEvent.Status.ALLOWED, UsageEvent.Status.FREE])
        .values("service")
        .annotate(total_charge=Sum("customer_charge"))
    )
    return {
        "wallets": wallets,
        "included_quotas": quotas,
        "recent_usage_events": recent_events,
        "usage_event_counts": totals,
        "low_balance_wallets": [wallet for wallet in wallets if wallet.balance <= wallet.low_balance_threshold],
    }


def report_rollup(candidate):
    group_field = "ward__llg__district__name" if candidate.candidate_type == CandidateType.PROVINCIAL else "ward__llg__name"
    return (
        Supporter.objects.filter(candidate=candidate, ward__isnull=False)
        .values(group_field)
        .annotate(
            total=Count("id"),
            strong=Count("id", filter=Q(support_status=SupportStatus.STRONG)),
            undecided=Count("id", filter=Q(support_status=SupportStatus.UNDECIDED)),
        )
        .order_by(group_field)
    )


def build_ward_brief_payload(candidate, ward_profile):
    ward = ward_profile.ward
    supporters = Supporter.objects.filter(candidate=candidate, ward=ward)
    influencers = Influencer.objects.filter(candidate=candidate, ward=ward)
    issues = CommunityIssue.objects.filter(candidate=candidate, ward=ward).exclude(status="RESOLVED").order_by("-created_at")[:5]
    events = CampaignEvent.objects.filter(candidate=candidate, ward=ward).order_by("-start_datetime")[:5]
    promises = PromiseTracker.objects.filter(candidate=candidate, ward=ward).exclude(status__in=["DELIVERED", "CANCELLED"])[:5]
    return {
        "ward": ward_profile.brief_summary(),
        "supporter_count": supporters.count(),
        "undecided_count": supporters.filter(support_status=SupportStatus.UNDECIDED).count(),
        "influencers": list(influencers.values_list("full_name", "community_role")[:8]),
        "issues": list(issues.values_list("title", "category", "priority")),
        "events": list(events.values_list("title", "start_datetime")),
        "promises": list(promises.values_list("title", "target_date")),
    }


def create_ward_ai_work_item(candidate, ward_profile, user=None):
    connector = ai_connector_for_candidate(candidate)
    plan_model = get_plan_ai_model(candidate)
    model_name = connector.ai_model if connector and connector.ai_model else (plan_model.model_id if plan_model else "")
    provider = connector.provider if connector else (plan_model.provider if plan_model else "")
    usage_event = require_usage_credit(
        candidate,
        UsageService.AI,
        "Generate ward brief draft",
        UsageUnit.REQUEST,
        quantity=1,
        connector=connector,
        provider=provider,
        model_name=model_name,
        reference=f"ward_profile:{ward_profile.id}",
        metadata={"ward": ward_profile.ward.name},
        user=user,
    )
    payload = build_ward_brief_payload(candidate, ward_profile)
    output = [
        f"Ward: {payload['ward']['ward']}",
        f"Support strength: {payload['ward']['support_strength']}",
        f"Supporters registered: {payload['supporter_count']} ({payload['undecided_count']} undecided)",
        f"Key issues: {payload['ward']['issues'] or 'No issues recorded'}",
        f"Talking points: {payload['ward']['talking_points'] or 'Listen first and confirm local priorities.'}",
    ]
    return AIWorkItem.objects.create(
        candidate=candidate,
        ward=ward_profile.ward,
        work_type=AIWorkItem.WorkType.WARD_BRIEF,
        ai_model=model_name,
        used_free_model=usage_event.status == UsageEvent.Status.FREE,
        source_snapshot=payload,
        output="\n".join(output),
        safety_notes="\n".join(SENSITIVE_AI_RULES),
        status=AIWorkItem.Status.READY_FOR_REVIEW,
        created_by=user,
        updated_by=user,
    )


def create_speech_ai_work_item(candidate, ward_profile, event=None, user=None):
    connector = ai_connector_for_candidate(candidate)
    plan_model = get_plan_ai_model(candidate)
    model_name = connector.ai_model if connector and connector.ai_model else (plan_model.model_id if plan_model else "")
    provider = connector.provider if connector else (plan_model.provider if plan_model else "")
    usage_event = require_usage_credit(
        candidate,
        UsageService.AI,
        "Generate speech notes draft",
        UsageUnit.REQUEST,
        quantity=1,
        connector=connector,
        provider=provider,
        model_name=model_name,
        reference=f"ward_profile:{ward_profile.id}",
        metadata={"ward": ward_profile.ward.name},
        user=user,
    )
    payload = build_ward_brief_payload(candidate, ward_profile)
    ward = payload["ward"]
    output_lines = [
        f"SPEECH OUTLINE — {ward['ward']}",
        "",
        f"OPEN WITH: Acknowledge {ward['leaders'] or 'the ward councillor, community elders, and local leaders'} by name.",
        "",
        "KEY THEMES TO ADDRESS:",
        f"  {ward['issues'] or 'Listen to community priorities first. Avoid making specific promises before understanding local needs.'}",
        "",
        "TALKING POINTS:",
        f"  {ward['talking_points'] or 'Reference local landmarks and community groups. Keep commitments specific and realistic.'}",
        "",
        f"LOCAL REFERENCES: {ward['landmarks'] or 'Use landmarks from the ward profile to show familiarity with the area.'}",
        "",
        f"PENDING PROMISES: {', '.join(p[0] for p in payload['promises']) if payload['promises'] else 'None on record.'}",
        "",
        "SENSITIVE TOPICS TO AVOID:",
        f"  {ward['sensitivities'] or 'Avoid divisive clan references or unresolved community conflicts. Check security notes.'}",
        "",
        f"SUPPORTER SNAPSHOT: {payload['supporter_count']} registered · {payload['undecided_count']} undecided",
    ]
    return AIWorkItem.objects.create(
        candidate=candidate,
        ward=ward_profile.ward,
        event=event,
        work_type=AIWorkItem.WorkType.SPEECH_NOTES,
        ai_model=model_name,
        used_free_model=usage_event.status == UsageEvent.Status.FREE,
        source_snapshot=payload,
        output="\n".join(output_lines),
        safety_notes="\n".join(SENSITIVE_AI_RULES),
        status=AIWorkItem.Status.READY_FOR_REVIEW,
        created_by=user,
        updated_by=user,
    )


def connector_health_check(connector):
    required = {
        ConnectorSetting.ConnectorType.AI: ["api_key", "ai_model"],
        ConnectorSetting.ConnectorType.WHATSAPP: ["access_token", "whatsapp_phone_number_id", "whatsapp_business_account_id"],
        ConnectorSetting.ConnectorType.SMS: ["api_key", "sms_sender_id"],
        ConnectorSetting.ConnectorType.EMAIL: ["email_host", "email_port", "email_username", "email_password", "email_from_address"],
        ConnectorSetting.ConnectorType.MAPS: ["maps_api_key"],
        ConnectorSetting.ConnectorType.PAYMENT: ["payment_public_key", "payment_secret_key", "payment_merchant_id"],
        ConnectorSetting.ConnectorType.STORAGE: ["api_key"],
        ConnectorSetting.ConnectorType.WEBHOOK: ["webhook_url", "webhook_secret"],
    }
    missing = [field for field in required.get(connector.connector_type, []) if not getattr(connector, field)]
    connector.last_tested_at = timezone.now()
    if missing:
        connector.status = ConnectorSetting.Status.FAILED
        connector.last_test_result = f"Missing required settings: {', '.join(missing)}"
    else:
        connector.status = ConnectorSetting.Status.ACTIVE if connector.is_enabled else ConnectorSetting.Status.CONFIGURED
        connector.last_test_result = "Configuration looks complete. Live provider test can be added per connector."
    connector.save(update_fields=["status", "last_tested_at", "last_test_result", "updated_at"])
    return connector


def connectors_for_candidate(candidate):
    configured = ConnectorSetting.objects.filter(candidate=candidate).order_by("connector_type", "name")
    configured_types = set(configured.values_list("connector_type", flat=True))
    missing_types = [choice for choice in ConnectorSetting.ConnectorType.choices if choice[0] not in configured_types]
    return configured, missing_types


def active_connector(candidate, connector_type):
    return (
        ConnectorSetting.objects.filter(
            candidate=candidate,
            connector_type=connector_type,
            is_enabled=True,
            status__in=[ConnectorSetting.Status.ACTIVE, ConnectorSetting.Status.CONFIGURED, ConnectorSetting.Status.NEEDS_TEST],
        )
        .order_by("name")
        .first()
    )


def ai_connector_for_candidate(candidate):
    return active_connector(candidate, ConnectorSetting.ConnectorType.AI)


def messaging_connector_for_channel(candidate, channel):
    if channel == "SMS":
        return active_connector(candidate, ConnectorSetting.ConnectorType.SMS)
    if channel == "EMAIL":
        return active_connector(candidate, ConnectorSetting.ConnectorType.EMAIL)
    if channel == "WHATSAPP":
        return active_connector(candidate, ConnectorSetting.ConnectorType.WHATSAPP)
    return None
