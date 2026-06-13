from .audit import client_ip
from .models import AccessLog
from .services import enabled_module_codes, resolve_active_candidate


class ActiveTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.campaign_candidate = None
        request.enabled_campaign_modules = set()
        candidate = resolve_active_candidate(request)
        if candidate:
            request.campaign_candidate = candidate
            request.enabled_campaign_modules = enabled_module_codes(candidate)
        response = self.get_response(request)
        if request.path.startswith(("/static/", "/media/")):
            return response
        if getattr(request, "user", None) and request.user.is_authenticated:
            AccessLog.objects.create(
                user=request.user,
                candidate=request.campaign_candidate,
                path=request.path[:260],
                method=request.method,
                status_code=response.status_code,
                ip_address=client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", "")[:260],
            )
        return response
