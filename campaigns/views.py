from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AIReviewForm,
    CallLogQuickForm,
    CitizenRequestQuickForm,
    CommunityAssistanceForm,
    CommunityGroupForm,
    CompetitorActivityForm,
    ConnectorSettingForm,
    DevelopmentFundForm,
    EventQuickForm,
    ExportRequestForm,
    FreeAIModelForm,
    IncludedUsageQuotaForm,
    PlanAIModelForm,
    InfluencerQuickForm,
    ImportBatchForm,
    IssueQuickForm,
    MessageQuickForm,
    PollingIncidentQuickForm,
    PollingLocationQuickForm,
    PollingStatusQuickForm,
    PreferenceDealForm,
    PromiseQuickForm,
    RegistrationDriveForm,
    SubscriptionQuoteForm,
    SupporterQuickForm,
    TaskQuickForm,
    TeamMemberQuickForm,
    TenantSettingsForm,
    UsageRateCardForm,
    UsageTopUpForm,
    WardProfileForm,
)
from .models import (
    AIWorkItem,
    CampaignEvent,
    CampaignTask,
    Candidate,
    CitizenRequest,
    CommunityAssistance,
    CommunityGroup,
    CommunityIssue,
    CompetitorActivity,
    ConnectorSetting,
    DevelopmentFund,
    ExportRequest,
    FreeAIModel,
    IncludedUsageQuota,
    PlanAIModel,
    Influencer,
    ImportBatch,
    Message,
    MessageRecipient,
    PollingIncident,
    PollingLocation,
    PollingStatus,
    PreferenceDeal,
    PromiseTracker,
    RegistrationDrive,
    SubscriptionQuote,
    SupportStatus,
    Supporter,
    TeamMember,
    TenantSettings,
    UsageEvent,
    UsageRateCard,
    UsageService,
    UsageWallet,
    WardProfile,
)
from .permissions import capability_required, module_required
from .import_export import build_export_file, process_import_batch
from .audit import log_audit
from .services import (
    accept_quote,
    build_ward_brief_payload,
    call_checklist,
    check_and_escalate_coordinator_alerts,
    connector_health_check,
    connectors_for_candidate,
    create_speech_ai_work_item,
    create_ward_ai_work_item,
    dashboard_metrics,
    dispatch_message,
    recipients_for_message,
    bundle_catalog,
    report_rollup,
    module_catalog_for_candidate,
    usage_summary,
    usage_wallet_for_candidate,
)


def _active_candidate(request):
    candidate_id = request.session.get("candidate_id")
    queryset = Candidate.objects.select_related("province", "district")
    if candidate_id:
        candidate = queryset.filter(id=candidate_id).first()
        if candidate:
            return candidate
    if request.user.is_superuser:
        candidate = queryset.first()
    else:
        member = TeamMember.objects.filter(user=request.user, is_active=True).first()
        candidate = queryset.filter(id=member.candidate_id).first() if member else None
    if candidate:
        request.session["candidate_id"] = candidate.id
    return candidate


@login_required
def switch_candidate(request, candidate_id):
    if request.user.is_superuser:
        get_object_or_404(Candidate, id=candidate_id)
    else:
        get_object_or_404(Candidate, id=candidate_id, teammembers__user=request.user, teammembers__is_active=True)
    request.session["candidate_id"] = candidate_id
    return redirect("dashboard")


@login_required
def dashboard(request):
    candidate = _active_candidate(request)
    tenants = Candidate.objects.all()
    if not candidate:
        return render(request, "campaigns/empty_state.html")

    tasks = CampaignTask.objects.filter(candidate=candidate).select_related("assigned_to")
    messages_qs = Message.objects.filter(candidate=candidate)
    events = CampaignEvent.objects.filter(candidate=candidate, start_datetime__gte=timezone.now()).order_by("start_datetime")[:5]
    issues = CommunityIssue.objects.filter(candidate=candidate).exclude(status="RESOLVED").order_by("-created_at")[:5]
    calls = call_checklist(candidate)
    usage = usage_summary(candidate)

    context = {
        "candidate": candidate,
        "candidates": tenants,
        **dashboard_metrics(candidate),
        "overdue_calls": calls["overdue"][:8],
        "due_calls": calls["due_today"][:8],
        "quiet_coordinators": calls["quiet_coordinators"][:8],
        "upcoming_events": events,
        "open_tasks": tasks.exclude(status__in=["COMPLETED", "CANCELLED"]).order_by("due_date")[:8],
        "urgent_messages": messages_qs.filter(priority__in=["IMPORTANT", "URGENT"]).order_by("-created_at")[:5],
        "open_issues": issues,
        "ward_strength": WardProfile.objects.filter(candidate=candidate).values("support_strength").annotate(total=Count("id")),
        "usage_wallets": usage["wallets"],
        "low_balance_wallets": usage["low_balance_wallets"],
    }
    return render(request, "campaigns/dashboard.html", context)


@login_required
def subscription(request):
    candidate = _active_candidate(request)
    return render(
        request,
        "campaigns/subscription.html",
        {
            "candidate": candidate,
            "module_catalog": module_catalog_for_candidate(candidate),
            "bundles": bundle_catalog(),
            "quotes": SubscriptionQuote.objects.filter(candidate=candidate)[:10],
        },
    )


@login_required
@capability_required("manage_subscription")
def subscription_quote_create(request):
    candidate = _active_candidate(request)
    form = SubscriptionQuoteForm(request.POST or None)
    if form.is_valid():
        quote = form.save(commit=False)
        quote.candidate = candidate
        quote.created_by = request.user
        quote.updated_by = request.user
        quote.save()
        form.save_m2m()
        quote.recalculate()
        quote.save(update_fields=["subtotal", "discount_amount", "total", "updated_at"])
        messages.success(request, "Subscription quote created.")
        log_audit(request, "SUBSCRIPTION_QUOTE_CREATED", quote, new_value={"total": str(quote.total)})
        return redirect("subscription")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Create Subscription Quote", "submit_label": "Save quote"})


@login_required
@capability_required("manage_subscription")
def subscription_quote_accept(request, quote_id):
    candidate = _active_candidate(request)
    quote = get_object_or_404(SubscriptionQuote, candidate=candidate, id=quote_id)
    accept_quote(quote, request.user)
    log_audit(request, "SUBSCRIPTION_QUOTE_ACCEPTED", quote, new_value={"total": str(quote.total)})
    messages.success(request, "Quote accepted and modules enabled.")
    return redirect("subscription")


@login_required
@capability_required("configure_settings")
def campaign_settings(request):
    candidate = _active_candidate(request)
    settings_obj, _ = TenantSettings.objects.get_or_create(candidate=candidate, defaults={"created_by": request.user, "updated_by": request.user})
    if request.method == "POST":
        form = TenantSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            settings_obj = form.save(commit=False)
            settings_obj.updated_by = request.user
            settings_obj.save()
            log_audit(request, "TENANT_SETTINGS_UPDATED", settings_obj)
            messages.success(request, "Campaign settings saved.")
            return redirect("campaign_settings")
    else:
        form = TenantSettingsForm(instance=settings_obj)
    connectors, missing_types = connectors_for_candidate(candidate)
    return render(
        request,
        "campaigns/settings.html",
        {
            "candidate": candidate,
            "form": form,
            "connectors": connectors,
            "missing_connector_types": missing_types,
        },
    )


@login_required
@capability_required("configure_settings")
def connector_create(request):
    candidate = _active_candidate(request)
    form = ConnectorSettingForm(request.POST or None)
    if form.is_valid():
        connector = form.save(commit=False)
        connector.candidate = candidate
        connector.created_by = request.user
        connector.updated_by = request.user
        connector.save()
        log_audit(request, "CONNECTOR_CREATED", connector, new_value={"type": connector.connector_type, "provider": connector.provider})
        messages.success(request, "Connector setting saved.")
        return redirect("campaign_settings")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Connector", "submit_label": "Save connector"})


@login_required
@capability_required("configure_settings")
def connector_update(request, connector_id):
    candidate = _active_candidate(request)
    connector = get_object_or_404(ConnectorSetting, candidate=candidate, id=connector_id)
    form = ConnectorSettingForm(request.POST or None, instance=connector)
    if form.is_valid():
        connector = form.save(commit=False)
        connector.updated_by = request.user
        connector.save()
        log_audit(request, "CONNECTOR_UPDATED", connector, new_value={"type": connector.connector_type, "provider": connector.provider})
        messages.success(request, "Connector setting updated.")
        return redirect("campaign_settings")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Edit Connector", "submit_label": "Save connector"})


@login_required
@capability_required("configure_settings")
def connector_test(request, connector_id):
    candidate = _active_candidate(request)
    connector = get_object_or_404(ConnectorSetting, candidate=candidate, id=connector_id)
    connector_health_check(connector)
    log_audit(request, "CONNECTOR_TESTED", connector, new_value={"status": connector.status})
    messages.success(request, connector.last_test_result)
    return redirect("campaign_settings")


@login_required
def usage_dashboard(request):
    candidate = _active_candidate(request)
    for service in [UsageService.AI, UsageService.WHATSAPP, UsageService.SMS, UsageService.EMAIL, UsageService.MAPS, UsageService.STORAGE]:
        usage_wallet_for_candidate(candidate, service)
    usage = usage_summary(candidate)
    return render(request, "campaigns/usage.html", {"candidate": candidate, **usage})


@login_required
@capability_required("configure_settings")
def usage_topup_create(request):
    candidate = _active_candidate(request)
    form = UsageTopUpForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        topup = form.save(commit=False)
        topup.candidate = candidate
        topup.received_by = request.user
        topup.created_by = request.user
        topup.updated_by = request.user
        topup.save()
        log_audit(request, "USAGE_TOPUP_CREATED", topup, new_value={"amount": str(topup.amount), "wallet": str(topup.wallet)})
        messages.success(request, "Prepaid usage credit added.")
        return redirect("usage_dashboard")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Prepaid Credit", "submit_label": "Add credit"})


@login_required
def platform_usage_settings(request):
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    rates = UsageRateCard.objects.all().order_by("service", "provider", "model_name")
    free_models = FreeAIModel.objects.all().order_by("provider", "name")
    plan_ai_models = PlanAIModel.objects.select_related("ai_model").order_by("plan", "ai_model__name")
    included_quotas = IncludedUsageQuota.objects.filter(is_active=True).select_related("module", "bundle")
    recent_usage = UsageEvent.objects.select_related("candidate", "wallet", "rate_card")[:50]
    wallets = UsageWallet.objects.select_related("candidate").order_by("candidate__name", "service")
    return render(
        request,
        "campaigns/platform_usage_settings.html",
        {
            "candidate": _active_candidate(request),
            "rates": rates,
            "free_models": free_models,
            "plan_ai_models": plan_ai_models,
            "included_quotas": included_quotas,
            "recent_usage": recent_usage,
            "wallets": wallets,
        },
    )


@login_required
def usage_rate_create(request):
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    candidate = _active_candidate(request)
    form = UsageRateCardForm(request.POST or None)
    if form.is_valid():
        rate = form.save(commit=False)
        rate.created_by = request.user
        rate.updated_by = request.user
        rate.save()
        log_audit(request, "USAGE_RATE_CREATED", rate, new_value={"service": rate.service, "markup_percent": str(rate.markup_percent)})
        messages.success(request, "Usage rate and markup saved.")
        return redirect("platform_usage_settings")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Usage Rate", "submit_label": "Save rate"})


@login_required
def free_ai_model_create(request):
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    candidate = _active_candidate(request)
    form = FreeAIModelForm(request.POST or None)
    if form.is_valid():
        model = form.save(commit=False)
        model.created_by = request.user
        model.updated_by = request.user
        model.save()
        log_audit(request, "FREE_AI_MODEL_CREATED", model, new_value={"model_id": model.model_id})
        messages.success(request, "Free AI model added.")
        return redirect("platform_usage_settings")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Free AI Model", "submit_label": "Save model"})


@login_required
def free_ai_model_edit(request, model_id):
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    candidate = _active_candidate(request)
    instance = get_object_or_404(FreeAIModel, id=model_id)
    form = FreeAIModelForm(request.POST or None, instance=instance)
    if form.is_valid():
        model = form.save(commit=False)
        model.updated_by = request.user
        model.save()
        log_audit(request, "FREE_AI_MODEL_UPDATED", model, new_value={"model_id": model.model_id, "is_active": model.is_active})
        messages.success(request, "Free AI model updated.")
        return redirect("platform_usage_settings")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": f"Edit {instance.name}", "submit_label": "Save changes"})


@login_required
def plan_ai_model_create(request):
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    candidate = _active_candidate(request)
    form = PlanAIModelForm(request.POST or None)
    if form.is_valid():
        assignment = form.save(commit=False)
        assignment.created_by = request.user
        assignment.updated_by = request.user
        assignment.save()
        log_audit(request, "PLAN_AI_MODEL_ASSIGNED", assignment, new_value={"plan": assignment.plan, "model": assignment.ai_model.model_id})
        messages.success(request, f"{assignment.ai_model.name} assigned to {assignment.get_plan_label()} plan.")
        return redirect("platform_usage_settings")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Assign AI Model to Plan", "submit_label": "Save assignment"})


@login_required
def plan_ai_model_delete(request, assignment_id):
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    assignment = get_object_or_404(PlanAIModel, id=assignment_id)
    if request.method == "POST":
        log_audit(request, "PLAN_AI_MODEL_REMOVED", assignment, new_value={"plan": assignment.plan, "model": assignment.ai_model.model_id})
        assignment.delete()
        messages.success(request, "Plan AI model assignment removed.")
    return redirect("platform_usage_settings")


@login_required
def included_quota_create(request):
    if not request.user.is_superuser:
        from django.core.exceptions import PermissionDenied

        raise PermissionDenied
    candidate = _active_candidate(request)
    form = IncludedUsageQuotaForm(request.POST or None)
    if form.is_valid():
        quota = form.save(commit=False)
        quota.created_by = request.user
        quota.updated_by = request.user
        quota.save()
        log_audit(request, "INCLUDED_USAGE_QUOTA_CREATED", quota, new_value={"service": quota.service, "quantity": quota.quantity})
        messages.success(request, "Included usage quota saved.")
        return redirect("platform_usage_settings")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Included Usage Quota", "submit_label": "Save quota"})


@login_required
@module_required("supporter-registry")
def supporters(request):
    candidate = _active_candidate(request)
    query = request.GET.get("q", "")
    records = Supporter.objects.filter(candidate=candidate).select_related("ward", "village").order_by("-created_at")
    if query:
        records = records.filter(Q(full_name__icontains=query) | Q(phone__icontains=query) | Q(village__name__icontains=query))
    return render(request, "campaigns/supporters.html", {"candidate": candidate, "records": records[:100], "query": query})


@login_required
@module_required("core-crm")
def team(request):
    candidate = _active_candidate(request)
    records = TeamMember.objects.filter(candidate=candidate).select_related("district", "llg", "ward", "village").order_by("role", "full_name")
    return render(request, "campaigns/team.html", {"candidate": candidate, "records": records})


@login_required
@module_required("core-crm")
@capability_required("manage_team")
def team_member_create(request):
    candidate = _active_candidate(request)
    form = TeamMemberQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        member = form.save(commit=False)
        member.candidate = candidate
        member.created_by = request.user
        member.updated_by = request.user
        member.save()
        log_audit(request, "TEAM_MEMBER_CREATED", member, new_value={"role": member.role})
        messages.success(request, "Team member saved.")
        return redirect("team")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Team Member", "submit_label": "Save team member"})


@login_required
@module_required("supporter-registry")
def supporter_create(request):
    candidate = _active_candidate(request)
    form = SupporterQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        supporter = form.save(commit=False)
        supporter.candidate = candidate
        supporter.created_by = request.user
        supporter.updated_by = request.user
        supporter.save()
        duplicate_count = supporter.possible_duplicates().count()
        if duplicate_count:
            messages.warning(request, f"Saved, with {duplicate_count} possible duplicate contact.")
        else:
            messages.success(request, "Supporter saved.")
        log_audit(request, "SUPPORTER_CREATED", supporter, new_value={"full_name": supporter.full_name})
        return redirect("supporters")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Register Supporter", "submit_label": "Save supporter"})


@login_required
@module_required("relationship-calls")
def calls(request):
    candidate = _active_candidate(request)
    check_and_escalate_coordinator_alerts(candidate, user=request.user)
    checklist = call_checklist(candidate)
    return render(request, "campaigns/calls.html", {"candidate": candidate, **checklist})


@login_required
@module_required("relationship-calls")
def call_create(request):
    candidate = _active_candidate(request)
    form = CallLogQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        call = form.save(commit=False)
        call.candidate = candidate
        call.recorded_by = request.user
        call.created_by = request.user
        call.updated_by = request.user
        call.save()
        log_audit(request, "CALL_LOG_CREATED", call, new_value={"person_called": call.person_called})
        messages.success(request, "Call recorded and next contact updated.")
        return redirect("calls")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Record Call", "submit_label": "Save call"})


@login_required
@module_required("messaging")
def messages_view(request):
    candidate = _active_candidate(request)
    records = Message.objects.filter(candidate=candidate).order_by("-created_at")[:50]
    return render(request, "campaigns/messages.html", {"candidate": candidate, "records": records})


@login_required
@module_required("messaging")
def message_create(request):
    candidate = _active_candidate(request)
    form = MessageQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        message = form.save(commit=False)
        message.candidate = candidate
        message.created_by = request.user
        message.updated_by = request.user
        message.save()
        recipients = recipients_for_message(message)
        recipient_count = sum(queryset.count() for queryset in recipients.values())
        log_audit(request, "MESSAGE_CREATED", message, new_value={"recipient_count": recipient_count})
        messages.success(request, f"Message saved for review/sending. Preview recipients: {recipient_count}.")
        return redirect("messages")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Compose Message", "submit_label": "Save message"})


@login_required
@module_required("messaging")
@capability_required("send_messages")
def message_send(request, message_id):
    candidate = _active_candidate(request)
    message = get_object_or_404(Message, candidate=candidate, id=message_id)
    try:
        recipient_count = dispatch_message(message, request.user)
    except ValueError as exc:
        messages.warning(request, str(exc))
        return redirect("usage_dashboard")
    log_audit(request, "MESSAGE_SENT", message, new_value={"recipient_count": recipient_count})
    messages.success(request, f"Message sent to {recipient_count} recipient records.")
    return redirect("messages")


@login_required
@module_required("messaging")
def message_detail(request, message_id):
    candidate = _active_candidate(request)
    message = get_object_or_404(Message, candidate=candidate, id=message_id)
    recipients = message.recipients.select_related("team_member", "supporter", "influencer").order_by("display_name")
    my_receipt = None
    member = TeamMember.objects.filter(user=request.user, candidate=candidate, is_active=True).first()
    if member:
        my_receipt = recipients.filter(team_member=member).first()
    return render(request, "campaigns/message_detail.html", {
        "candidate": candidate,
        "message": message,
        "recipients": recipients,
        "my_receipt": my_receipt,
    })


@login_required
@module_required("messaging")
def message_mark_read(request, message_id):
    candidate = _active_candidate(request)
    message = get_object_or_404(Message, candidate=candidate, id=message_id)
    member = TeamMember.objects.filter(user=request.user, candidate=candidate, is_active=True).first()
    if member:
        receipt, _ = MessageRecipient.objects.get_or_create(
            message=message, team_member=member,
            defaults={"display_name": member.full_name, "phone": member.phone, "email": member.email},
        )
        if not receipt.read_at:
            receipt.read_at = timezone.now()
            receipt.save(update_fields=["read_at"])
            log_audit(request, "MESSAGE_READ", message, new_value={"recipient": member.full_name})
    messages.success(request, "Message marked as read.")
    return redirect("message_detail", message_id=message_id)


@login_required
@module_required("messaging")
def message_mark_acknowledged(request, message_id):
    candidate = _active_candidate(request)
    message = get_object_or_404(Message, candidate=candidate, id=message_id)
    member = TeamMember.objects.filter(user=request.user, candidate=candidate, is_active=True).first()
    if member:
        receipt, _ = MessageRecipient.objects.get_or_create(
            message=message, team_member=member,
            defaults={"display_name": member.full_name, "phone": member.phone, "email": member.email},
        )
        if not receipt.acknowledged_at:
            receipt.acknowledged_at = timezone.now()
            receipt.save(update_fields=["acknowledged_at"])
            log_audit(request, "MESSAGE_ACKNOWLEDGED", message, new_value={"recipient": member.full_name})
    messages.success(request, "Message acknowledged.")
    return redirect("message_detail", message_id=message_id)


@login_required
@module_required("events-tasks")
def tasks(request):
    candidate = _active_candidate(request)
    records = CampaignTask.objects.filter(candidate=candidate).select_related("assigned_to").order_by("due_date", "-created_at")[:80]
    return render(request, "campaigns/tasks.html", {"candidate": candidate, "records": records})


@login_required
@module_required("events-tasks")
def task_create(request):
    candidate = _active_candidate(request)
    form = TaskQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        task = form.save(commit=False)
        task.candidate = candidate
        task.created_by = request.user
        task.updated_by = request.user
        task.save()
        log_audit(request, "TASK_CREATED", task, new_value={"title": task.title})
        messages.success(request, "Task saved.")
        return redirect("tasks")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Create Task", "submit_label": "Save task"})


@login_required
@module_required("ward-intelligence")
@capability_required("submit_reports")
def ward_profile_create(request):
    candidate = _active_candidate(request)
    form = WardProfileForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.candidate = candidate
        profile.created_by = request.user
        profile.updated_by = request.user
        profile.save()
        log_audit(request, "WARD_PROFILE_CREATED", profile, new_value={"ward": profile.ward.name})
        messages.success(request, "Ward intelligence profile saved.")
        return redirect("ward_brief_detail", profile_id=profile.id)
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Create Ward Profile", "submit_label": "Save ward profile"})


@login_required
@module_required("ward-intelligence")
@capability_required("submit_reports")
def ward_profile_edit(request, profile_id):
    candidate = _active_candidate(request)
    profile = get_object_or_404(WardProfile, candidate=candidate, id=profile_id)
    form = WardProfileForm(request.POST or None, instance=profile, candidate=candidate)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.updated_by = request.user
        profile.save()
        log_audit(request, "WARD_PROFILE_UPDATED", profile, new_value={"ward": profile.ward.name})
        messages.success(request, "Ward intelligence profile updated.")
        return redirect("ward_brief_detail", profile_id=profile.id)
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": f"Edit Ward Profile: {profile.ward}", "submit_label": "Save changes"})


@login_required
@module_required("ward-intelligence")
def ward_briefs(request):
    candidate = _active_candidate(request)
    records = WardProfile.objects.filter(candidate=candidate).select_related("ward", "ward__llg").order_by("ward__name")
    return render(request, "campaigns/ward_briefs.html", {"candidate": candidate, "records": records})


@login_required
@module_required("ward-intelligence")
def ward_brief_detail(request, profile_id):
    candidate = _active_candidate(request)
    profile = get_object_or_404(WardProfile.objects.select_related("ward", "ward__llg"), candidate=candidate, id=profile_id)
    payload = build_ward_brief_payload(candidate, profile)
    log_audit(request, "WARD_BRIEF_VIEWED", profile, new_value={"ward": profile.ward.name})
    return render(request, "campaigns/ward_brief_detail.html", {"candidate": candidate, "profile": profile, "payload": payload})


@login_required
@module_required("ai-assistant")
def ward_brief_ai_create(request, profile_id):
    candidate = _active_candidate(request)
    profile = get_object_or_404(WardProfile, candidate=candidate, id=profile_id)
    try:
        work_item = create_ward_ai_work_item(candidate, profile, request.user)
    except ValueError as exc:
        messages.warning(request, str(exc))
        return redirect("usage_dashboard")
    log_audit(request, "AI_WARD_BRIEF_CREATED", work_item, new_value={"ward": profile.ward.name})
    messages.success(request, "Ward brief assistant draft created for human review.")
    return redirect("ai_review", work_item.id)


@login_required
@module_required("ai-assistant")
def ward_speech_create(request, profile_id):
    candidate = _active_candidate(request)
    profile = get_object_or_404(WardProfile, candidate=candidate, id=profile_id)
    try:
        work_item = create_speech_ai_work_item(candidate, profile, user=request.user)
    except ValueError as exc:
        messages.warning(request, str(exc))
        return redirect("usage_dashboard")
    log_audit(request, "AI_SPEECH_NOTES_CREATED", work_item, new_value={"ward": profile.ward.name})
    messages.success(request, "Speech notes draft created for human review.")
    return redirect("ai_review", work_item.id)


def _list_create(request, model, form_class, template, title, success_message, create_route=None, queryset=None):
    candidate = _active_candidate(request)
    records = (queryset or model.objects.filter(candidate=candidate)).order_by("-created_at")[:100]
    if request.method == "POST":
        form = form_class(request.POST, request.FILES or None, candidate=candidate)
        if form.is_valid():
            record = form.save(commit=False)
            record.candidate = candidate
            record.created_by = request.user
            record.updated_by = request.user
            record.save()
            form.save_m2m()
            log_audit(request, f"{model.__name__.upper()}_CREATED", record)
            messages.success(request, success_message)
            return redirect(create_route or request.resolver_match.url_name)
    else:
        form = form_class(candidate=candidate)
    return render(request, template, {"candidate": candidate, "records": records, "form": form, "title": title})


@login_required
@module_required("relationship-calls")
def influencers(request):
    candidate = _active_candidate(request)
    query = request.GET.get("q", "")
    records = Influencer.objects.filter(candidate=candidate).select_related("ward", "village", "assigned_owner").order_by("next_contact_due_date", "full_name")
    if query:
        records = records.filter(Q(full_name__icontains=query) | Q(phone__icontains=query) | Q(community_role__icontains=query))
    return render(request, "campaigns/influencers.html", {"candidate": candidate, "records": records[:100], "query": query})


@login_required
@module_required("relationship-calls")
def influencer_create(request):
    candidate = _active_candidate(request)
    form = InfluencerQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        record = form.save(commit=False)
        record.candidate = candidate
        record.created_by = request.user
        record.updated_by = request.user
        record.save()
        log_audit(request, "INFLUENCER_CREATED", record, new_value={"full_name": record.full_name})
        messages.success(request, "Influencer saved and reminder schedule prepared.")
        return redirect("influencers")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Influencer", "submit_label": "Save influencer"})


@login_required
@module_required("events-tasks")
def events(request):
    candidate = _active_candidate(request)
    records = CampaignEvent.objects.filter(candidate=candidate).select_related("ward", "village", "landmark").order_by("start_datetime")[:100]
    return render(request, "campaigns/events.html", {"candidate": candidate, "records": records})


@login_required
@module_required("events-tasks")
def event_create(request):
    candidate = _active_candidate(request)
    form = EventQuickForm(request.POST or None, request.FILES or None, candidate=candidate)
    if form.is_valid():
        event = form.save(commit=False)
        event.candidate = candidate
        event.created_by = request.user
        event.updated_by = request.user
        event.save()
        log_audit(request, "EVENT_CREATED", event, new_value={"title": event.title})
        messages.success(request, "Event saved with planning fields ready.")
        return redirect("events")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Plan Event", "submit_label": "Save event"})


@login_required
@module_required("ward-intelligence")
def issues(request):
    candidate = _active_candidate(request)
    records = CommunityIssue.objects.filter(candidate=candidate).select_related("ward", "village").order_by("-created_at")[:100]
    promises = PromiseTracker.objects.filter(candidate=candidate).select_related("ward", "follow_up_owner").order_by("target_date")[:60]
    return render(request, "campaigns/issues.html", {"candidate": candidate, "records": records, "promises": promises})


@login_required
@module_required("ward-intelligence")
def issue_create(request):
    candidate = _active_candidate(request)
    form = IssueQuickForm(request.POST or None, request.FILES or None, candidate=candidate)
    if form.is_valid():
        issue = form.save(commit=False)
        issue.candidate = candidate
        issue.created_by = request.user
        issue.updated_by = request.user
        issue.save()
        log_audit(request, "COMMUNITY_ISSUE_CREATED", issue, new_value={"title": issue.title})
        messages.success(request, "Community issue saved.")
        return redirect("issues")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Record Issue", "submit_label": "Save issue"})


@login_required
@module_required("ward-intelligence")
def promise_create(request):
    candidate = _active_candidate(request)
    form = PromiseQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        promise = form.save(commit=False)
        promise.candidate = candidate
        promise.created_by = request.user
        promise.updated_by = request.user
        promise.save()
        log_audit(request, "PROMISE_CREATED", promise, new_value={"title": promise.title})
        messages.success(request, "Promise saved for follow-up.")
        return redirect("issues")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Track Promise", "submit_label": "Save promise"})


@login_required
def reports(request):
    candidate = _active_candidate(request)
    log_audit(request, "REPORT_VIEWED", candidate, new_value={"report": "dashboard_rollup"})
    return render(
        request,
        "campaigns/reports.html",
        {
            "candidate": candidate,
            "metrics": dashboard_metrics(candidate),
            "rollup": report_rollup(candidate),
            "rollup_label": "District" if candidate.uses_district_layer else "LLG",
        },
    )


@login_required
@capability_required("import_data")
def data_operations(request):
    candidate = _active_candidate(request)
    imports = ImportBatch.objects.filter(candidate=candidate)[:20]
    exports = ExportRequest.objects.filter(candidate=candidate)[:20]
    return render(request, "campaigns/data_operations.html", {"candidate": candidate, "imports": imports, "exports": exports})


@login_required
@capability_required("import_data")
def import_create(request):
    candidate = _active_candidate(request)
    form = ImportBatchForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        batch = form.save(commit=False)
        batch.candidate = candidate
        batch.uploaded_by = request.user
        batch.created_by = request.user
        batch.updated_by = request.user
        batch.save()
        process_import_batch(batch)
        log_audit(request, "BULK_IMPORT", batch, new_value={"type": batch.import_type, "valid_rows": batch.valid_rows, "error_rows": batch.error_rows})
        messages.success(request, f"Import processed: {batch.valid_rows} rows imported, {batch.error_rows} rows with errors.")
        return redirect("data_operations")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Import CSV", "submit_label": "Upload and process"})


@login_required
@capability_required("export_data")
def export_create(request):
    candidate = _active_candidate(request)
    form = ExportRequestForm(request.POST or None)
    if form.is_valid():
        export = form.save(commit=False)
        export.candidate = candidate
        export.requested_by = request.user
        export.created_by = request.user
        export.updated_by = request.user
        export.status = "APPROVED" if request.user.is_superuser else "REQUESTED"
        export.save()
        if export.status == "APPROVED":
            export.approved_by = request.user
            export.approved_at = timezone.now()
            build_export_file(export)
        log_audit(request, "EXPORT_REQUESTED", export, new_value={"type": export.export_type, "status": export.status})
        messages.success(request, "Export request saved.")
        return redirect("data_operations")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Request Export", "submit_label": "Save export"})


@login_required
@capability_required("export_data")
def export_download(request, export_id):
    candidate = _active_candidate(request)
    export = get_object_or_404(ExportRequest, candidate=candidate, id=export_id)
    if export.status != "READY":
        build_export_file(export)
    log_audit(request, "EXPORT_DOWNLOADED", export, new_value={"type": export.export_type})
    return FileResponse(export.output_file.open("rb"), as_attachment=True, filename=export.output_file.name.split("/")[-1])


@login_required
@module_required("polling-war-room")
def polling(request):
    candidate = _active_candidate(request)
    locations = PollingLocation.objects.filter(candidate=candidate).select_related("ward", "assigned_scrutineer").order_by("ward__name", "name")
    incidents = PollingIncident.objects.filter(candidate=candidate).exclude(status="RESOLVED").order_by("-created_at")[:20]
    statuses = PollingStatus.objects.filter(candidate=candidate).select_related("polling_location", "reported_by")[:20]
    return render(request, "campaigns/polling.html", {"candidate": candidate, "locations": locations, "incidents": incidents, "statuses": statuses})


@login_required
@module_required("polling-war-room")
def polling_location_create(request):
    candidate = _active_candidate(request)
    form = PollingLocationQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        location = form.save(commit=False)
        location.candidate = candidate
        location.created_by = request.user
        location.updated_by = request.user
        location.save()
        log_audit(request, "POLLING_LOCATION_CREATED", location, new_value={"name": location.name})
        messages.success(request, "Polling location saved.")
        return redirect("polling")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Polling Location", "submit_label": "Save location"})


@login_required
@module_required("polling-war-room")
def polling_status_create(request):
    candidate = _active_candidate(request)
    form = PollingStatusQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        status = form.save(commit=False)
        status.candidate = candidate
        status.created_by = request.user
        status.updated_by = request.user
        status.save()
        log_audit(request, "POLLING_STATUS_CREATED", status, new_value={"location": status.polling_location.name})
        messages.success(request, "Polling status update saved.")
        return redirect("polling")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Polling Status Update", "submit_label": "Save status"})


@login_required
@module_required("polling-war-room")
def polling_incident_create(request):
    candidate = _active_candidate(request)
    form = PollingIncidentQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        incident = form.save(commit=False)
        incident.candidate = candidate
        incident.created_by = request.user
        incident.updated_by = request.user
        incident.save()
        log_audit(request, "POLLING_INCIDENT_CREATED", incident, new_value={"title": incident.title})
        messages.success(request, "Polling incident saved.")
        return redirect("polling")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Report Polling Incident", "submit_label": "Save incident"})


@login_required
@module_required("constituency-management")
def constituency(request):
    candidate = _active_candidate(request)
    records = CitizenRequest.objects.filter(candidate=candidate).select_related("ward", "assigned_to").order_by("-created_at")[:100]
    return render(request, "campaigns/constituency.html", {"candidate": candidate, "records": records})


@login_required
@module_required("constituency-management")
def citizen_request_create(request):
    candidate = _active_candidate(request)
    form = CitizenRequestQuickForm(request.POST or None, candidate=candidate)
    if form.is_valid():
        record = form.save(commit=False)
        record.candidate = candidate
        record.created_by = request.user
        record.updated_by = request.user
        record.save()
        log_audit(request, "CITIZEN_REQUEST_CREATED", record, new_value={"title": record.title})
        messages.success(request, "Citizen request saved.")
        return redirect("constituency")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Citizen Request", "submit_label": "Save request"})


@login_required
@module_required("ai-assistant")
def ai_work_items(request):
    candidate = _active_candidate(request)
    records = AIWorkItem.objects.filter(candidate=candidate).select_related("ward", "event").order_by("-created_at")[:100]
    return render(request, "campaigns/ai.html", {"candidate": candidate, "records": records})


@login_required
@module_required("ai-assistant")
def ai_review(request, item_id):
    candidate = _active_candidate(request)
    item = get_object_or_404(AIWorkItem, candidate=candidate, id=item_id)
    form = AIReviewForm(request.POST or None, instance=item)
    if form.is_valid():
        item = form.save(commit=False)
        item.reviewed_by = request.user
        item.reviewed_at = timezone.now()
        item.updated_by = request.user
        item.save()
        log_audit(request, "AI_DRAFT_REVIEWED", item, new_value={"status": item.status})
        messages.success(request, "AI draft review saved.")
        return redirect("ai_work_items")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Review AI Draft", "submit_label": "Save review"})


# ── PNG campaign feature views ────────────────────────────────────────────────

@login_required
def preference_deals(request):
    candidate = _active_candidate(request)
    records = PreferenceDeal.objects.filter(candidate=candidate).order_by("-created_at")
    return render(request, "campaigns/preference_deals.html", {"candidate": candidate, "records": records})


@login_required
@capability_required("manage_settings")
def preference_deal_create(request):
    candidate = _active_candidate(request)
    form = PreferenceDealForm(candidate, request.POST or None)
    if form.is_valid():
        deal = form.save(commit=False)
        deal.candidate = candidate
        deal.created_by = request.user
        deal.updated_by = request.user
        deal.save()
        log_audit(request, "PREFERENCE_DEAL_CREATED", deal, new_value={"partner": deal.partner_candidate_name})
        messages.success(request, f"Preference deal with {deal.partner_candidate_name} saved.")
        return redirect("preference_deals")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "New Preference Deal", "submit_label": "Save deal"})


@login_required
@capability_required("manage_settings")
def preference_deal_edit(request, deal_id):
    candidate = _active_candidate(request)
    deal = get_object_or_404(PreferenceDeal, candidate=candidate, id=deal_id)
    form = PreferenceDealForm(candidate, request.POST or None, instance=deal)
    if form.is_valid():
        deal = form.save(commit=False)
        deal.updated_by = request.user
        deal.save()
        log_audit(request, "PREFERENCE_DEAL_UPDATED", deal, new_value={"status": deal.status})
        messages.success(request, "Preference deal updated.")
        return redirect("preference_deals")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": f"Edit Deal — {deal.partner_candidate_name}", "submit_label": "Save changes"})


@login_required
def community_groups(request):
    candidate = _active_candidate(request)
    ward_id = request.GET.get("ward")
    records = CommunityGroup.objects.filter(candidate=candidate).select_related("ward", "village", "key_contact")
    if ward_id:
        records = records.filter(ward_id=ward_id)
    return render(request, "campaigns/community_groups.html", {"candidate": candidate, "records": records, "wards": candidate.available_wards()})


@login_required
def community_group_create(request):
    candidate = _active_candidate(request)
    form = CommunityGroupForm(candidate, request.POST or None)
    if form.is_valid():
        group = form.save(commit=False)
        group.candidate = candidate
        group.created_by = request.user
        group.updated_by = request.user
        group.save()
        log_audit(request, "COMMUNITY_GROUP_CREATED", group, new_value={"name": group.name, "ward": group.ward.name})
        messages.success(request, f"Community group '{group.name}' saved.")
        return redirect("community_groups")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "New Community Group", "submit_label": "Save group"})


@login_required
def community_group_edit(request, group_id):
    candidate = _active_candidate(request)
    group = get_object_or_404(CommunityGroup, candidate=candidate, id=group_id)
    form = CommunityGroupForm(candidate, request.POST or None, instance=group)
    if form.is_valid():
        group = form.save(commit=False)
        group.updated_by = request.user
        group.save()
        log_audit(request, "COMMUNITY_GROUP_UPDATED", group, new_value={"alignment": group.alignment})
        messages.success(request, "Community group updated.")
        return redirect("community_groups")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": f"Edit — {group.name}", "submit_label": "Save changes"})


@login_required
def community_assistance(request):
    candidate = _active_candidate(request)
    records = CommunityAssistance.objects.filter(candidate=candidate).select_related("ward", "village", "approved_by").order_by("-date")[:200]
    total_pgk = sum(r.estimated_value_pgk for r in records)
    return render(request, "campaigns/community_assistance.html", {"candidate": candidate, "records": records, "total_pgk": total_pgk})


@login_required
@capability_required("manage_settings")
def community_assistance_create(request):
    candidate = _active_candidate(request)
    form = CommunityAssistanceForm(candidate, request.POST or None)
    if form.is_valid():
        record = form.save(commit=False)
        record.candidate = candidate
        record.created_by = request.user
        record.updated_by = request.user
        record.save()
        log_audit(request, "COMMUNITY_ASSISTANCE_CREATED", record, new_value={"type": record.assistance_type, "value": str(record.estimated_value_pgk)})
        messages.success(request, "Community assistance record saved.")
        return redirect("community_assistance")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Record Community Assistance", "submit_label": "Save record"})


@login_required
def competitor_activities(request):
    candidate = _active_candidate(request)
    records = CompetitorActivity.objects.filter(candidate=candidate).select_related("ward", "response_assigned_to").order_by("-date")[:200]
    return render(request, "campaigns/competitor_activities.html", {"candidate": candidate, "records": records})


@login_required
def competitor_activity_create(request):
    candidate = _active_candidate(request)
    form = CompetitorActivityForm(candidate, request.POST or None)
    if form.is_valid():
        record = form.save(commit=False)
        record.candidate = candidate
        record.created_by = request.user
        record.updated_by = request.user
        record.save()
        log_audit(request, "COMPETITOR_ACTIVITY_CREATED", record, new_value={"opponent": record.opponent_name, "type": record.activity_type})
        messages.success(request, "Competitor activity logged.")
        return redirect("competitor_activities")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Log Competitor Activity", "submit_label": "Save"})


@login_required
def competitor_activity_edit(request, activity_id):
    candidate = _active_candidate(request)
    record = get_object_or_404(CompetitorActivity, candidate=candidate, id=activity_id)
    form = CompetitorActivityForm(candidate, request.POST or None, instance=record)
    if form.is_valid():
        record = form.save(commit=False)
        record.updated_by = request.user
        record.save()
        messages.success(request, "Competitor activity updated.")
        return redirect("competitor_activities")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": f"Edit — {record.opponent_name}", "submit_label": "Save changes"})


@login_required
def development_funds(request):
    candidate = _active_candidate(request)
    records = DevelopmentFund.objects.filter(candidate=candidate).select_related("ward", "district").order_by("-financial_year", "fund_name")
    return render(request, "campaigns/development_funds.html", {"candidate": candidate, "records": records})


@login_required
@capability_required("manage_settings")
def development_fund_create(request):
    candidate = _active_candidate(request)
    form = DevelopmentFundForm(candidate, request.POST or None)
    if form.is_valid():
        record = form.save(commit=False)
        record.candidate = candidate
        record.created_by = request.user
        record.updated_by = request.user
        record.save()
        log_audit(request, "DEVELOPMENT_FUND_CREATED", record, new_value={"fund": record.fund_name, "year": record.financial_year})
        messages.success(request, f"Fund '{record.fund_name}' saved.")
        return redirect("development_funds")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "Add Development Fund", "submit_label": "Save fund"})


@login_required
@capability_required("manage_settings")
def development_fund_edit(request, fund_id):
    candidate = _active_candidate(request)
    record = get_object_or_404(DevelopmentFund, candidate=candidate, id=fund_id)
    form = DevelopmentFundForm(candidate, request.POST or None, instance=record)
    if form.is_valid():
        record = form.save(commit=False)
        record.updated_by = request.user
        record.save()
        log_audit(request, "DEVELOPMENT_FUND_UPDATED", record, new_value={"spent": str(record.spent_pgk)})
        messages.success(request, "Fund updated.")
        return redirect("development_funds")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": f"Edit — {record.fund_name}", "submit_label": "Save changes"})


@login_required
def registration_drives(request):
    candidate = _active_candidate(request)
    records = RegistrationDrive.objects.filter(candidate=candidate).select_related("ward").prefetch_related("team_members")
    return render(request, "campaigns/registration_drives.html", {"candidate": candidate, "records": records})


@login_required
def registration_drive_create(request):
    candidate = _active_candidate(request)
    form = RegistrationDriveForm(candidate, request.POST or None)
    if form.is_valid():
        record = form.save(commit=False)
        record.candidate = candidate
        record.created_by = request.user
        record.updated_by = request.user
        record.save()
        form.save_m2m()
        log_audit(request, "REGISTRATION_DRIVE_CREATED", record, new_value={"ward": record.ward.name, "target": record.target_count})
        messages.success(request, f"Registration drive '{record.title}' created.")
        return redirect("registration_drives")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": "New Registration Drive", "submit_label": "Create drive"})


@login_required
def registration_drive_edit(request, drive_id):
    candidate = _active_candidate(request)
    record = get_object_or_404(RegistrationDrive, candidate=candidate, id=drive_id)
    form = RegistrationDriveForm(candidate, request.POST or None, instance=record)
    if form.is_valid():
        record = form.save(commit=False)
        record.updated_by = request.user
        record.save()
        form.save_m2m()
        log_audit(request, "REGISTRATION_DRIVE_UPDATED", record, new_value={"actual_count": record.actual_count, "status": record.status})
        messages.success(request, "Registration drive updated.")
        return redirect("registration_drives")
    return render(request, "campaigns/form.html", {"candidate": candidate, "form": form, "title": f"Edit — {record.title}", "submit_label": "Save changes"})


@login_required
def polling_command_center(request):
    """Polling-day live command center: booth tallies, security risks, scrutineer status."""
    candidate = _active_candidate(request)
    locations = PollingLocation.objects.filter(candidate=candidate).select_related(
        "ward", "assigned_scrutineer", "backup_scrutineer"
    ).prefetch_related("status_updates").order_by("ward__name", "name")

    total_our_tally = 0
    for loc in locations:
        latest = loc.status_updates.first()
        loc.latest_status = latest
        if latest and latest.our_tally:
            total_our_tally += latest.our_tally

    return render(request, "campaigns/polling_command_center.html", {
        "candidate": candidate,
        "locations": locations,
        "total_our_tally": total_our_tally,
    })
