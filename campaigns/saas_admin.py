"""
Custom SaaS Admin Site for CampaignMasta platform operators.
Accessible at /saas-admin/ — separate from the candidate-facing /admin/.
"""
from django.contrib.admin import AdminSite
from django.db.models import Count, F, Q, Sum
from django.utils import timezone


class SaaSAdminSite(AdminSite):
    site_header = "CampaignMasta Platform Admin"
    site_title = "CampaignMasta SaaS"
    index_title = "Platform Control Centre"
    site_url = "/"
    index_template = "saas_admin/index.html"
    login_template = "saas_admin/login.html"
    app_index_template = "saas_admin/app_index.html"

    def index(self, request, extra_context=None):
        from .models import (
            Candidate,
            Subscription,
            SupportTicket,
            UsageEvent,
            UsageWallet,
        )

        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        tenant_qs = Candidate.objects.values("status").annotate(count=Count("id"))
        tenant_by_status = {row["status"]: row["count"] for row in tenant_qs}

        active_tenants = tenant_by_status.get("ACTIVE", 0)
        trial_tenants = tenant_by_status.get("TRIAL", 0)
        suspended_tenants = tenant_by_status.get("SUSPENDED", 0)
        total_tenants = Candidate.objects.count()

        active_subs = Subscription.objects.filter(status="ACTIVE").count()
        revenue_mtd = (
            UsageEvent.objects.filter(
                created_at__gte=month_start,
                status="BILLED",
            ).aggregate(total=Sum("customer_charge"))["total"]
            or 0
        )

        open_tickets = SupportTicket.objects.filter(status__in=["OPEN", "IN_PROGRESS"]).count()
        sensitive_access = SupportTicket.objects.filter(
            temporary_sensitive_access=True,
            status__in=["OPEN", "IN_PROGRESS"],
        ).count()

        low_balance_wallets = UsageWallet.objects.filter(
            is_active=True,
            balance__lte=F("low_balance_threshold"),
        ).count()

        recent_events = UsageEvent.objects.select_related("candidate").order_by("-created_at")[:10]
        recent_tenants = Candidate.objects.order_by("-created_at")[:5]
        recent_tickets = SupportTicket.objects.order_by("-created_at")[:5]

        extra_context = extra_context or {}
        extra_context.update(
            {
                "saas_stats": {
                    "total_tenants": total_tenants,
                    "active_tenants": active_tenants,
                    "trial_tenants": trial_tenants,
                    "suspended_tenants": suspended_tenants,
                    "active_subscriptions": active_subs,
                    "revenue_mtd": revenue_mtd,
                    "open_tickets": open_tickets,
                    "sensitive_access_tickets": sensitive_access,
                    "low_balance_wallets": low_balance_wallets,
                },
                "recent_events": recent_events,
                "recent_tenants": recent_tenants,
                "recent_tickets": recent_tickets,
            }
        )
        return super().index(request, extra_context)

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        ORDER = [
            "Tenants & Billing",
            "Platform Modules",
            "Usage & Wallets",
            "Geography",
            "Support & Ops",
            "Audit & Logs",
        ]
        order_map = {name: i for i, name in enumerate(ORDER)}
        app_list.sort(key=lambda a: order_map.get(a["name"], 99))
        return app_list


saas_admin_site = SaaSAdminSite(name="saas_admin")
