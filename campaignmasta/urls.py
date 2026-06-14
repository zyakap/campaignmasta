from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from campaigns import marketing_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("saas-admin/", include("campaigns.saas_urls")),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="campaigns/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/", include("campaignmasta.api_urls")),
    # Marketing pages (public, no auth required)
    path("", marketing_views.home, name="marketing_home"),
    path("features/", marketing_views.features, name="marketing_features"),
    path("pricing/", marketing_views.pricing, name="marketing_pricing"),
    path("subscription-interest/", marketing_views.subscription_interest, name="marketing_subscription_interest"),
    path("download/", marketing_views.download, name="marketing_download"),
    path("", include("campaigns.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
