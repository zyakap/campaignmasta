from .services import candidates_for_user


def campaign_context(request):
    user = getattr(request, "user", None)
    return {
        "active_campaign_candidate": getattr(request, "campaign_candidate", None),
        "enabled_campaign_modules": getattr(request, "enabled_campaign_modules", set()),
        # Candidate switcher options, scoped to what the user is allowed to access.
        "available_candidates": candidates_for_user(user) if user is not None else [],
    }
