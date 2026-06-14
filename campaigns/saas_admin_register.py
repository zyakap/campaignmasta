"""
Register all models with the SaaS admin site, organised into logical groups
by overriding each ModelAdmin's app_label via a custom Meta proxy trick.
We use plain ModelAdmin subclasses pointing to the same models.
"""
from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


class SaaSTemplateMixin:
    """Point every SaaS admin view at the AdminLTE-wrapped templates."""
    change_list_template = "saas_admin/change_list.html"
    change_form_template = "saas_admin/change_form.html"
    delete_confirmation_template = "saas_admin/delete_confirmation.html"
    object_history_template = "saas_admin/object_history.html"


from .models import (
    AIWorkItem,
    AccessLog,
    AuditLog,
    CallLog,
    CampaignEvent,
    CampaignTask,
    CandidateProfile,
    Candidate,
    CitizenRequest,
    CommunityGrant,
    CommunityIssue,
    ConnectorSetting,
    DataLifecycleRequest,
    DevelopmentProject,
    District,
    EventAttendance,
    EventChecklistItem,
    ExportRequest,
    FreeAIModel,
    ImportBatch,
    IncludedUsageQuota,
    Influencer,
    LLG,
    Landmark,
    Message,
    MessageRecipient,
    ModuleBundle,
    ModulePrice,
    Notification,
    PollingIncident,
    PollingLocation,
    PollingStatus,
    PromiseTracker,
    Province,
    ReminderEscalation,
    SoftwareModule,
    Subscription,
    SubscriptionQuote,
    SubscriptionInterest,
    Supporter,
    SupportTicket,
    TeamMember,
    TenantModuleSubscription,
    TenantSettings,
    TenantUsageQuota,
    UsageEvent,
    UsageRateCard,
    UsageTopUp,
    UsageWallet,
    Village,
    Ward,
    WardDevelopmentPlan,
    WardProfile,
)
from .saas_admin import saas_admin_site


# ─── Tenants & Billing ────────────────────────────────────────────────────────

class CandidateForm(forms.ModelForm):
    """Candidate form that embeds login-credential creation."""

    # ── Login credentials ──────────────────────────────────────────────────────
    username = forms.CharField(
        label="Login username",
        max_length=150,
        help_text="The username the candidate uses to log in to their campaign app.",
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text="Min 8 characters. Leave blank when editing to keep the current password.",
    )
    password_confirm = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(render_value=False),
        required=False,
    )

    class Meta:
        model = Candidate
        exclude = ("user", "created_by", "updated_by")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if instance and instance.pk and instance.user_id:
            self.fields["username"].initial = instance.user.username
            self.fields["username"].help_text = (
                "Current login username. Changing this updates the linked account."
            )
            self.fields["password"].required = False
        else:
            self.fields["password"].required = True
            self.fields["password"].help_text = "Required when creating a new candidate."

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        pw2 = cleaned.get("password_confirm")
        username = cleaned.get("username")

        # Username uniqueness check (exclude own linked user on edit)
        if username:
            qs = User.objects.filter(username=username)
            if self.instance.pk and self.instance.user_id:
                qs = qs.exclude(pk=self.instance.user_id)
            if qs.exists():
                self.add_error("username", f"Username '{username}' is already taken.")

        # Password validation
        if pw:
            if pw != pw2:
                self.add_error("password_confirm", "Passwords do not match.")
            else:
                try:
                    validate_password(pw)
                except DjangoValidationError as exc:
                    self.add_error("password", exc)
        elif not self.instance.pk:
            self.add_error("password", "Password is required when creating a new candidate.")

        return cleaned


class CandidateProfileInline(admin.StackedInline):
    model = CandidateProfile
    fk_name = "candidate"
    extra = 1
    min_num = 0
    max_num = 1
    can_delete = False
    verbose_name = "Candidate Profile"
    verbose_name_plural = "Candidate Profile"
    exclude = ("created_by", "updated_by")


class CandidateSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    form = CandidateForm
    inlines = [CandidateProfileInline]
    list_display = ("name", "login_username", "candidate_type", "province", "district", "subscription_plan", "status", "created_at")
    list_filter = ("candidate_type", "subscription_plan", "status", "province")
    search_fields = ("name", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at", "login_account_info")
    fieldsets = (
        ("Login Credentials", {
            "fields": ("username", "password", "password_confirm"),
            "description": "These credentials are used by the candidate to log in to their campaign dashboard.",
        }),
        ("Identity", {"fields": ("name", "candidate_type", "province", "district")}),
        ("Subscription", {"fields": ("subscription_plan", "status", "constituency_mode")}),
        ("Account Info", {"fields": ("login_account_info", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def login_username(self, obj):
        return obj.user.username if obj.user else "—"
    login_username.short_description = "Login username"

    def login_account_info(self, obj):
        if obj.user:
            return (
                f"Username: {obj.user.username} | "
                f"Email: {obj.user.email or '—'} | "
                f"Last login: {obj.user.last_login or 'Never'} | "
                f"Active: {'Yes' if obj.user.is_active else 'No'}"
            )
        return "No login account linked yet."
    login_account_info.short_description = "Linked account summary"

    def save_model(self, request, obj, form, change):
        username = form.cleaned_data["username"]
        password = form.cleaned_data.get("password")

        if change and obj.user_id:
            # Update existing user
            user = obj.user
            if user.username != username:
                user.username = username
            if password:
                user.set_password(password)
            user.save()
        else:
            # Create new user
            user = User.objects.create_user(username=username, password=password)
            obj.user = user

        super().save_model(request, obj, form, change)


class SubscriptionInterestSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("full_name", "candidate_option", "province", "district", "mobile_number", "email", "meeting_appointment", "status", "created_at")
    list_filter = ("status", "candidate_option", "province", "district")
    search_fields = ("full_name", "mobile_number", "whatsapp_number", "email")
    readonly_fields = ("created_at", "updated_at", "whatsapp_contact")
    fieldsets = (
        ("Request", {"fields": ("status", "full_name", "candidate_option", "province", "district")}),
        ("Contact", {"fields": ("mobile_number", "whatsapp_number", "whatsapp_contact", "email", "meeting_appointment")}),
        ("Internal follow-up", {"fields": ("internal_notes",)}),
        ("Audit", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


class SubscriptionSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("candidate", "plan", "billing_cycle", "status", "amount", "start_date", "end_date")
    list_filter = ("plan", "billing_cycle", "status")
    search_fields = ("candidate__name", "invoice_number")
    readonly_fields = ("created_at", "updated_at")


class SubscriptionQuoteSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("candidate", "billing_cycle", "currency", "subtotal", "discount_amount", "total", "accepted_at", "created_at")
    list_filter = ("billing_cycle", "currency")
    search_fields = ("candidate__name", "notes")
    filter_horizontal = ("modules", "bundles")
    readonly_fields = ("created_at",)


class TenantModuleSubscriptionSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("candidate", "module", "source", "bundle", "is_enabled", "start_date", "end_date", "price_locked")
    list_filter = ("module__category", "source", "is_enabled")
    search_fields = ("candidate__name", "module__name", "module__code")


saas_admin_site.register(Candidate, CandidateSaaSAdmin)
saas_admin_site.register(SubscriptionInterest, SubscriptionInterestSaaSAdmin)
saas_admin_site.register(Subscription, SubscriptionSaaSAdmin)
saas_admin_site.register(SubscriptionQuote, SubscriptionQuoteSaaSAdmin)
saas_admin_site.register(TenantModuleSubscription, TenantModuleSubscriptionSaaSAdmin)


# ─── Platform Modules ─────────────────────────────────────────────────────────

class ModulePriceInline(admin.TabularInline):
    model = ModulePrice
    extra = 0


class IncludedUsageQuotaInline(admin.TabularInline):
    model = IncludedUsageQuota
    fk_name = "module"
    extra = 0


class SoftwareModuleSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("name", "code", "category", "is_core", "is_active", "sort_order")
    list_filter = ("category", "is_core", "is_active")
    search_fields = ("name", "code", "description")
    inlines = [ModulePriceInline, IncludedUsageQuotaInline]


class BundleIncludedUsageQuotaInline(admin.TabularInline):
    model = IncludedUsageQuota
    fk_name = "bundle"
    extra = 0


class ModuleBundleSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("name", "code", "billing_cycle", "currency", "bundle_price", "discount_percent", "is_full_package", "is_active")
    list_filter = ("billing_cycle", "currency", "is_full_package", "is_active")
    search_fields = ("name", "code", "description")
    filter_horizontal = ("modules",)
    inlines = [BundleIncludedUsageQuotaInline]


class FreeAIModelSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("name", "provider", "model_id", "daily_free_requests", "monthly_free_requests", "is_active")
    list_filter = ("provider", "is_active")
    search_fields = ("name", "provider", "model_id")


class ConnectorSettingSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("name", "candidate", "connector_type", "provider", "is_enabled", "status", "last_tested_at")
    list_filter = ("connector_type", "provider", "is_enabled", "status")
    search_fields = ("name", "provider", "api_base_url")
    readonly_fields = ("last_tested_at", "last_test_result")
    change_form_template = "saas_admin/connectorsetting_change_form.html"


saas_admin_site.register(SoftwareModule, SoftwareModuleSaaSAdmin)
saas_admin_site.register(ModuleBundle, ModuleBundleSaaSAdmin)
saas_admin_site.register(FreeAIModel, FreeAIModelSaaSAdmin)
saas_admin_site.register(ConnectorSetting, ConnectorSettingSaaSAdmin)


# ─── Usage & Wallets ──────────────────────────────────────────────────────────

class UsageWalletSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("candidate", "service", "currency", "balance", "free_units_remaining", "low_balance_threshold", "is_active")
    list_filter = ("service", "currency", "is_active")
    search_fields = ("candidate__name",)


class UsageEventSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("candidate", "service", "action", "quantity", "billable_quantity", "unit", "customer_charge", "status", "created_at")
    list_filter = ("service", "unit", "status")
    search_fields = ("candidate__name", "action", "reference")
    readonly_fields = ("created_at", "updated_at")


class UsageTopUpSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("candidate", "wallet", "amount", "currency", "payment_method", "payment_reference", "received_at", "received_by")
    list_filter = ("wallet__service", "currency", "payment_method")
    search_fields = ("candidate__name", "payment_reference")


class UsageRateCardSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("service", "provider", "model_name", "unit", "currency", "provider_cost_per_unit", "markup_percent", "fixed_markup_per_unit", "minimum_charge", "is_free", "is_active")
    list_filter = ("service", "provider", "unit", "currency", "is_free", "is_active")
    search_fields = ("provider", "model_name")


class TenantUsageQuotaSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("candidate", "subscription", "service", "unit", "included_quantity", "used_quantity", "remaining_quantity", "reset_period_end", "is_active")
    list_filter = ("service", "unit", "is_active")
    search_fields = ("candidate__name",)


class IncludedUsageQuotaSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("module", "bundle", "service", "unit", "quantity", "billing_cycle", "is_active")
    list_filter = ("service", "unit", "billing_cycle", "is_active")


saas_admin_site.register(UsageWallet, UsageWalletSaaSAdmin)
saas_admin_site.register(UsageEvent, UsageEventSaaSAdmin)
saas_admin_site.register(UsageTopUp, UsageTopUpSaaSAdmin)
saas_admin_site.register(UsageRateCard, UsageRateCardSaaSAdmin)
saas_admin_site.register(TenantUsageQuota, TenantUsageQuotaSaaSAdmin)
saas_admin_site.register(IncludedUsageQuota, IncludedUsageQuotaSaaSAdmin)


# ─── Geography ────────────────────────────────────────────────────────────────

saas_admin_site.register(Province)
saas_admin_site.register(District)
saas_admin_site.register(LLG)
saas_admin_site.register(Ward)
saas_admin_site.register(Village)


# ─── Support & Ops ────────────────────────────────────────────────────────────

class SupportTicketSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "status", "temporary_sensitive_access", "assigned_to", "created_at")
    list_filter = ("status", "temporary_sensitive_access")
    search_fields = ("title", "description", "requested_by")


class ImportBatchSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("import_type", "candidate", "status", "total_rows", "valid_rows", "error_rows", "created_at")
    list_filter = ("import_type", "status")


class ExportRequestSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("export_type", "candidate", "requested_by", "approved_by", "status", "created_at")
    list_filter = ("export_type", "status")


class DataLifecycleRequestSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("request_type", "candidate", "requested_by", "status", "reviewed_by", "reviewed_at")
    list_filter = ("request_type", "status")
    search_fields = ("requested_by", "reason")


saas_admin_site.register(SupportTicket, SupportTicketSaaSAdmin)
saas_admin_site.register(ImportBatch, ImportBatchSaaSAdmin)
saas_admin_site.register(ExportRequest, ExportRequestSaaSAdmin)
saas_admin_site.register(DataLifecycleRequest, DataLifecycleRequestSaaSAdmin)


# ─── Audit & Logs ─────────────────────────────────────────────────────────────

class AuditLogSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("action", "candidate", "user", "object_type", "object_id", "timestamp")
    list_filter = ("action", "object_type")
    search_fields = ("action", "object_type", "object_id")
    readonly_fields = ("timestamp",)


class AccessLogSaaSAdmin(SaaSTemplateMixin, admin.ModelAdmin):
    list_display = ("user", "candidate", "method", "path", "status_code", "ip_address", "created_at")
    list_filter = ("method", "status_code")
    search_fields = ("path", "ip_address")
    readonly_fields = ("created_at",)


saas_admin_site.register(AuditLog, AuditLogSaaSAdmin)
saas_admin_site.register(AccessLog, AccessLogSaaSAdmin)
