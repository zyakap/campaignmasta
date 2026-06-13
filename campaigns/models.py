from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CandidateType(models.TextChoices):
    DISTRICT_OPEN = "DISTRICT_OPEN", "District Open"
    PROVINCIAL = "PROVINCIAL", "Provincial"


class Province(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="districts")
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("province", "name")
        ordering = ["province__name", "name"]

    def __str__(self):
        return self.name


class LLG(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="llgs")
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("district", "name")
        ordering = ["district__name", "name"]

    def __str__(self):
        return self.name


class Ward(models.Model):
    llg = models.ForeignKey(LLG, on_delete=models.CASCADE, related_name="wards")
    name = models.CharField(max_length=120)
    number = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = ("llg", "name")
        ordering = ["llg__name", "name"]

    def __str__(self):
        return self.name


class Village(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="villages")
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("ward", "name")
        ordering = ["ward__name", "name"]

    def __str__(self):
        return self.name


class Candidate(TimeStampedModel):
    class Status(models.TextChoices):
        TRIAL = "TRIAL", "Trial"
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        ARCHIVED = "ARCHIVED", "Archived"

    class Plan(models.TextChoices):
        STARTER = "STARTER", "Starter"
        PROFESSIONAL = "PROFESSIONAL", "Professional"
        FULL_PACKAGE = "FULL_PACKAGE", "Full Package"

    name = models.CharField(max_length=160)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="candidate_tenant",
        help_text="The login account for this candidate.",
    )
    candidate_type = models.CharField(max_length=24, choices=CandidateType.choices)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    subscription_plan = models.CharField(max_length=24, choices=Plan.choices, default=Plan.STARTER)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.TRIAL)
    constituency_mode = models.BooleanField(
        default=False,
        help_text="Switch to post-election constituency service mode. Hides campaign-only features and promotes constituency management.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def clean(self):
        if self.candidate_type == CandidateType.DISTRICT_OPEN and not self.district:
            raise ValidationError({"district": "District Open candidates must select one district."})
        if self.candidate_type == CandidateType.PROVINCIAL and self.district:
            raise ValidationError({"district": "Provincial candidates use all districts in the province."})
        if self.district and self.district.province_id != self.province_id:
            raise ValidationError({"district": "District must belong to the selected province."})

    def __str__(self):
        return self.name

    @property
    def uses_district_layer(self):
        return self.candidate_type == CandidateType.PROVINCIAL

    def available_districts(self):
        qs = District.objects.filter(province=self.province)
        if self.candidate_type == CandidateType.DISTRICT_OPEN and self.district_id:
            return qs.filter(id=self.district_id)
        return qs

    def available_llgs(self):
        return LLG.objects.filter(district__in=self.available_districts())

    def available_wards(self):
        return Ward.objects.filter(llg__in=self.available_llgs())


class TenantOwnedModel(TimeStampedModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="%(class)ss", db_column="tenant_id")

    class Meta:
        abstract = True


class CandidateProfile(TenantOwnedModel):
    full_name = models.CharField(max_length=160)
    photo = models.ImageField(upload_to="candidate_photos/", blank=True)
    party = models.CharField(max_length=160, blank=True)
    slogan = models.CharField(max_length=220, blank=True)
    biography = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    campaign_office = models.TextField(blank=True)
    campaign_start_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class BillingCycle(models.TextChoices):
    MONTHLY = "MONTHLY", "Monthly"
    QUARTERLY = "QUARTERLY", "Quarterly"
    ANNUAL = "ANNUAL", "Annual"
    CAMPAIGN_PERIOD = "CAMPAIGN_PERIOD", "Campaign Period"


class Subscription(TenantOwnedModel):
    class Status(models.TextChoices):
        TRIAL = "TRIAL", "Trial"
        ACTIVE = "ACTIVE", "Active"
        OVERDUE = "OVERDUE", "Overdue"
        SUSPENDED = "SUSPENDED", "Suspended"
        CANCELLED = "CANCELLED", "Cancelled"

    plan = models.CharField(max_length=24, choices=Candidate.Plan.choices)
    billing_cycle = models.CharField(max_length=24, choices=BillingCycle.choices, default=BillingCycle.MONTHLY)
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.TRIAL)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=80, blank=True)
    invoice_number = models.CharField(max_length=80, blank=True)
    receipt = models.FileField(upload_to="receipts/", blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.candidate} {self.get_plan_display()} subscription"


class SoftwareModule(TimeStampedModel):
    class Category(models.TextChoices):
        FOUNDATION = "FOUNDATION", "Foundation"
        FIELD = "FIELD", "Field Operations"
        CRM = "CRM", "Relationship CRM"
        MESSAGING = "MESSAGING", "Messaging"
        INTELLIGENCE = "INTELLIGENCE", "Intelligence"
        POLLING = "POLLING", "Polling-Day"
        AI = "AI", "AI Assistant"
        CONSTITUENCY = "CONSTITUENCY", "Constituency"
        PLATFORM = "PLATFORM", "Platform"

    code = models.SlugField(max_length=60, unique=True)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=24, choices=Category.choices)
    description = models.TextField(blank=True)
    is_core = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class ModulePrice(TimeStampedModel):
    module = models.ForeignKey(SoftwareModule, on_delete=models.CASCADE, related_name="prices")
    billing_cycle = models.CharField(max_length=24, choices=BillingCycle.choices)
    currency = models.CharField(max_length=3, default="PGK")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    setup_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("module", "billing_cycle", "currency")
        ordering = ["module__sort_order", "billing_cycle"]

    def __str__(self):
        return f"{self.module} {self.billing_cycle} {self.currency} {self.price}"


class ModuleBundle(TimeStampedModel):
    code = models.SlugField(max_length=60, unique=True)
    name = models.CharField(max_length=140)
    description = models.TextField(blank=True)
    modules = models.ManyToManyField(SoftwareModule, related_name="bundles", blank=True)
    billing_cycle = models.CharField(max_length=24, choices=BillingCycle.choices, default=BillingCycle.MONTHLY)
    currency = models.CharField(max_length=3, default="PGK")
    bundle_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_full_package = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ["sort_order", "name"]

    def standalone_total(self):
        total = 0
        for module in self.modules.all():
            price = module.prices.filter(billing_cycle=self.billing_cycle, currency=self.currency, is_active=True).first()
            if price:
                total += price.price
        return total

    def savings_amount(self):
        return max(self.standalone_total() - self.bundle_price, 0)

    def __str__(self):
        return self.name


class TenantModuleSubscription(TenantOwnedModel):
    class Source(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual Module"
        BUNDLE = "BUNDLE", "Bundle"
        FULL_PACKAGE = "FULL_PACKAGE", "Full Package"
        TRIAL = "TRIAL", "Trial"

    module = models.ForeignKey(SoftwareModule, on_delete=models.PROTECT, related_name="tenant_subscriptions")
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name="module_entitlements")
    bundle = models.ForeignKey(ModuleBundle, on_delete=models.SET_NULL, null=True, blank=True, related_name="tenant_entitlements")
    source = models.CharField(max_length=24, choices=Source.choices, default=Source.INDIVIDUAL)
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    price_locked = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("candidate", "module")
        ordering = ["candidate__name", "module__sort_order"]

    def __str__(self):
        return f"{self.candidate}: {self.module}"


class SubscriptionQuote(TimeStampedModel):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="subscription_quotes", db_column="tenant_id")
    billing_cycle = models.CharField(max_length=24, choices=BillingCycle.choices, default=BillingCycle.MONTHLY)
    currency = models.CharField(max_length=3, default="PGK")
    modules = models.ManyToManyField(SoftwareModule, blank=True)
    bundles = models.ManyToManyField(ModuleBundle, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def recalculate(self):
        module_ids = set()
        subtotal = 0
        bundle_total = 0
        for bundle in self.bundles.all():
            bundle_total += bundle.bundle_price
            module_ids.update(bundle.modules.values_list("id", flat=True))
        for module in self.modules.exclude(id__in=module_ids):
            price = module.prices.filter(billing_cycle=self.billing_cycle, currency=self.currency, is_active=True).first()
            if price:
                subtotal += price.price
        standalone_bundle_total = sum(bundle.standalone_total() for bundle in self.bundles.all())
        self.subtotal = subtotal + standalone_bundle_total
        self.discount_amount = max(standalone_bundle_total - bundle_total, 0)
        self.total = subtotal + bundle_total

    def __str__(self):
        return f"Quote for {self.candidate} ({self.total} {self.currency})"


class TenantSettings(TenantOwnedModel):
    sms_sender_name = models.CharField(max_length=40, blank=True)
    default_call_frequency_high = models.PositiveIntegerField(default=7)
    default_call_frequency_medium = models.PositiveIntegerField(default=14)
    default_call_frequency_low = models.PositiveIntegerField(default=30)
    export_requires_approval = models.BooleanField(default=True)
    ai_assistant_enabled = models.BooleanField(default=False)
    polling_day_mode = models.BooleanField(default=False)
    constituency_mode = models.BooleanField(default=False)
    data_retention_notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "candidate settings"

    def __str__(self):
        return f"Settings for {self.candidate}"


class ConnectorSetting(TenantOwnedModel):
    class ConnectorType(models.TextChoices):
        AI = "AI", "AI Provider"
        WHATSAPP = "WHATSAPP", "WhatsApp Business"
        SMS = "SMS", "SMS Gateway"
        EMAIL = "EMAIL", "Email"
        MAPS = "MAPS", "Maps / GIS"
        PAYMENT = "PAYMENT", "Payment Gateway"
        STORAGE = "STORAGE", "File Storage"
        WEBHOOK = "WEBHOOK", "Webhook"

    class Status(models.TextChoices):
        DISABLED = "DISABLED", "Disabled"
        CONFIGURED = "CONFIGURED", "Configured"
        NEEDS_TEST = "NEEDS_TEST", "Needs Test"
        ACTIVE = "ACTIVE", "Active"
        FAILED = "FAILED", "Failed"

    connector_type = models.CharField(max_length=24, choices=ConnectorType.choices)
    name = models.CharField(max_length=120)
    provider = models.CharField(max_length=80, blank=True)
    is_enabled = models.BooleanField(default=False)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.DISABLED)

    api_base_url = models.URLField(blank=True)
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    access_token = models.TextField(blank=True)
    webhook_url = models.URLField(blank=True)
    webhook_secret = models.CharField(max_length=255, blank=True)

    ai_model = models.CharField(max_length=80, blank=True)
    ai_temperature = models.DecimalField(max_digits=3, decimal_places=2, default=0.30)
    ai_system_policy = models.TextField(blank=True)

    whatsapp_phone_number_id = models.CharField(max_length=120, blank=True)
    whatsapp_business_account_id = models.CharField(max_length=120, blank=True)
    whatsapp_default_template = models.CharField(max_length=120, blank=True)

    sms_sender_id = models.CharField(max_length=40, blank=True)
    sms_default_country_code = models.CharField(max_length=8, default="+675")

    email_host = models.CharField(max_length=120, blank=True)
    email_port = models.PositiveIntegerField(null=True, blank=True)
    email_username = models.CharField(max_length=120, blank=True)
    email_password = models.CharField(max_length=255, blank=True)
    email_use_tls = models.BooleanField(default=True)
    email_from_address = models.EmailField(blank=True)

    payment_public_key = models.CharField(max_length=255, blank=True)
    payment_secret_key = models.CharField(max_length=255, blank=True)
    payment_merchant_id = models.CharField(max_length=120, blank=True)

    maps_api_key = models.CharField(max_length=255, blank=True)
    extra_config = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)
    last_tested_at = models.DateTimeField(null=True, blank=True)
    last_test_result = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("candidate", "connector_type", "name")
        ordering = ["connector_type", "name"]

    def has_credentials(self):
        return any([self.api_key, self.api_secret, self.access_token, self.email_password, self.payment_secret_key, self.maps_api_key])

    def masked_summary(self):
        return {
            "api_key": bool(self.api_key),
            "api_secret": bool(self.api_secret),
            "access_token": bool(self.access_token),
            "webhook_secret": bool(self.webhook_secret),
            "email_password": bool(self.email_password),
            "payment_secret_key": bool(self.payment_secret_key),
            "maps_api_key": bool(self.maps_api_key),
        }

    def __str__(self):
        return f"{self.candidate}: {self.name}"


class UsageService(models.TextChoices):
    AI = "AI", "AI"
    WHATSAPP = "WHATSAPP", "WhatsApp"
    SMS = "SMS", "SMS"
    EMAIL = "EMAIL", "Email"
    MAPS = "MAPS", "Maps"
    STORAGE = "STORAGE", "Storage"
    PAYMENT = "PAYMENT", "Payment"


class UsageUnit(models.TextChoices):
    TOKEN = "TOKEN", "Token"
    MESSAGE = "MESSAGE", "Message"
    CONVERSATION = "CONVERSATION", "Conversation"
    EMAIL = "EMAIL", "Email"
    REQUEST = "REQUEST", "Request"
    MEGABYTE = "MEGABYTE", "Megabyte"
    TRANSACTION = "TRANSACTION", "Transaction"


class UsageWallet(TenantOwnedModel):
    service = models.CharField(max_length=24, choices=UsageService.choices)
    currency = models.CharField(max_length=3, default="PGK")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    free_units_remaining = models.PositiveIntegerField(default=0)
    low_balance_threshold = models.DecimalField(max_digits=12, decimal_places=2, default=5)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("candidate", "service", "currency")
        ordering = ["candidate__name", "service"]

    def can_spend(self, amount):
        return self.is_active and self.balance >= amount

    def __str__(self):
        return f"{self.candidate} {self.get_service_display()} wallet"


class IncludedUsageQuota(TimeStampedModel):
    module = models.ForeignKey(SoftwareModule, on_delete=models.CASCADE, null=True, blank=True, related_name="included_usage_quotas")
    bundle = models.ForeignKey(ModuleBundle, on_delete=models.CASCADE, null=True, blank=True, related_name="included_usage_quotas")
    service = models.CharField(max_length=24, choices=UsageService.choices)
    unit = models.CharField(max_length=24, choices=UsageUnit.choices)
    quantity = models.PositiveIntegerField(default=0)
    billing_cycle = models.CharField(max_length=24, choices=BillingCycle.choices, default=BillingCycle.MONTHLY)
    description = models.CharField(max_length=220, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["service", "unit"]

    def clean(self):
        if not self.module_id and not self.bundle_id:
            raise ValidationError("Quota must belong to a module or bundle.")
        if self.module_id and self.bundle_id:
            raise ValidationError("Quota can belong to a module or bundle, not both.")

    def __str__(self):
        owner = self.module or self.bundle
        return f"{owner}: {self.quantity} {self.get_unit_display()} {self.get_service_display()}"


class TenantUsageQuota(TenantOwnedModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="tenant_usage_quotas")
    source_module = models.ForeignKey(SoftwareModule, on_delete=models.SET_NULL, null=True, blank=True)
    source_bundle = models.ForeignKey(ModuleBundle, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.CharField(max_length=24, choices=UsageService.choices)
    unit = models.CharField(max_length=24, choices=UsageUnit.choices)
    included_quantity = models.PositiveIntegerField(default=0)
    used_quantity = models.PositiveIntegerField(default=0)
    reset_period_start = models.DateField(default=timezone.localdate)
    reset_period_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["candidate__name", "service", "unit"]

    @property
    def remaining_quantity(self):
        return max(self.included_quantity - self.used_quantity, 0)

    def consume(self, quantity):
        applied = min(quantity, self.remaining_quantity)
        self.used_quantity += applied
        self.save(update_fields=["used_quantity", "updated_at"])
        return applied

    def __str__(self):
        return f"{self.candidate} {self.get_service_display()} quota"


class UsageTopUp(TenantOwnedModel):
    wallet = models.ForeignKey(UsageWallet, on_delete=models.CASCADE, related_name="topups")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="PGK")
    payment_reference = models.CharField(max_length=120, blank=True)
    payment_method = models.CharField(max_length=80, blank=True)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    received_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-received_at"]

    def apply(self):
        from decimal import Decimal

        self.wallet.balance = Decimal(self.wallet.balance) + Decimal(self.amount)
        self.wallet.save(update_fields=["balance", "updated_at"])

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.apply()

    def __str__(self):
        return f"{self.amount} {self.currency} top-up for {self.wallet}"


class UsageRateCard(TimeStampedModel):
    service = models.CharField(max_length=24, choices=UsageService.choices)
    provider = models.CharField(max_length=80, blank=True)
    model_name = models.CharField(max_length=120, blank=True)
    unit = models.CharField(max_length=24, choices=UsageUnit.choices)
    currency = models.CharField(max_length=3, default="PGK")
    provider_cost_per_unit = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    markup_percent = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    fixed_markup_per_unit = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    minimum_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    effective_from = models.DateField(default=timezone.localdate)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["service", "provider", "model_name", "unit"]

    def customer_price_per_unit(self):
        if self.is_free:
            return 0
        return self.provider_cost_per_unit + (self.provider_cost_per_unit * self.markup_percent / 100) + self.fixed_markup_per_unit

    def calculate_charge(self, quantity):
        if self.is_free:
            return 0
        charge = self.customer_price_per_unit() * quantity
        return max(charge, self.minimum_charge)

    def __str__(self):
        label = self.model_name or self.provider or self.get_service_display()
        return f"{label} {self.get_unit_display()} rate"


class FreeAIModel(TimeStampedModel):
    name = models.CharField(max_length=120)
    provider = models.CharField(max_length=80, blank=True)
    model_id = models.CharField(max_length=120, unique=True)
    context_window = models.PositiveIntegerField(null=True, blank=True)
    daily_free_requests = models.PositiveIntegerField(default=0)
    monthly_free_requests = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["provider", "name"]

    def __str__(self):
        return self.name


class PlanAIModel(TimeStampedModel):
    """Maps subscription plans to free AI models. Controls which model tenants use immediately upon activation."""

    plan = models.CharField(max_length=24, choices=Candidate.Plan.choices)
    ai_model = models.ForeignKey(FreeAIModel, on_delete=models.CASCADE, related_name="plan_assignments")
    is_default = models.BooleanField(
        default=True,
        help_text="Use this model as the default for AI features on this plan.",
    )

    class Meta:
        unique_together = [("plan", "ai_model")]
        ordering = ["plan", "ai_model__name"]

    def get_plan_label(self):
        return dict(Candidate.Plan.choices).get(self.plan, self.plan)

    def __str__(self):
        return f"{self.get_plan_label()} → {self.ai_model.name}"


class UsageEvent(TenantOwnedModel):
    class Status(models.TextChoices):
        ALLOWED = "ALLOWED", "Allowed"
        INCLUDED_QUOTA = "INCLUDED_QUOTA", "Included Quota"
        BLOCKED_NO_CREDIT = "BLOCKED_NO_CREDIT", "Blocked - No Credit"
        FREE = "FREE", "Free"
        REFUNDED = "REFUNDED", "Refunded"

    service = models.CharField(max_length=24, choices=UsageService.choices)
    connector = models.ForeignKey(ConnectorSetting, on_delete=models.SET_NULL, null=True, blank=True)
    wallet = models.ForeignKey(UsageWallet, on_delete=models.SET_NULL, null=True, blank=True, related_name="usage_events")
    quota = models.ForeignKey(TenantUsageQuota, on_delete=models.SET_NULL, null=True, blank=True, related_name="usage_events")
    rate_card = models.ForeignKey(UsageRateCard, on_delete=models.SET_NULL, null=True, blank=True)
    free_ai_model = models.ForeignKey(FreeAIModel, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=120)
    unit = models.CharField(max_length=24, choices=UsageUnit.choices)
    quantity = models.PositiveIntegerField(default=1)
    included_quantity_applied = models.PositiveIntegerField(default=0)
    billable_quantity = models.PositiveIntegerField(default=0)
    provider_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    markup_amount = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    customer_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_before = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.ALLOWED)
    reference = models.CharField(max_length=120, blank=True)
    metadata = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.candidate} {self.get_service_display()} {self.customer_charge}"


class SupportTicket(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, blank=True, related_name="support_tickets", db_column="tenant_id")
    title = models.CharField(max_length=180)
    description = models.TextField()
    requested_by = models.CharField(max_length=160, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_support_tickets")
    temporary_sensitive_access = models.BooleanField(default=False)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.OPEN)
    resolution_notes = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Role(models.TextChoices):
    CANDIDATE = "CANDIDATE", "Candidate"
    CAMPAIGN_MANAGER = "CAMPAIGN_MANAGER", "Campaign Manager"
    IT_ADMIN = "IT_ADMIN", "IT Administrator"
    DISTRICT_COORDINATOR = "DISTRICT_COORDINATOR", "District Coordinator"
    LLG_COORDINATOR = "LLG_COORDINATOR", "LLG Coordinator"
    WARD_COORDINATOR = "WARD_COORDINATOR", "Ward Coordinator"
    VILLAGE_COORDINATOR = "VILLAGE_COORDINATOR", "Village Coordinator"
    VOLUNTEER = "VOLUNTEER", "Volunteer"
    SCRUTINEER = "SCRUTINEER", "Polling-Day Scrutineer"


class Gender(models.TextChoices):
    FEMALE = "FEMALE", "Female"
    MALE = "MALE", "Male"
    OTHER = "OTHER", "Other"
    UNSPECIFIED = "UNSPECIFIED", "Unspecified"


class TeamMember(TenantOwnedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=160)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    role = models.CharField(max_length=32, choices=Role.choices)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    influence_level = models.CharField(max_length=20, blank=True)
    profile_photo = models.ImageField(upload_to="team_photos/", blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["role", "full_name"]

    def clean(self):
        if self.candidate_id:
            if self.role == Role.DISTRICT_COORDINATOR and self.candidate.candidate_type != CandidateType.PROVINCIAL:
                raise ValidationError({"role": "District Coordinators are only enabled for Provincial campaigns."})
            if self.province_id != self.candidate.province_id:
                raise ValidationError({"province": "Team member must be assigned inside the candidate province."})

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"


class SupportStatus(models.TextChoices):
    STRONG = "STRONG", "Strong Supporter"
    LEANING = "LEANING", "Leaning Supporter"
    UNDECIDED = "UNDECIDED", "Undecided"
    NOT_SUPPORTIVE = "NOT_SUPPORTIVE", "Not Supportive"
    UNKNOWN = "UNKNOWN", "Unknown"


class InfluenceLevel(models.TextChoices):
    HIGH = "HIGH", "High"
    MEDIUM = "MEDIUM", "Medium"
    LOW = "LOW", "Low"


class Supporter(TenantOwnedModel):
    full_name = models.CharField(max_length=160)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    age_range = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    clan = models.CharField(max_length=120, blank=True)
    church_group = models.CharField(max_length=120, blank=True)
    occupation = models.CharField(max_length=120, blank=True)
    enrollment_status = models.CharField(
        max_length=24,
        choices=[("VERIFIED_ENROLLED", "Verified Enrolled"), ("NEEDS_RE_ENROLMENT", "Needs Re-enrolment"), ("UNKNOWN", "Unknown")],
        default="UNKNOWN",
    )
    support_status = models.CharField(max_length=24, choices=SupportStatus.choices, default=SupportStatus.UNKNOWN)
    influence_level = models.CharField(max_length=20, choices=InfluenceLevel.choices, default=InfluenceLevel.LOW)
    introduced_by = models.CharField(max_length=160, blank=True)
    main_issue = models.CharField(max_length=220, blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    consent_to_messages = models.BooleanField(default=False)
    registered_by = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["full_name"]
        indexes = [models.Index(fields=["candidate", "phone", "ward", "village"])]

    def possible_duplicates(self):
        return Supporter.objects.filter(
            candidate=self.candidate,
            full_name__iexact=self.full_name,
            phone=self.phone,
            ward=self.ward,
            village=self.village,
        ).exclude(pk=self.pk)

    def __str__(self):
        return self.full_name


class WardProfile(TenantOwnedModel):
    ward = models.OneToOneField(Ward, on_delete=models.CASCADE, related_name="campaign_profile")
    councillor_name = models.CharField(max_length=160, blank=True)
    key_clans = models.TextField(blank=True)
    key_churches = models.TextField(blank=True)
    schools = models.TextField(blank=True)
    markets = models.TextField(blank=True)
    health_facilities = models.TextField(blank=True)
    important_landmarks = models.TextField(blank=True)
    access_routes = models.TextField(blank=True)
    meeting_places = models.TextField(blank=True)
    population_estimate = models.PositiveIntegerField(null=True, blank=True)
    estimated_voting_population = models.PositiveIntegerField(null=True, blank=True)
    previous_election_notes = models.TextField(blank=True)
    support_strength = models.CharField(max_length=20, choices=[("STRONG", "Strong"), ("MEDIUM", "Medium"), ("WEAK", "Weak"), ("UNKNOWN", "Unknown")], default="UNKNOWN")
    main_community_issues = models.TextField(blank=True)
    security_concerns = models.TextField(blank=True)
    youth_groups = models.TextField(blank=True)
    womens_groups = models.TextField(blank=True)
    church_groups = models.TextField(blank=True)
    business_groups = models.TextField(blank=True)
    important_families = models.TextField(blank=True)
    notes_for_candidate = models.TextField(blank=True)

    def __str__(self):
        return f"Ward brief: {self.ward}"

    def brief_summary(self):
        return {
            "ward": self.ward.name,
            "support_strength": self.get_support_strength_display(),
            "landmarks": self.important_landmarks,
            "leaders": self.councillor_name,
            "issues": self.main_community_issues,
            "sensitivities": self.security_concerns,
            "talking_points": self.notes_for_candidate,
        }


class Landmark(TenantOwnedModel):
    class LandmarkType(models.TextChoices):
        CHURCH = "CHURCH", "Church"
        SCHOOL = "SCHOOL", "School"
        MARKET = "MARKET", "Market"
        HEALTH_FACILITY = "HEALTH_FACILITY", "Health Facility"
        COMMUNITY_HALL = "COMMUNITY_HALL", "Community Hall"
        ROAD = "ROAD", "Road / Access Route"
        POLLING_LOCATION = "POLLING_LOCATION", "Polling Location"
        OTHER = "OTHER", "Other"

    name = models.CharField(max_length=180)
    landmark_type = models.CharField(max_length=32, choices=LandmarkType.choices, default=LandmarkType.OTHER)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    gps_coordinates = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Influencer(TenantOwnedModel):
    full_name = models.CharField(max_length=160)
    photo = models.ImageField(upload_to="influencer_photos/", blank=True)
    phone = models.CharField(max_length=40, blank=True)
    alternative_phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    community_role = models.CharField(max_length=160, blank=True)
    influence_category = models.CharField(max_length=80, blank=True)
    influence_level = models.CharField(max_length=20, choices=InfluenceLevel.choices, default=InfluenceLevel.MEDIUM)
    estimated_network_size = models.PositiveIntegerField(null=True, blank=True)
    relationship_status = models.CharField(max_length=20, choices=[("STRONG", "Strong"), ("MEDIUM", "Medium"), ("WEAK", "Weak"), ("UNKNOWN", "Unknown")], default="UNKNOWN")
    preferred_contact_method = models.CharField(max_length=20, choices=[("CALL", "Call"), ("SMS", "SMS"), ("WHATSAPP", "WhatsApp"), ("VISIT", "Visit")], default="CALL")
    contact_frequency_days = models.PositiveIntegerField(default=14)
    last_call_date = models.DateField(null=True, blank=True)
    last_meeting_date = models.DateField(null=True, blank=True)
    last_message_date = models.DateField(null=True, blank=True)
    next_contact_due_date = models.DateField(null=True, blank=True)
    assigned_owner = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    @property
    def influence_score(self):
        base = {"HIGH": 80, "MEDIUM": 55, "LOW": 30}.get(self.influence_level, 40)
        if self.estimated_network_size:
            base += min(self.estimated_network_size // 20, 20)
        if self.relationship_status == "STRONG":
            base += 10
        return min(base, 100)

    def save(self, *args, **kwargs):
        if not self.next_contact_due_date:
            anchor = self.last_call_date or timezone.localdate()
            self.next_contact_due_date = anchor + timedelta(days=self.contact_frequency_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class CallLog(TenantOwnedModel):
    caller = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls_made")
    called_team_member = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="calls_received")
    influencer = models.ForeignKey(Influencer, on_delete=models.SET_NULL, null=True, blank=True)
    supporter = models.ForeignKey(Supporter, on_delete=models.SET_NULL, null=True, blank=True)
    person_called = models.CharField(max_length=160)
    person_type = models.CharField(max_length=40, default="Influencer")
    phone_number = models.CharField(max_length=40, blank=True)
    call_datetime = models.DateTimeField(default=timezone.now)
    call_outcome = models.CharField(max_length=24, choices=[("ANSWERED", "Answered"), ("MISSED", "Missed"), ("CALL_BACK", "Call Back"), ("SWITCHED_OFF", "Switched Off"), ("WRONG_NUMBER", "Wrong Number")], default="ANSWERED")
    discussion_summary = models.TextField(blank=True)
    issues_raised = models.TextField(blank=True)
    commitments_made = models.TextField(blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    next_call_due_date = models.DateField(null=True, blank=True)
    call_duration = models.DurationField(null=True, blank=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.next_call_due_date:
            frequency = self.influencer.contact_frequency_days if self.influencer_id else 7
            self.next_call_due_date = self.call_datetime.date() + timedelta(days=frequency)
        super().save(*args, **kwargs)
        if self.influencer_id:
            self.influencer.last_call_date = self.call_datetime.date()
            self.influencer.next_contact_due_date = self.next_call_due_date
            self.influencer.save(update_fields=["last_call_date", "next_contact_due_date", "updated_at"])

    def __str__(self):
        return f"{self.person_called} on {self.call_datetime:%Y-%m-%d}"


class Message(TenantOwnedModel):
    class MessageType(models.TextChoices):
        STANDARD = "STANDARD", "Standard"
        POLLING_DAY_REMINDER = "POLLING_DAY_REMINDER", "Polling Day Reminder"
        PREFERENCE_INSTRUCTIONS = "PREFERENCE_INSTRUCTIONS", "Preference Instructions"
        CONSTITUENCY_NEWSLETTER = "CONSTITUENCY_NEWSLETTER", "Constituency Newsletter"

    sender = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    message_type = models.CharField(max_length=32, choices=MessageType.choices, default=MessageType.STANDARD)
    recipient_type = models.CharField(max_length=60, default="All Team")
    recipient_group = models.CharField(max_length=120, blank=True)
    subject = models.CharField(max_length=180)
    body = models.TextField()
    priority = models.CharField(max_length=20, choices=[("NORMAL", "Normal"), ("IMPORTANT", "Important"), ("URGENT", "Urgent")], default="NORMAL")
    delivery_channel = models.CharField(max_length=20, choices=[("IN_APP", "In-App"), ("SMS", "SMS"), ("EMAIL", "Email"), ("WHATSAPP", "WhatsApp")], default="IN_APP")
    scheduled_send_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("DRAFT", "Draft"), ("SCHEDULED", "Scheduled"), ("SENT", "Sent"), ("FAILED", "Failed")], default="DRAFT")
    read_receipt_required = models.BooleanField(default=False)
    acknowledgement_required = models.BooleanField(default=False)
    attachment = models.FileField(upload_to="message_attachments/", blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject


class MessageRecipient(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="recipients")
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, null=True, blank=True)
    supporter = models.ForeignKey(Supporter, on_delete=models.CASCADE, null=True, blank=True)
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE, null=True, blank=True)
    display_name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    failed = models.BooleanField(default=False)

    class Meta:
        ordering = ["message", "display_name"]

    def __str__(self):
        return self.display_name or str(self.team_member or self.supporter or self.influencer)


class CampaignTask(TenantOwnedModel):
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    assigned_by = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_tasks")
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=[("LOW", "Low"), ("NORMAL", "Normal"), ("HIGH", "High"), ("URGENT", "Urgent")], default="NORMAL")
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=[("PENDING", "Pending"), ("IN_PROGRESS", "In Progress"), ("COMPLETED", "Completed"), ("OVERDUE", "Overdue"), ("CANCELLED", "Cancelled")], default="PENDING")
    attachment = models.FileField(upload_to="task_attachments/", blank=True)
    completion_notes = models.TextField(blank=True)

    def __str__(self):
        return self.title


class CampaignEvent(TenantOwnedModel):
    class VenueType(models.TextChoices):
        MARKET_DAY = "MARKET_DAY", "Market Day"
        CHURCH_SERVICE = "CHURCH_SERVICE", "Church Service"
        ROADSIDE_RALLY = "ROADSIDE_RALLY", "Roadside Rally"
        VILLAGE_MEETING = "VILLAGE_MEETING", "Village Meeting"
        FEAST_MUMU = "FEAST_MUMU", "Feast / Mumu"
        FORMAL_HALL = "FORMAL_HALL", "Formal Hall / Building"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=180)
    event_type = models.CharField(max_length=40, choices=[("WARD_VISIT", "Ward Visit"), ("RALLY", "Rally"), ("MEETING", "Meeting"), ("FUNDRAISER", "Fundraiser"), ("AWARENESS", "Awareness"), ("POLLING_TRAINING", "Polling Training")])
    venue_type = models.CharField(max_length=24, choices=VenueType.choices, blank=True)
    ward_coverage = models.ManyToManyField(Ward, blank=True, related_name="coverage_events", help_text="Wards whose people typically attend this venue — used to auto-suggest speech notes.")
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    venue = models.CharField(max_length=180, blank=True)
    landmark = models.ForeignKey(Landmark, on_delete=models.SET_NULL, null=True, blank=True)
    host_person = models.CharField(max_length=160, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    expected_crowd_size = models.PositiveIntegerField(null=True, blank=True)
    actual_attendance = models.PositiveIntegerField(null=True, blank=True)
    talking_points = models.TextField(blank=True)
    issues_to_address = models.TextField(blank=True)
    people_to_acknowledge = models.TextField(blank=True)
    security_notes = models.TextField(blank=True)
    logistics_checklist = models.TextField(blank=True)
    photos = models.FileField(upload_to="event_photos/", blank=True)
    videos = models.FileField(upload_to="event_videos/", blank=True)
    event_report = models.TextField(blank=True)

    def __str__(self):
        return self.title


class EventChecklistItem(TenantOwnedModel):
    event = models.ForeignKey(CampaignEvent, on_delete=models.CASCADE, related_name="checklist_items")
    title = models.CharField(max_length=120)
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["event__start_datetime", "title"]

    def __str__(self):
        return f"{self.event}: {self.title}"


class EventAttendance(TenantOwnedModel):
    event = models.ForeignKey(CampaignEvent, on_delete=models.CASCADE, related_name="attendance_records")
    supporter = models.ForeignKey(Supporter, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40, blank=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True)
    checked_in_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} at {self.event}"


class CommunityIssue(TenantOwnedModel):
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=80)
    description = models.TextField()
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    reported_by = models.CharField(max_length=160, blank=True)
    priority = models.CharField(max_length=20, choices=[("LOW", "Low"), ("NORMAL", "Normal"), ("HIGH", "High"), ("URGENT", "Urgent")], default="NORMAL")
    status = models.CharField(max_length=24, choices=[("NEW", "New"), ("UNDER_REVIEW", "Under Review"), ("FOLLOW_UP", "Follow-Up"), ("RESOLVED", "Resolved"), ("DEFERRED", "Deferred")], default="NEW")
    related_event = models.ForeignKey(CampaignEvent, on_delete=models.SET_NULL, null=True, blank=True)
    related_influencer = models.ForeignKey(Influencer, on_delete=models.SET_NULL, null=True, blank=True)
    photos = models.FileField(upload_to="issue_photos/", blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title


class PromiseTracker(TenantOwnedModel):
    class Category(models.TextChoices):
        INFRASTRUCTURE = "INFRASTRUCTURE", "Infrastructure (Roads / Bridges)"
        EDUCATION = "EDUCATION", "Education"
        HEALTH = "HEALTH", "Health"
        WATER_SANITATION = "WATER_SANITATION", "Water & Sanitation"
        ECONOMIC = "ECONOMIC", "Economic / Livelihood"
        SERVICES = "SERVICES", "Government Services"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=180)
    description = models.TextField()
    category = models.CharField(max_length=24, choices=Category.choices, default=Category.OTHER)
    made_by = models.CharField(max_length=160, blank=True)
    made_to = models.CharField(max_length=160, blank=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    event = models.ForeignKey(CampaignEvent, on_delete=models.SET_NULL, null=True, blank=True)
    promise_date = models.DateField(default=timezone.localdate)
    target_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=[("OPEN", "Open"), ("IN_PROGRESS", "In Progress"), ("DELIVERED", "Delivered"), ("CANCELLED", "Cancelled"), ("DEFERRED", "Deferred")], default="OPEN")
    delivery_evidence = models.FileField(upload_to="promise_evidence/", blank=True)
    public_facing = models.BooleanField(default=False, help_text="Show on public constituency page once delivered.")
    follow_up_owner = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title


class PollingLocation(TenantOwnedModel):
    class SecurityRisk(models.TextChoices):
        LOW = "LOW", "Low"
        MODERATE = "MODERATE", "Moderate"
        HIGH = "HIGH", "High"
        REFUSED = "REFUSED", "Refused — Do Not Enter"

    name = models.CharField(max_length=180)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    gps_coordinates = models.CharField(max_length=80, blank=True)
    assigned_scrutineer = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="polling_locations")
    backup_scrutineer = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="backup_polling_locations")
    contact_number = models.CharField(max_length=40, blank=True)
    status = models.CharField(max_length=40, default="Pending")
    scrutineer_checked_in = models.BooleanField(default=False)
    transport_status = models.CharField(max_length=80, blank=True)
    last_status_update = models.DateTimeField(null=True, blank=True)
    past_vote_data = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder, help_text='Previous election tallies. Format: {"2022": {"our_candidate": 340, "opponent_a": 120}}')
    security_risk = models.CharField(max_length=16, choices=SecurityRisk.choices, default=SecurityRisk.LOW)
    expected_turnout = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PollingIncident(TenantOwnedModel):
    polling_location = models.ForeignKey(PollingLocation, on_delete=models.CASCADE, related_name="incidents")
    reported_by = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=180)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=[("NORMAL", "Normal"), ("HIGH", "High"), ("URGENT", "Urgent")], default="NORMAL")
    status = models.CharField(max_length=24, choices=[("OPEN", "Open"), ("IN_PROGRESS", "In Progress"), ("RESOLVED", "Resolved")], default="OPEN")

    def __str__(self):
        return self.title


class Notification(TenantOwnedModel):
    class Channel(models.TextChoices):
        IN_APP = "IN_APP", "In-App"
        SMS = "SMS", "SMS"
        EMAIL = "EMAIL", "Email"
        WHATSAPP = "WHATSAPP", "WhatsApp Future"

    recipient = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=180)
    body = models.TextField()
    channel = models.CharField(max_length=24, choices=Channel.choices, default=Channel.IN_APP)
    related_object_type = models.CharField(max_length=80, blank=True)
    related_object_id = models.CharField(max_length=80, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ReminderEscalation(TenantOwnedModel):
    title = models.CharField(max_length=180)
    owner = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="owned_escalations")
    escalated_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="received_escalations")
    reason = models.CharField(max_length=220)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=[("OPEN", "Open"), ("ACKNOWLEDGED", "Acknowledged"), ("RESOLVED", "Resolved")], default="OPEN")
    resolved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["status", "due_date"]

    def __str__(self):
        return self.title


class PollingStatus(TenantOwnedModel):
    polling_location = models.ForeignKey(PollingLocation, on_delete=models.CASCADE, related_name="status_updates")
    reported_by = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    status_time = models.DateTimeField(default=timezone.now)
    scrutineer_present = models.BooleanField(default=False)
    booth_open = models.BooleanField(default=False)
    materials_available = models.BooleanField(default=True)
    communication_ok = models.BooleanField(default=True)
    our_tally = models.PositiveIntegerField(null=True, blank=True, help_text="Votes for our candidate observed at this booth so far.")
    transport_notes = models.TextField(blank=True)
    logistical_issues = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-status_time"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.polling_location.scrutineer_checked_in = self.scrutineer_present
        self.polling_location.last_status_update = self.status_time
        self.polling_location.save(update_fields=["scrutineer_checked_in", "last_status_update", "updated_at"])

    def __str__(self):
        return f"{self.polling_location} status {self.status_time:%Y-%m-%d %H:%M}"


class AIWorkItem(TenantOwnedModel):
    class WorkType(models.TextChoices):
        WARD_BRIEF = "WARD_BRIEF", "Ward Brief"
        SPEECH_NOTES = "SPEECH_NOTES", "Speech Notes"
        DAILY_SUMMARY = "DAILY_SUMMARY", "Daily Campaign Summary"
        CALL_SUGGESTIONS = "CALL_SUGGESTIONS", "Suggested Calls"
        ISSUE_TRENDS = "ISSUE_TRENDS", "Issue Trend Analysis"
        MESSAGE_DRAFT = "MESSAGE_DRAFT", "Message Draft"
        EVENT_REPORT = "EVENT_REPORT", "Event Report Summary"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        READY_FOR_REVIEW = "READY_FOR_REVIEW", "Ready for Human Review"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    work_type = models.CharField(max_length=32, choices=WorkType.choices)
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(CampaignEvent, on_delete=models.SET_NULL, null=True, blank=True)
    ai_model = models.CharField(max_length=120, blank=True)
    used_free_model = models.BooleanField(default=False)
    prompt = models.TextField(blank=True)
    source_snapshot = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)
    output = models.TextField(blank=True)
    safety_notes = models.TextField(blank=True)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.DRAFT)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_ai_items")
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_work_type_display()} for {self.candidate}"


class ImportBatch(TenantOwnedModel):
    class ImportType(models.TextChoices):
        SUPPORTERS = "SUPPORTERS", "Supporters CSV"
        TEAM_MEMBERS = "TEAM_MEMBERS", "Team Members CSV"
        INFLUENCERS = "INFLUENCERS", "Influencers CSV"
        WARD_DATA = "WARD_DATA", "Ward Data CSV"
        POLLING_LOCATIONS = "POLLING_LOCATIONS", "Polling Locations CSV"
        GEOGRAPHY = "GEOGRAPHY", "Geography CSV"

    import_type = models.CharField(max_length=32, choices=ImportType.choices)
    uploaded_file = models.FileField(upload_to="imports/")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="campaign_imports")
    status = models.CharField(max_length=24, choices=[("PENDING", "Pending"), ("VALIDATED", "Validated"), ("IMPORTED", "Imported"), ("FAILED", "Failed")], default="PENDING")
    total_rows = models.PositiveIntegerField(default=0)
    valid_rows = models.PositiveIntegerField(default=0)
    error_rows = models.PositiveIntegerField(default=0)
    validation_errors = models.JSONField(default=list, blank=True, encoder=DjangoJSONEncoder)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_import_type_display()} import for {self.candidate}"


class ExportRequest(TenantOwnedModel):
    class ExportType(models.TextChoices):
        SUPPORTERS = "SUPPORTERS", "Supporter Report"
        CALLS = "CALLS", "Call Report"
        WARDS = "WARDS", "Ward Report"
        EVENTS = "EVENTS", "Event Report"
        MESSAGES = "MESSAGES", "Messaging Report"
        POLLING = "POLLING", "Polling Readiness Report"
        COORDINATORS = "COORDINATORS", "Coordinator Performance Report"

    export_type = models.CharField(max_length=32, choices=ExportType.choices)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="campaign_exports")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_campaign_exports")
    status = models.CharField(max_length=24, choices=[("REQUESTED", "Requested"), ("APPROVED", "Approved"), ("REJECTED", "Rejected"), ("READY", "Ready")], default="REQUESTED")
    filters = models.JSONField(default=dict, blank=True, encoder=DjangoJSONEncoder)
    output_file = models.FileField(upload_to="exports/", blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_export_type_display()} export for {self.candidate}"


class CitizenRequest(TenantOwnedModel):
    title = models.CharField(max_length=180)
    requester_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40, blank=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    category = models.CharField(max_length=80, blank=True)
    description = models.TextField()
    status = models.CharField(max_length=24, choices=[("NEW", "New"), ("UNDER_REVIEW", "Under Review"), ("REFERRED", "Referred"), ("RESOLVED", "Resolved"), ("DECLINED", "Declined")], default="NEW")
    assigned_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    def __str__(self):
        return self.title


class DevelopmentProject(TenantOwnedModel):
    name = models.CharField(max_length=180)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=24, choices=[("PLANNED", "Planned"), ("IN_PROGRESS", "In Progress"), ("COMPLETED", "Completed"), ("ON_HOLD", "On Hold")], default="PLANNED")
    start_date = models.DateField(null=True, blank=True)
    target_completion_date = models.DateField(null=True, blank=True)
    public_notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CommunityGrant(TenantOwnedModel):
    recipient = models.CharField(max_length=180)
    purpose = models.CharField(max_length=220)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    llg = models.ForeignKey(LLG, on_delete=models.PROTECT, null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=24, choices=[("REQUESTED", "Requested"), ("APPROVED", "Approved"), ("PAID", "Paid"), ("DECLINED", "Declined")], default="REQUESTED")
    request_date = models.DateField(default=timezone.localdate)
    decision_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.recipient


class WardDevelopmentPlan(TenantOwnedModel):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="development_plans")
    priorities = models.TextField()
    projects = models.ManyToManyField(DevelopmentProject, blank=True)
    community_feedback = models.TextField(blank=True)
    next_visit_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=24, choices=[("DRAFT", "Draft"), ("ACTIVE", "Active"), ("ARCHIVED", "Archived")], default="DRAFT")

    def __str__(self):
        return f"Development plan for {self.ward}"


# ── PNG-specific campaign models ──────────────────────────────────────────────

class PreferenceDeal(TenantOwnedModel):
    """LPV preference deal — agreements to direct 2nd/3rd votes to partner candidates."""

    class Status(models.TextChoices):
        VERBAL = "VERBAL", "Verbal — Not Yet Confirmed"
        AGREED = "AGREED", "Agreed"
        BROKEN = "BROKEN", "Fallen Through"
        INACTIVE = "INACTIVE", "Inactive"

    partner_candidate_name = models.CharField(max_length=160)
    partner_party = models.CharField(max_length=120, blank=True)
    partner_seat = models.CharField(max_length=160, blank=True, help_text="e.g. Goroka Open, Eastern Highlands Provincial")
    preference_number = models.PositiveSmallIntegerField(default=2, help_text="Which preference number to direct (2 or 3).")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.VERBAL)
    contact_person = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="preference_deal_contacts")
    ward_directives = models.TextField(blank=True, help_text="Which wards should push this deal and any specific instructions.")
    deal_terms = models.TextField(blank=True, help_text="Internal: terms agreed. Not shared externally.")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.preference_number} deal with {self.partner_candidate_name}"


class CommunityGroup(TenantOwnedModel):
    """Clan, church, women's group, or other voting bloc within a ward."""

    class GroupType(models.TextChoices):
        CLAN = "CLAN", "Clan / Family Group"
        CHURCH = "CHURCH", "Church"
        WOMENS_GROUP = "WOMENS_GROUP", "Women's Group"
        YOUTH_GROUP = "YOUTH_GROUP", "Youth Group"
        SPORTS_CLUB = "SPORTS_CLUB", "Sports Club"
        BUSINESS = "BUSINESS", "Business Association"
        POLITICAL = "POLITICAL", "Political Group"
        OTHER = "OTHER", "Other"

    class Alignment(models.TextChoices):
        STRONG_SUPPORTER = "STRONG_SUPPORTER", "Strong Supporter"
        LEANING_SUPPORT = "LEANING_SUPPORT", "Leaning — Support"
        NEUTRAL = "NEUTRAL", "Neutral"
        LEANING_AWAY = "LEANING_AWAY", "Leaning — Against"
        UNKNOWN = "UNKNOWN", "Unknown"

    name = models.CharField(max_length=160)
    group_type = models.CharField(max_length=20, choices=GroupType.choices, default=GroupType.OTHER)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name="community_groups")
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    estimated_voting_members = models.PositiveIntegerField(null=True, blank=True)
    alignment = models.CharField(max_length=20, choices=Alignment.choices, default=Alignment.UNKNOWN)
    key_contact = models.ForeignKey(Influencer, on_delete=models.SET_NULL, null=True, blank=True, related_name="community_groups")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["ward__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_group_type_display()}, {self.ward})"


class CommunityAssistance(TenantOwnedModel):
    """Tracks community assistance provided during campaign. Keeps candidate legally protected."""

    class AssistanceType(models.TextChoices):
        FOOD_FEAST = "FOOD_FEAST", "Food / Feast / Mumu"
        SCHOOL_MATERIALS = "SCHOOL_MATERIALS", "School Materials"
        TOOLS_EQUIPMENT = "TOOLS_EQUIPMENT", "Tools & Equipment"
        MEDICAL_SUPPLIES = "MEDICAL_SUPPLIES", "Medical Supplies"
        TRANSPORT = "TRANSPORT", "Transport Assistance"
        INFRASTRUCTURE = "INFRASTRUCTURE", "Minor Infrastructure"
        CASH_CONTRIBUTION = "CASH_CONTRIBUTION", "Cash Contribution (Record Only)"
        OTHER = "OTHER", "Other"

    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name="community_assistances")
    village = models.ForeignKey(Village, on_delete=models.PROTECT, null=True, blank=True)
    date = models.DateField(default=timezone.localdate)
    recipient_group = models.CharField(max_length=180, help_text="e.g. Kondiu Youth Group, St Joseph's Church")
    assistance_type = models.CharField(max_length=24, choices=AssistanceType.choices, default=AssistanceType.OTHER)
    description = models.TextField()
    estimated_value_pgk = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    approved_by = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_assistances")
    related_event = models.ForeignKey(CampaignEvent, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.get_assistance_type_display()} — {self.ward} ({self.date})"


class CompetitorActivity(TenantOwnedModel):
    """Tracks opponent movements and promises. Feeds into ward briefings."""

    class ActivityType(models.TextChoices):
        WARD_VISIT = "WARD_VISIT", "Ward Visit"
        PROMISE_MADE = "PROMISE_MADE", "Promise Made"
        RALLY = "RALLY", "Rally / Event"
        MEDIA = "MEDIA", "Media / Radio Appearance"
        PREFERENCE_DEAL = "PREFERENCE_DEAL", "Preference Deal Announced"
        DISTRIBUTION = "DISTRIBUTION", "Distribution / Handout"
        OTHER = "OTHER", "Other"

    class Source(models.TextChoices):
        CONFIRMED = "CONFIRMED", "Confirmed"
        SOCIAL_MEDIA = "SOCIAL_MEDIA", "Social Media"
        MEDIA_REPORT = "MEDIA_REPORT", "Media Report"
        RUMOUR = "RUMOUR", "Rumour / Unverified"

    opponent_name = models.CharField(max_length=160)
    opponent_party = models.CharField(max_length=120, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True, related_name="competitor_activities")
    date = models.DateField(default=timezone.localdate)
    activity_type = models.CharField(max_length=20, choices=ActivityType.choices, default=ActivityType.OTHER)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.RUMOUR)
    description = models.TextField()
    response_action = models.TextField(blank=True)
    response_assigned_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="competitor_responses")

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.opponent_name} — {self.get_activity_type_display()} ({self.date})"


class DevelopmentFund(TenantOwnedModel):
    """Tracks DSIP / SDP / grant funds allocated to wards. Post-election constituency use."""

    class FundType(models.TextChoices):
        DSIP = "DSIP", "DSIP — District Services Improvement Program"
        SDP = "SDP", "SDP — Special Development Program (Provincial)"
        COMMUNITY_MINE = "COMMUNITY_MINE", "Community Mine Continuation Agreement"
        GRANT = "GRANT", "External Grant"
        OTHER = "OTHER", "Other"

    fund_name = models.CharField(max_length=180)
    fund_type = models.CharField(max_length=20, choices=FundType.choices, default=FundType.DSIP)
    financial_year = models.CharField(max_length=10, help_text="e.g. 2025 or 2025/26")
    total_allocation_pgk = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    spent_pgk = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, null=True, blank=True, related_name="development_funds")
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-financial_year", "fund_name"]

    @property
    def remaining_pgk(self):
        return self.total_allocation_pgk - self.spent_pgk

    def __str__(self):
        return f"{self.fund_name} {self.financial_year}"


class RegistrationDrive(TenantOwnedModel):
    """Voter registration drive — tracks ward-level enrolment efforts."""

    class Status(models.TextChoices):
        PLANNED = "PLANNED", "Planned"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    title = models.CharField(max_length=180)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name="registration_drives")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    team_members = models.ManyToManyField(TeamMember, blank=True, related_name="registration_drives")
    target_count = models.PositiveIntegerField(default=0, help_text="Target number of people to help enrol.")
    actual_count = models.PositiveIntegerField(default=0, help_text="Actual number helped to enrol.")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PLANNED)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, blank=True, db_column="tenant_id")
    action = models.CharField(max_length=80)
    object_type = models.CharField(max_length=80, blank=True)
    object_id = models.CharField(max_length=80, blank=True)
    old_value = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    new_value = models.JSONField(null=True, blank=True, encoder=DjangoJSONEncoder)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device = models.CharField(max_length=220, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.action} at {self.timestamp:%Y-%m-%d %H:%M}"


class AccessLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, blank=True, db_column="tenant_id")
    path = models.CharField(max_length=260)
    method = models.CharField(max_length=12)
    status_code = models.PositiveIntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=260, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.method} {self.path}"


class DataLifecycleRequest(TenantOwnedModel):
    class RequestType(models.TextChoices):
        CORRECTION = "CORRECTION", "Personal Data Correction"
        EXPORT = "EXPORT", "Tenant Data Export"
        ARCHIVAL = "ARCHIVAL", "Tenant Archival"
        DELETION = "DELETION", "Tenant Data Deletion"

    request_type = models.CharField(max_length=24, choices=RequestType.choices)
    requested_by = models.CharField(max_length=160)
    reason = models.TextField()
    status = models.CharField(max_length=24, choices=[("REQUESTED", "Requested"), ("APPROVED", "Approved"), ("COMPLETED", "Completed"), ("REJECTED", "Rejected")], default="REQUESTED")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    completion_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_request_type_display()} for {self.candidate}"
