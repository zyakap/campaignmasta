from django.contrib import admin

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
    Influencer,
    ImportBatch,
    IncludedUsageQuota,
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
    Subscription,
    SubscriptionQuote,
    Supporter,
    SupportTicket,
    SoftwareModule,
    TeamMember,
    TenantSettings,
    TenantModuleSubscription,
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


class TenantAdminMixin:
    list_filter = ("candidate",)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_filter = ("province",)
    search_fields = ("name", "province__name")


@admin.register(LLG)
class LLGAdmin(admin.ModelAdmin):
    list_filter = ("district__province", "district")
    search_fields = ("name", "district__name")


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_filter = ("llg__district__province", "llg__district", "llg")
    search_fields = ("name", "number", "llg__name")


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_filter = ("ward__llg__district__province", "ward__llg", "ward")
    search_fields = ("name", "ward__name")


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("name", "candidate_type", "province", "district", "subscription_plan", "status")
    list_filter = ("candidate_type", "subscription_plan", "status", "province")
    search_fields = ("name",)


@admin.register(CandidateProfile)
class CandidateProfileAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("full_name", "candidate", "party", "phone", "email")
    search_fields = ("full_name", "party", "phone", "email")


@admin.register(Subscription)
class SubscriptionAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("candidate", "plan", "billing_cycle", "status", "amount", "start_date", "end_date")
    list_filter = ("candidate", "plan", "billing_cycle", "status")
    search_fields = ("candidate__name", "invoice_number")


class ModulePriceInline(admin.TabularInline):
    model = ModulePrice
    extra = 0


class IncludedUsageQuotaInline(admin.TabularInline):
    model = IncludedUsageQuota
    fk_name = "module"
    extra = 0


@admin.register(SoftwareModule)
class SoftwareModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category", "is_core", "is_active", "sort_order")
    list_filter = ("category", "is_core", "is_active")
    search_fields = ("name", "code", "description")
    inlines = [ModulePriceInline, IncludedUsageQuotaInline]


class BundleIncludedUsageQuotaInline(admin.TabularInline):
    model = IncludedUsageQuota
    fk_name = "bundle"
    extra = 0


@admin.register(ModuleBundle)
class ModuleBundleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "billing_cycle", "currency", "bundle_price", "discount_percent", "is_full_package", "is_active")
    list_filter = ("billing_cycle", "currency", "is_full_package", "is_active")
    search_fields = ("name", "code", "description")
    filter_horizontal = ("modules",)
    inlines = [BundleIncludedUsageQuotaInline]


@admin.register(TenantModuleSubscription)
class TenantModuleSubscriptionAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("candidate", "module", "source", "bundle", "is_enabled", "start_date", "end_date", "price_locked")
    list_filter = ("candidate", "module__category", "source", "is_enabled")
    search_fields = ("candidate__name", "module__name", "module__code", "notes")


@admin.register(SubscriptionQuote)
class SubscriptionQuoteAdmin(admin.ModelAdmin):
    list_display = ("candidate", "billing_cycle", "currency", "subtotal", "discount_amount", "total", "accepted_at", "created_at")
    list_filter = ("billing_cycle", "currency", "accepted_at")
    search_fields = ("candidate__name", "notes")
    filter_horizontal = ("modules", "bundles")


@admin.register(TenantSettings)
class TenantSettingsAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("candidate", "ai_assistant_enabled", "polling_day_mode", "constituency_mode", "export_requires_approval")
    list_filter = ("candidate", "ai_assistant_enabled", "polling_day_mode", "constituency_mode")


@admin.register(ConnectorSetting)
class ConnectorSettingAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "candidate", "connector_type", "provider", "is_enabled", "status", "last_tested_at")
    list_filter = ("candidate", "connector_type", "provider", "is_enabled", "status")
    search_fields = ("name", "provider", "api_base_url", "webhook_url", "notes")
    readonly_fields = ("last_tested_at", "last_test_result")


@admin.register(UsageWallet)
class UsageWalletAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("candidate", "service", "currency", "balance", "free_units_remaining", "low_balance_threshold", "is_active")
    list_filter = ("candidate", "service", "currency", "is_active")
    search_fields = ("candidate__name", "notes")


@admin.register(IncludedUsageQuota)
class IncludedUsageQuotaAdmin(admin.ModelAdmin):
    list_display = ("module", "bundle", "service", "unit", "quantity", "billing_cycle", "is_active")
    list_filter = ("service", "unit", "billing_cycle", "is_active")
    search_fields = ("module__name", "bundle__name", "description")


@admin.register(TenantUsageQuota)
class TenantUsageQuotaAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("candidate", "subscription", "service", "unit", "included_quantity", "used_quantity", "remaining_quantity", "reset_period_end", "is_active")
    list_filter = ("candidate", "service", "unit", "is_active")
    search_fields = ("candidate__name", "notes")


@admin.register(UsageTopUp)
class UsageTopUpAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("candidate", "wallet", "amount", "currency", "payment_method", "payment_reference", "received_at", "received_by")
    list_filter = ("candidate", "wallet__service", "currency", "payment_method")
    search_fields = ("candidate__name", "payment_reference", "notes")


@admin.register(UsageRateCard)
class UsageRateCardAdmin(admin.ModelAdmin):
    list_display = ("service", "provider", "model_name", "unit", "currency", "provider_cost_per_unit", "markup_percent", "fixed_markup_per_unit", "minimum_charge", "is_free", "is_active")
    list_filter = ("service", "provider", "unit", "currency", "is_free", "is_active")
    search_fields = ("provider", "model_name", "notes")


@admin.register(FreeAIModel)
class FreeAIModelAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "model_id", "daily_free_requests", "monthly_free_requests", "is_active")
    list_filter = ("provider", "is_active")
    search_fields = ("name", "provider", "model_id", "notes")


@admin.register(UsageEvent)
class UsageEventAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("candidate", "service", "action", "quantity", "included_quantity_applied", "billable_quantity", "unit", "customer_charge", "balance_before", "balance_after", "status", "created_at")
    list_filter = ("candidate", "service", "unit", "status")
    search_fields = ("candidate__name", "action", "reference")
    readonly_fields = ("created_at", "updated_at")


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("title", "candidate", "status", "temporary_sensitive_access", "assigned_to", "created_at")
    list_filter = ("status", "temporary_sensitive_access", "candidate")
    search_fields = ("title", "description", "requested_by")


@admin.register(TeamMember)
class TeamMemberAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("full_name", "candidate", "role", "phone", "province", "district", "llg", "ward", "is_active")
    list_filter = ("candidate", "role", "is_active", "province", "district", "llg")
    search_fields = ("full_name", "phone", "email")


@admin.register(Supporter)
class SupporterAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("full_name", "candidate", "phone", "support_status", "influence_level", "ward", "village", "consent_to_messages")
    list_filter = ("candidate", "support_status", "influence_level", "consent_to_messages", "province", "district", "llg", "ward")
    search_fields = ("full_name", "phone", "village__name", "clan")


@admin.register(WardProfile)
class WardProfileAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("ward", "candidate", "support_strength", "population_estimate", "estimated_voting_population")
    list_filter = ("candidate", "support_strength", "ward__llg")
    search_fields = ("ward__name", "councillor_name", "main_community_issues")


@admin.register(Landmark)
class LandmarkAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "candidate", "landmark_type", "province", "district", "llg", "ward", "village")
    list_filter = ("candidate", "landmark_type", "province", "district", "llg", "ward")
    search_fields = ("name", "notes", "gps_coordinates")


@admin.register(Influencer)
class InfluencerAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("full_name", "candidate", "community_role", "influence_level", "relationship_status", "next_contact_due_date", "assigned_owner")
    list_filter = ("candidate", "influence_level", "relationship_status", "province", "district", "llg", "ward")
    search_fields = ("full_name", "phone", "community_role")


@admin.register(CallLog)
class CallLogAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("person_called", "candidate", "caller", "call_outcome", "call_datetime", "next_call_due_date")
    list_filter = ("candidate", "call_outcome", "person_type")
    search_fields = ("person_called", "phone_number", "discussion_summary")


class MessageRecipientInline(admin.TabularInline):
    model = MessageRecipient
    extra = 0


@admin.register(Message)
class MessageAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("subject", "candidate", "sender", "recipient_type", "priority", "delivery_channel", "status", "created_at")
    list_filter = ("candidate", "priority", "delivery_channel", "status")
    search_fields = ("subject", "body", "recipient_group")
    inlines = [MessageRecipientInline]


@admin.register(CampaignTask)
class CampaignTaskAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "assigned_to", "priority", "due_date", "status")
    list_filter = ("candidate", "priority", "status", "province", "district", "llg", "ward")
    search_fields = ("title", "description")


@admin.register(CampaignEvent)
class CampaignEventAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "event_type", "ward", "venue", "start_datetime", "expected_crowd_size", "actual_attendance")
    list_filter = ("candidate", "event_type", "province", "district", "llg", "ward")
    search_fields = ("title", "venue", "host_person", "talking_points")


@admin.register(EventChecklistItem)
class EventChecklistItemAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "event", "assigned_to", "is_complete")
    list_filter = ("candidate", "is_complete", "event")
    search_fields = ("title", "notes", "event__title")


@admin.register(EventAttendance)
class EventAttendanceAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("full_name", "candidate", "event", "phone", "village", "checked_in_at")
    list_filter = ("candidate", "event", "village")
    search_fields = ("full_name", "phone", "event__title")


@admin.register(CommunityIssue)
class CommunityIssueAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "category", "priority", "status", "ward", "created_at")
    list_filter = ("candidate", "category", "priority", "status", "province", "district", "llg", "ward")
    search_fields = ("title", "description", "reported_by")


@admin.register(PromiseTracker)
class PromiseTrackerAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "made_to", "promise_date", "target_date", "status", "follow_up_owner")
    list_filter = ("candidate", "status", "province", "district", "llg", "ward")
    search_fields = ("title", "description", "made_to")


@admin.register(PollingLocation)
class PollingLocationAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "candidate", "ward", "assigned_scrutineer", "backup_scrutineer", "status")
    list_filter = ("candidate", "status", "province", "district", "llg", "ward")
    search_fields = ("name", "village__name", "contact_number")


@admin.register(PollingIncident)
class PollingIncidentAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "polling_location", "priority", "status", "created_at")
    list_filter = ("candidate", "priority", "status")
    search_fields = ("title", "description")


@admin.register(PollingStatus)
class PollingStatusAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("polling_location", "candidate", "reported_by", "scrutineer_present", "booth_open", "communication_ok", "status_time")
    list_filter = ("candidate", "scrutineer_present", "booth_open", "communication_ok")
    search_fields = ("polling_location__name", "transport_notes", "logistical_issues")


@admin.register(AIWorkItem)
class AIWorkItemAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("work_type", "candidate", "ward", "event", "status", "reviewed_by", "created_at")
    list_filter = ("candidate", "work_type", "status")
    search_fields = ("prompt", "output", "safety_notes")


@admin.register(ImportBatch)
class ImportBatchAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("import_type", "candidate", "status", "total_rows", "valid_rows", "error_rows", "created_at")
    list_filter = ("candidate", "import_type", "status")


@admin.register(ExportRequest)
class ExportRequestAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("export_type", "candidate", "requested_by", "approved_by", "status", "created_at")
    list_filter = ("candidate", "export_type", "status")


@admin.register(CitizenRequest)
class CitizenRequestAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "requester_name", "category", "status", "assigned_to", "due_date")
    list_filter = ("candidate", "category", "status", "province", "district", "llg", "ward")
    search_fields = ("title", "requester_name", "phone", "description")


@admin.register(DevelopmentProject)
class DevelopmentProjectAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "candidate", "status", "budget", "ward", "target_completion_date")
    list_filter = ("candidate", "status", "province", "district", "llg", "ward")
    search_fields = ("name", "description", "public_notes")


@admin.register(CommunityGrant)
class CommunityGrantAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("recipient", "candidate", "purpose", "amount", "status", "request_date")
    list_filter = ("candidate", "status", "province", "district", "llg", "ward")
    search_fields = ("recipient", "purpose", "notes")


@admin.register(WardDevelopmentPlan)
class WardDevelopmentPlanAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("ward", "candidate", "status", "next_visit_date")
    list_filter = ("candidate", "status", "ward__llg")
    search_fields = ("ward__name", "priorities", "community_feedback")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "candidate", "user", "object_type", "object_id", "timestamp")
    list_filter = ("candidate", "action", "object_type")
    search_fields = ("action", "object_type", "object_id", "device")
    readonly_fields = ("timestamp",)


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ("user", "candidate", "method", "path", "status_code", "ip_address", "created_at")
    list_filter = ("candidate", "method", "status_code")
    search_fields = ("path", "user_agent", "ip_address")
    readonly_fields = ("created_at",)


@admin.register(Notification)
class NotificationAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "recipient", "channel", "delivered_at", "read_at", "created_at")
    list_filter = ("candidate", "channel", "delivered_at", "read_at")
    search_fields = ("title", "body", "recipient__full_name")


@admin.register(ReminderEscalation)
class ReminderEscalationAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("title", "candidate", "owner", "escalated_to", "status", "due_date")
    list_filter = ("candidate", "status", "due_date")
    search_fields = ("title", "reason", "notes")


@admin.register(DataLifecycleRequest)
class DataLifecycleRequestAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("request_type", "candidate", "requested_by", "status", "reviewed_by", "reviewed_at")
    list_filter = ("candidate", "request_type", "status")
    search_fields = ("requested_by", "reason", "completion_notes")
