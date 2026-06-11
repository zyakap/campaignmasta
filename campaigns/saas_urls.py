from django.urls import path

from .saas_admin import saas_admin_site

urlpatterns = [
    path("", saas_admin_site.urls),
]
