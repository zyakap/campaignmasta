from django import forms

from .models import (
    AIWorkItem,
    CallLog,
    CampaignEvent,
    CampaignTask,
    CitizenRequest,
    CommunityIssue,
    ConnectorSetting,
    ExportRequest,
    FreeAIModel,
    Influencer,
    ImportBatch,
    IncludedUsageQuota,
    PlanAIModel,
    Message,
    ModuleBundle,
    PollingIncident,
    PollingLocation,
    CommunityAssistance,
    CommunityGroup,
    CompetitorActivity,
    DevelopmentFund,
    PollingStatus,
    PreferenceDeal,
    PromiseTracker,
    RegistrationDrive,
    SoftwareModule,
    SubscriptionQuote,
    Supporter,
    TeamMember,
    TenantSettings,
    UsageRateCard,
    UsageTopUp,
    UsageWallet,
    Village,
    Ward,
    WardProfile,
)
from .services import role_choices_for_candidate


class MobileFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css} mobile-input".strip()


class SupporterQuickForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = Supporter
        fields = [
            "full_name",
            "phone",
            "gender",
            "age_range",
            "province",
            "district",
            "llg",
            "ward",
            "village",
            "support_status",
            "influence_level",
            "main_issue",
            "follow_up_required",
            "follow_up_date",
            "consent_to_messages",
            "notes",
        ]
        widgets = {
            "follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate:
            self.fields["province"].queryset = self.fields["province"].queryset.filter(id=candidate.province_id)
            district_queryset = self.fields["district"].queryset.filter(province=candidate.province)
            if candidate.district_id:
                district_queryset = district_queryset.filter(id=candidate.district_id)
            self.fields["district"].queryset = district_queryset
            self.fields["llg"].queryset = self.fields["llg"].queryset.filter(district__in=district_queryset)
            self.fields["ward"].queryset = self.fields["ward"].queryset.filter(llg__district__in=district_queryset)
            self.fields["village"].queryset = self.fields["village"].queryset.filter(
                ward__llg__district__in=district_queryset, approval_status="APPROVED"
            )


class TeamMemberQuickForm(MobileFormMixin, forms.ModelForm):
    login_username = forms.CharField(
        max_length=150,
        required=False,
        help_text="Optional. Set a username so this team member can log in to the mobile app.",
    )
    login_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text="Set or reset the mobile-app password. Leave blank to keep the existing password.",
    )

    class Meta:
        model = TeamMember
        fields = [
            "full_name",
            "gender",
            "phone",
            "email",
            "role",
            "province",
            "district",
            "llg",
            "ward",
            "village",
            "influence_level",
            "notes",
            "is_active",
        ]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, candidate=None, creator_member=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.candidate = candidate
        self.creator_member = creator_member
        if candidate:
            self.fields["role"].choices = role_choices_for_candidate(candidate)
            self.fields["province"].queryset = self.fields["province"].queryset.filter(id=candidate.province_id)
            district_queryset = candidate.available_districts()
            self.fields["district"].queryset = district_queryset
            self.fields["llg"].queryset = candidate.available_llgs()
            self.fields["ward"].queryset = candidate.available_wards()
            self.fields["village"].queryset = self.fields["village"].queryset.filter(
                ward__in=candidate.available_wards(), approval_status="APPROVED"
            )
            self._restrict_to_creator(creator_member)
        if self.instance and self.instance.pk and self.instance.user_id:
            self.fields["login_username"].initial = self.instance.user.username

    def _restrict_to_creator(self, creator_member):
        """Limit the role choices to subordinate roles, and the geography fields
        to the creator's own branch, so coordinators only build their own team."""
        from .permissions import VIEW_ALL_ROLES, creatable_roles

        if creator_member is None or creator_member.role in VIEW_ALL_ROLES:
            return  # candidate / manager / IT admin create campaign-wide
        # Restrict creatable roles.
        self.fields["role"].choices = creatable_roles(creator_member, self.candidate)
        # Lock geography to the creator's assignment and narrow the level below.
        if creator_member.district_id:
            self.fields["district"].queryset = self.fields["district"].queryset.filter(id=creator_member.district_id)
            self.fields["district"].initial = creator_member.district_id
        if creator_member.llg_id:
            self.fields["llg"].queryset = self.fields["llg"].queryset.filter(id=creator_member.llg_id)
            self.fields["llg"].initial = creator_member.llg_id
        elif creator_member.district_id:
            self.fields["llg"].queryset = self.fields["llg"].queryset.filter(district_id=creator_member.district_id)
        if creator_member.ward_id:
            self.fields["ward"].queryset = self.fields["ward"].queryset.filter(id=creator_member.ward_id)
            self.fields["ward"].initial = creator_member.ward_id
        elif creator_member.llg_id:
            self.fields["ward"].queryset = self.fields["ward"].queryset.filter(llg_id=creator_member.llg_id)
        if creator_member.village_id:
            self.fields["village"].queryset = self.fields["village"].queryset.filter(id=creator_member.village_id)
        elif creator_member.ward_id:
            self.fields["village"].queryset = self.fields["village"].queryset.filter(ward_id=creator_member.ward_id)

    def clean_login_username(self):
        from django.contrib.auth import get_user_model

        username = (self.cleaned_data.get("login_username") or "").strip()
        if not username:
            return username
        User = get_user_model()
        clash = User.objects.filter(username__iexact=username)
        if self.instance and self.instance.pk and self.instance.user_id:
            clash = clash.exclude(pk=self.instance.user_id)
        if clash.exists():
            raise forms.ValidationError("That username is already taken. Choose another.")
        return username

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get("login_username")
        password = cleaned.get("login_password")
        creating_login = username and not (self.instance and self.instance.user_id)
        if creating_login and not password:
            self.add_error("login_password", "Set a password when creating a new mobile login.")
        if password and not username and not (self.instance and self.instance.user_id):
            self.add_error("login_username", "Set a username to enable mobile login.")
        return cleaned


class VillageQuickForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = Village
        fields = ["ward", "name"]

    def __init__(self, *args, candidate=None, creator_member=None, **kwargs):
        super().__init__(*args, **kwargs)
        qs = candidate.available_wards() if candidate else Ward.objects.all()
        if creator_member is not None:
            from .permissions import VIEW_ALL_ROLES

            if creator_member.role not in VIEW_ALL_ROLES:
                if creator_member.ward_id:
                    qs = qs.filter(id=creator_member.ward_id)
                elif creator_member.llg_id:
                    qs = qs.filter(llg_id=creator_member.llg_id)
                elif creator_member.district_id:
                    qs = qs.filter(llg__district_id=creator_member.district_id)
        self.fields["ward"].queryset = qs
        self.fields["name"].widget.attrs["placeholder"] = "Village / area name"


class CallLogQuickForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = CallLog
        fields = [
            "caller",
            "called_team_member",
            "influencer",
            "supporter",
            "person_called",
            "person_type",
            "phone_number",
            "call_outcome",
            "discussion_summary",
            "issues_raised",
            "commitments_made",
            "follow_up_required",
            "follow_up_date",
            "next_call_due_date",
        ]
        widgets = {
            "discussion_summary": forms.Textarea(attrs={"rows": 3}),
            "issues_raised": forms.Textarea(attrs={"rows": 2}),
            "commitments_made": forms.Textarea(attrs={"rows": 2}),
            "follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "next_call_due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate:
            self.fields["caller"].queryset = self.fields["caller"].queryset.filter(candidate=candidate)
            self.fields["called_team_member"].queryset = self.fields["called_team_member"].queryset.filter(candidate=candidate)
            self.fields["influencer"].queryset = self.fields["influencer"].queryset.filter(candidate=candidate)
            self.fields["supporter"].queryset = self.fields["supporter"].queryset.filter(candidate=candidate)


class MessageQuickForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "sender",
            "recipient_type",
            "recipient_group",
            "subject",
            "body",
            "priority",
            "delivery_channel",
            "read_receipt_required",
            "acknowledgement_required",
            "status",
        ]
        widgets = {"body": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate:
            self.fields["sender"].queryset = self.fields["sender"].queryset.filter(candidate=candidate)
            from .services import message_target_options

            self.fields["recipient_type"] = forms.ChoiceField(choices=[(item, item) for item in message_target_options(candidate)])
            self.fields["recipient_type"].widget.attrs["class"] = "mobile-input"


class TaskQuickForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = CampaignTask
        fields = [
            "title",
            "description",
            "assigned_to",
            "assigned_by",
            "province",
            "district",
            "llg",
            "ward",
            "priority",
            "due_date",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate:
            if "assigned_to" in self.fields:
                self.fields["assigned_to"].queryset = self.fields["assigned_to"].queryset.filter(candidate=candidate)
            if "assigned_by" in self.fields:
                self.fields["assigned_by"].queryset = self.fields["assigned_by"].queryset.filter(candidate=candidate)
            if "province" in self.fields:
                self.fields["province"].queryset = self.fields["province"].queryset.filter(id=candidate.province_id)
            district_queryset = self.fields["district"].queryset.filter(province=candidate.province)
            if candidate.district_id:
                district_queryset = district_queryset.filter(id=candidate.district_id)
            if "district" in self.fields:
                self.fields["district"].queryset = district_queryset
            if "llg" in self.fields:
                self.fields["llg"].queryset = self.fields["llg"].queryset.filter(district__in=district_queryset)
            if "ward" in self.fields:
                self.fields["ward"].queryset = self.fields["ward"].queryset.filter(llg__district__in=district_queryset)


class InfluencerQuickForm(SupporterQuickForm):
    class Meta:
        model = Influencer
        fields = [
            "full_name",
            "phone",
            "alternative_phone",
            "email",
            "province",
            "district",
            "llg",
            "ward",
            "village",
            "community_role",
            "influence_category",
            "influence_level",
            "estimated_network_size",
            "relationship_status",
            "preferred_contact_method",
            "contact_frequency_days",
            "next_contact_due_date",
            "assigned_owner",
            "notes",
        ]
        widgets = {
            "next_contact_due_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, candidate=candidate, **kwargs)
        if candidate:
            self.fields["assigned_owner"].queryset = TeamMember.objects.filter(candidate=candidate)


class EventQuickForm(TaskQuickForm):
    class Meta:
        model = CampaignEvent
        fields = [
            "title",
            "event_type",
            "province",
            "district",
            "llg",
            "ward",
            "village",
            "venue",
            "landmark",
            "host_person",
            "start_datetime",
            "end_datetime",
            "expected_crowd_size",
            "talking_points",
            "issues_to_address",
            "people_to_acknowledge",
            "security_notes",
            "logistics_checklist",
        ]
        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "talking_points": forms.Textarea(attrs={"rows": 3}),
            "issues_to_address": forms.Textarea(attrs={"rows": 3}),
            "people_to_acknowledge": forms.Textarea(attrs={"rows": 2}),
            "security_notes": forms.Textarea(attrs={"rows": 2}),
            "logistics_checklist": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, candidate=candidate, **kwargs)
        if candidate:
            self.fields["village"].queryset = self.fields["village"].queryset.filter(ward__in=candidate.available_wards())
            self.fields["landmark"].queryset = self.fields["landmark"].queryset.filter(candidate=candidate)


class IssueQuickForm(TaskQuickForm):
    class Meta:
        model = CommunityIssue
        fields = [
            "title",
            "category",
            "description",
            "province",
            "district",
            "llg",
            "ward",
            "village",
            "reported_by",
            "priority",
            "status",
            "related_event",
            "related_influencer",
            "notes",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, candidate=candidate, **kwargs)
        if candidate:
            self.fields["village"].queryset = self.fields["village"].queryset.filter(ward__in=candidate.available_wards())
            self.fields["related_event"].queryset = self.fields["related_event"].queryset.filter(candidate=candidate)
            self.fields["related_influencer"].queryset = self.fields["related_influencer"].queryset.filter(candidate=candidate)


class PromiseQuickForm(TaskQuickForm):
    class Meta:
        model = PromiseTracker
        fields = [
            "title",
            "description",
            "made_by",
            "made_to",
            "province",
            "district",
            "llg",
            "ward",
            "event",
            "promise_date",
            "target_date",
            "status",
            "follow_up_owner",
            "notes",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "promise_date": forms.DateInput(attrs={"type": "date"}),
            "target_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, candidate=candidate, **kwargs)
        if candidate:
            self.fields["event"].queryset = self.fields["event"].queryset.filter(candidate=candidate)
            self.fields["follow_up_owner"].queryset = self.fields["follow_up_owner"].queryset.filter(candidate=candidate)


class PollingLocationQuickForm(TaskQuickForm):
    class Meta:
        model = PollingLocation
        fields = [
            "name",
            "province",
            "district",
            "llg",
            "ward",
            "village",
            "gps_coordinates",
            "assigned_scrutineer",
            "backup_scrutineer",
            "contact_number",
            "status",
            "transport_status",
            "notes",
        ]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, candidate=candidate, **kwargs)
        if candidate:
            scrutineers = TeamMember.objects.filter(candidate=candidate, role="SCRUTINEER")
            self.fields["assigned_scrutineer"].queryset = scrutineers
            self.fields["backup_scrutineer"].queryset = scrutineers


class PollingStatusQuickForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = PollingStatus
        fields = [
            "polling_location",
            "reported_by",
            "scrutineer_present",
            "booth_open",
            "materials_available",
            "communication_ok",
            "transport_notes",
            "logistical_issues",
            "notes",
        ]
        widgets = {
            "transport_notes": forms.Textarea(attrs={"rows": 2}),
            "logistical_issues": forms.Textarea(attrs={"rows": 2}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate:
            self.fields["polling_location"].queryset = self.fields["polling_location"].queryset.filter(candidate=candidate)
            self.fields["reported_by"].queryset = self.fields["reported_by"].queryset.filter(candidate=candidate)


class PollingIncidentQuickForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = PollingIncident
        fields = ["polling_location", "reported_by", "title", "description", "priority", "status"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate:
            self.fields["polling_location"].queryset = self.fields["polling_location"].queryset.filter(candidate=candidate)
            self.fields["reported_by"].queryset = self.fields["reported_by"].queryset.filter(candidate=candidate)


class CitizenRequestQuickForm(TaskQuickForm):
    class Meta:
        model = CitizenRequest
        fields = [
            "title",
            "requester_name",
            "phone",
            "province",
            "district",
            "llg",
            "ward",
            "village",
            "category",
            "description",
            "status",
            "assigned_to",
            "due_date",
            "resolution_notes",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "resolution_notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, candidate=candidate, **kwargs)
        if candidate:
            self.fields["assigned_to"].queryset = self.fields["assigned_to"].queryset.filter(candidate=candidate)


class WardProfileForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = WardProfile
        fields = [
            "ward",
            "councillor_name",
            "key_clans",
            "key_churches",
            "schools",
            "markets",
            "health_facilities",
            "important_landmarks",
            "access_routes",
            "meeting_places",
            "population_estimate",
            "estimated_voting_population",
            "previous_election_notes",
            "support_strength",
            "main_community_issues",
            "security_concerns",
            "youth_groups",
            "womens_groups",
            "church_groups",
            "business_groups",
            "important_families",
            "notes_for_candidate",
        ]
        widgets = {
            "key_clans": forms.Textarea(attrs={"rows": 2}),
            "key_churches": forms.Textarea(attrs={"rows": 2}),
            "schools": forms.Textarea(attrs={"rows": 2}),
            "markets": forms.Textarea(attrs={"rows": 2}),
            "health_facilities": forms.Textarea(attrs={"rows": 2}),
            "important_landmarks": forms.Textarea(attrs={"rows": 3}),
            "access_routes": forms.Textarea(attrs={"rows": 2}),
            "meeting_places": forms.Textarea(attrs={"rows": 2}),
            "previous_election_notes": forms.Textarea(attrs={"rows": 3}),
            "main_community_issues": forms.Textarea(attrs={"rows": 3}),
            "security_concerns": forms.Textarea(attrs={"rows": 2}),
            "youth_groups": forms.Textarea(attrs={"rows": 2}),
            "womens_groups": forms.Textarea(attrs={"rows": 2}),
            "church_groups": forms.Textarea(attrs={"rows": 2}),
            "business_groups": forms.Textarea(attrs={"rows": 2}),
            "important_families": forms.Textarea(attrs={"rows": 2}),
            "notes_for_candidate": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate:
            self.fields["ward"].queryset = candidate.available_wards()


class AIReviewForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = AIWorkItem
        fields = ["output", "status", "safety_notes"]
        widgets = {
            "output": forms.Textarea(attrs={"rows": 10}),
            "safety_notes": forms.Textarea(attrs={"rows": 4}),
        }


class SubscriptionQuoteForm(MobileFormMixin, forms.ModelForm):
    modules = forms.ModelMultipleChoiceField(
        queryset=SoftwareModule.objects.filter(is_active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    bundles = forms.ModelMultipleChoiceField(
        queryset=ModuleBundle.objects.filter(is_active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = SubscriptionQuote
        fields = ["billing_cycle", "currency", "modules", "bundles", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["modules"].queryset = SoftwareModule.objects.filter(is_active=True).order_by("sort_order", "name")
        self.fields["bundles"].queryset = ModuleBundle.objects.filter(is_active=True).order_by("sort_order", "name")


class ImportBatchForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = ImportBatch
        fields = ["import_type", "uploaded_file"]


class ExportRequestForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = ExportRequest
        fields = ["export_type", "filters"]
        widgets = {"filters": forms.Textarea(attrs={"rows": 3})}

    def clean_filters(self):
        # A blank JSON textarea returns None, which violates the NOT NULL column.
        return self.cleaned_data.get("filters") or {}


class TenantSettingsForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = TenantSettings
        fields = [
            "sms_sender_name",
            "default_call_frequency_high",
            "default_call_frequency_medium",
            "default_call_frequency_low",
            "export_requires_approval",
            "ai_assistant_enabled",
            "polling_day_mode",
            "constituency_mode",
            "data_retention_notes",
        ]
        widgets = {"data_retention_notes": forms.Textarea(attrs={"rows": 3})}


class ConnectorSettingForm(MobileFormMixin, forms.ModelForm):
    SECRET_FIELDS = [
        "api_key",
        "api_secret",
        "access_token",
        "webhook_secret",
        "email_password",
        "payment_secret_key",
        "maps_api_key",
    ]

    class Meta:
        model = ConnectorSetting
        fields = [
            "connector_type",
            "name",
            "provider",
            "is_enabled",
            "status",
            "api_base_url",
            "api_key",
            "api_secret",
            "access_token",
            "webhook_url",
            "webhook_secret",
            "ai_model",
            "ai_temperature",
            "ai_system_policy",
            "whatsapp_phone_number_id",
            "whatsapp_business_account_id",
            "whatsapp_default_template",
            "sms_sender_id",
            "sms_default_country_code",
            "email_host",
            "email_port",
            "email_username",
            "email_password",
            "email_use_tls",
            "email_from_address",
            "payment_public_key",
            "payment_secret_key",
            "payment_merchant_id",
            "maps_api_key",
            "extra_config",
            "notes",
        ]
        widgets = {
            "api_secret": forms.PasswordInput(render_value=False),
            "api_key": forms.PasswordInput(render_value=False),
            "access_token": forms.PasswordInput(render_value=False),
            "webhook_secret": forms.PasswordInput(render_value=False),
            "email_password": forms.PasswordInput(render_value=False),
            "payment_secret_key": forms.PasswordInput(render_value=False),
            "maps_api_key": forms.PasswordInput(render_value=False),
            "ai_system_policy": forms.Textarea(attrs={"rows": 4}),
            "extra_config": forms.Textarea(attrs={"rows": 4}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_extra_config(self):
        # A blank JSON textarea returns None, which violates the NOT NULL column.
        return self.cleaned_data.get("extra_config") or {}

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.pk:
            existing = ConnectorSetting.objects.get(pk=instance.pk)
            for field in self.SECRET_FIELDS:
                if not self.cleaned_data.get(field):
                    setattr(instance, field, getattr(existing, field))
        if instance.is_enabled and instance.status == ConnectorSetting.Status.DISABLED:
            instance.status = ConnectorSetting.Status.NEEDS_TEST
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class UsageRateCardForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = UsageRateCard
        fields = [
            "service",
            "provider",
            "model_name",
            "unit",
            "currency",
            "provider_cost_per_unit",
            "markup_percent",
            "fixed_markup_per_unit",
            "minimum_charge",
            "is_free",
            "is_active",
            "effective_from",
            "notes",
        ]
        widgets = {
            "effective_from": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class UsageTopUpForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = UsageTopUp
        fields = ["wallet", "amount", "currency", "payment_method", "payment_reference", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, candidate=None, **kwargs):
        super().__init__(*args, **kwargs)
        if candidate:
            self.fields["wallet"].queryset = UsageWallet.objects.filter(candidate=candidate, is_active=True)


class FreeAIModelForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = FreeAIModel
        fields = [
            "name",
            "provider",
            "model_id",
            "context_window",
            "daily_free_requests",
            "monthly_free_requests",
            "is_active",
            "notes",
        ]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}


class PlanAIModelForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = PlanAIModel
        fields = ["plan", "ai_model", "is_default"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ai_model"].queryset = FreeAIModel.objects.filter(is_active=True).order_by("provider", "name")
        self.fields["ai_model"].label = "Free AI model"
        self.fields["is_default"].help_text = "Tenants on this plan will use this model automatically for all AI features."


class IncludedUsageQuotaForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = IncludedUsageQuota
        fields = [
            "module",
            "bundle",
            "service",
            "unit",
            "quantity",
            "billing_cycle",
            "description",
            "is_active",
        ]


# ── PNG campaign feature forms ────────────────────────────────────────────────

class PreferenceDealForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = PreferenceDeal
        fields = [
            "partner_candidate_name",
            "partner_party",
            "partner_seat",
            "preference_number",
            "status",
            "contact_person",
            "ward_directives",
            "deal_terms",
            "notes",
        ]
        widgets = {
            "ward_directives": forms.Textarea(attrs={"rows": 3}),
            "deal_terms": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, candidate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contact_person"].queryset = TeamMember.objects.filter(candidate=candidate, is_active=True)


class CommunityGroupForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = CommunityGroup
        fields = ["name", "group_type", "ward", "village", "estimated_voting_members", "alignment", "key_contact", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, candidate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Village
        self.fields["ward"].queryset = candidate.available_wards()
        self.fields["village"].queryset = Village.objects.filter(ward__in=candidate.available_wards())
        self.fields["key_contact"].queryset = Influencer.objects.filter(candidate=candidate)
        self.fields["key_contact"].required = False


class CommunityAssistanceForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = CommunityAssistance
        fields = [
            "ward",
            "village",
            "date",
            "recipient_group",
            "assistance_type",
            "description",
            "estimated_value_pgk",
            "approved_by",
            "related_event",
            "notes",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 2}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, candidate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Village, CampaignEvent
        self.fields["ward"].queryset = candidate.available_wards()
        self.fields["village"].queryset = Village.objects.filter(ward__in=candidate.available_wards())
        self.fields["approved_by"].queryset = TeamMember.objects.filter(candidate=candidate, is_active=True)
        self.fields["related_event"].queryset = CampaignEvent.objects.filter(candidate=candidate).order_by("-start_datetime")
        self.fields["village"].required = False
        self.fields["approved_by"].required = False
        self.fields["related_event"].required = False


class CompetitorActivityForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = CompetitorActivity
        fields = [
            "opponent_name",
            "opponent_party",
            "ward",
            "date",
            "activity_type",
            "source",
            "description",
            "response_action",
            "response_assigned_to",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "response_action": forms.Textarea(attrs={"rows": 2}),
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, candidate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ward"].queryset = candidate.available_wards()
        self.fields["response_assigned_to"].queryset = TeamMember.objects.filter(candidate=candidate, is_active=True)
        self.fields["ward"].required = False
        self.fields["response_assigned_to"].required = False


class DevelopmentFundForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = DevelopmentFund
        fields = ["fund_name", "fund_type", "financial_year", "total_allocation_pgk", "spent_pgk", "ward", "district", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, candidate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ward"].queryset = candidate.available_wards()
        self.fields["district"].queryset = candidate.available_districts()
        self.fields["ward"].required = False
        self.fields["district"].required = False


class RegistrationDriveForm(MobileFormMixin, forms.ModelForm):
    class Meta:
        model = RegistrationDrive
        fields = ["title", "ward", "start_date", "end_date", "team_members", "target_count", "actual_count", "status", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, candidate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ward"].queryset = candidate.available_wards()
        self.fields["team_members"].queryset = TeamMember.objects.filter(candidate=candidate, is_active=True)
        self.fields["end_date"].required = False
