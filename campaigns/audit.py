from .models import AuditLog, Notification, ReminderEscalation


def client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def log_audit(request, action, obj=None, old_value=None, new_value=None, candidate=None):
    candidate = candidate or getattr(request, "campaign_candidate", None)
    return AuditLog.objects.create(
        user=request.user if getattr(request, "user", None) and request.user.is_authenticated else None,
        candidate=candidate,
        action=action,
        object_type=obj.__class__.__name__ if obj else "",
        object_id=str(getattr(obj, "id", "")) if obj else "",
        old_value=old_value,
        new_value=new_value,
        ip_address=client_ip(request),
        device=request.META.get("HTTP_USER_AGENT", "")[:220],
    )


def notify_team_member(candidate, recipient, title, body, related_object=None, channel="IN_APP", user=None):
    return Notification.objects.create(
        candidate=candidate,
        recipient=recipient,
        title=title,
        body=body,
        channel=channel,
        related_object_type=related_object.__class__.__name__ if related_object else "",
        related_object_id=str(getattr(related_object, "id", "")) if related_object else "",
        created_by=user,
        updated_by=user,
    )


def create_escalation(candidate, title, owner, escalated_to, reason, due_date=None, user=None):
    escalation = ReminderEscalation.objects.create(
        candidate=candidate,
        title=title,
        owner=owner,
        escalated_to=escalated_to,
        reason=reason,
        due_date=due_date,
        created_by=user,
        updated_by=user,
    )
    if escalated_to:
        notify_team_member(
            candidate,
            escalated_to,
            title,
            reason,
            related_object=escalation,
            user=user,
        )
    return escalation
