def campaign_context(request):
    return {
        "active_campaign_candidate": getattr(request, "campaign_candidate", None),
        "enabled_campaign_modules": getattr(request, "enabled_campaign_modules", set()),
    }
