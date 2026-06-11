from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import (
    CallLog,
    CommunityGroup,
    CompetitorActivity,
    Influencer,
    Message,
    MessageRecipient,
    PollingLocation,
    PollingStatus,
    PreferenceDeal,
    RegistrationDrive,
    Supporter,
    TeamMember,
    WardProfile,
)


# ─── Auth ─────────────────────────────────────────────────────────────────────

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["username"],
            password=attrs["password"],
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")
        attrs["user"] = user
        return attrs


# ─── Supporter ────────────────────────────────────────────────────────────────

class SupporterSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source="province.name", read_only=True)
    district_name = serializers.CharField(source="district.name", read_only=True, default=None)
    llg_name = serializers.CharField(source="llg.name", read_only=True, default=None)
    ward_name = serializers.CharField(source="ward.name", read_only=True, default=None)
    village_name = serializers.CharField(source="village.name", read_only=True, default=None)

    class Meta:
        model = Supporter
        fields = [
            "id",
            "full_name",
            "gender",
            "age_range",
            "phone",
            "province",
            "province_name",
            "district",
            "district_name",
            "llg",
            "llg_name",
            "ward",
            "ward_name",
            "village",
            "village_name",
            "clan",
            "church_group",
            "occupation",
            "enrollment_status",
            "support_status",
            "influence_level",
            "introduced_by",
            "main_issue",
            "follow_up_required",
            "follow_up_date",
            "consent_to_messages",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context["request"]
        team_member = TeamMember.objects.filter(user=request.user).first()
        if not team_member:
            raise serializers.ValidationError("No TeamMember found for this user.")
        validated_data["candidate"] = team_member.candidate
        validated_data["created_by"] = request.user
        return super().create(validated_data)


# ─── TeamMember ───────────────────────────────────────────────────────────────

class TeamMemberSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source="province.name", read_only=True)
    ward_name = serializers.CharField(source="ward.name", read_only=True, default=None)

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "full_name",
            "gender",
            "phone",
            "email",
            "role",
            "province",
            "province_name",
            "district",
            "llg",
            "ward",
            "ward_name",
            "village",
            "influence_level",
            "is_active",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ─── Influencer ───────────────────────────────────────────────────────────────

class InfluencerSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source="ward.name", read_only=True, default=None)

    class Meta:
        model = Influencer
        fields = [
            "id",
            "full_name",
            "phone",
            "alternative_phone",
            "community_role",
            "influence_level",
            "relationship_status",
            "preferred_contact_method",
            "contact_frequency_days",
            "last_call_date",
            "next_contact_due_date",
            "ward",
            "ward_name",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ─── Message ──────────────────────────────────────────────────────────────────

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True, default=None)
    is_read = serializers.SerializerMethodField()
    is_acknowledged = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "subject",
            "body",
            "message_type",
            "recipient_type",
            "priority",
            "delivery_channel",
            "status",
            "sender_name",
            "read_receipt_required",
            "acknowledgement_required",
            "sent_at",
            "is_read",
            "is_acknowledged",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_is_read(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        team_member = TeamMember.objects.filter(user=request.user).first()
        if not team_member:
            return False
        recipient = obj.recipients.filter(team_member=team_member).first()
        return recipient.read_at is not None if recipient else False

    def get_is_acknowledged(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        team_member = TeamMember.objects.filter(user=request.user).first()
        if not team_member:
            return False
        recipient = obj.recipients.filter(team_member=team_member).first()
        return recipient.acknowledged_at is not None if recipient else False


# ─── WardProfile ──────────────────────────────────────────────────────────────

class WardProfileSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source="ward.name", read_only=True)
    ward_number = serializers.CharField(source="ward.number", read_only=True)
    llg_name = serializers.CharField(source="ward.llg.name", read_only=True)

    class Meta:
        model = WardProfile
        fields = [
            "id",
            "ward",
            "ward_name",
            "ward_number",
            "llg_name",
            "councillor_name",
            "support_strength",
            "population_estimate",
            "estimated_voting_population",
            "key_clans",
            "key_churches",
            "main_community_issues",
            "notes_for_candidate",
            "security_concerns",
            "previous_election_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ─── CallLog ──────────────────────────────────────────────────────────────────

class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = [
            "id",
            "caller",
            "influencer",
            "supporter",
            "person_called",
            "person_type",
            "phone_number",
            "call_datetime",
            "call_outcome",
            "discussion_summary",
            "issues_raised",
            "commitments_made",
            "follow_up_required",
            "follow_up_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context["request"]
        team_member = TeamMember.objects.filter(user=request.user).first()
        if not team_member:
            raise serializers.ValidationError("No TeamMember found for this user.")
        validated_data["candidate"] = team_member.candidate
        validated_data["created_by"] = request.user
        return super().create(validated_data)


# ─── CommunityGroup ───────────────────────────────────────────────────────────

class CommunityGroupSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source="ward.name", read_only=True)

    class Meta:
        model = CommunityGroup
        fields = [
            "id",
            "name",
            "group_type",
            "ward",
            "ward_name",
            "village",
            "estimated_voting_members",
            "alignment",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context["request"]
        team_member = TeamMember.objects.filter(user=request.user).first()
        if not team_member:
            raise serializers.ValidationError("No TeamMember found for this user.")
        validated_data["candidate"] = team_member.candidate
        validated_data["created_by"] = request.user
        return super().create(validated_data)


# ─── PollingLocation ──────────────────────────────────────────────────────────

class PollingLocationSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source="ward.name", read_only=True, default=None)
    scrutineer_name = serializers.CharField(
        source="assigned_scrutineer.full_name", read_only=True, default=None
    )

    class Meta:
        model = PollingLocation
        fields = [
            "id",
            "name",
            "ward",
            "ward_name",
            "village",
            "gps_coordinates",
            "assigned_scrutineer",
            "scrutineer_name",
            "contact_number",
            "status",
            "scrutineer_checked_in",
            "security_risk",
            "expected_turnout",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ─── PollingStatus ────────────────────────────────────────────────────────────

class PollingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollingStatus
        fields = [
            "id",
            "polling_location",
            "reported_by",
            "status_time",
            "scrutineer_present",
            "booth_open",
            "materials_available",
            "communication_ok",
            "our_tally",
            "transport_notes",
            "logistical_issues",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context["request"]
        team_member = TeamMember.objects.filter(user=request.user).first()
        if not team_member:
            raise serializers.ValidationError("No TeamMember found for this user.")
        validated_data["candidate"] = team_member.candidate
        validated_data["created_by"] = request.user
        return super().create(validated_data)


# ─── CompetitorActivity ───────────────────────────────────────────────────────

class CompetitorActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorActivity
        fields = [
            "id",
            "opponent_name",
            "opponent_party",
            "ward",
            "date",
            "activity_type",
            "source",
            "description",
            "response_action",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context["request"]
        team_member = TeamMember.objects.filter(user=request.user).first()
        if not team_member:
            raise serializers.ValidationError("No TeamMember found for this user.")
        validated_data["candidate"] = team_member.candidate
        validated_data["created_by"] = request.user
        return super().create(validated_data)


# ─── PreferenceDeal ───────────────────────────────────────────────────────────

class PreferenceDealSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenceDeal
        fields = [
            "id",
            "partner_candidate_name",
            "partner_party",
            "partner_seat",
            "preference_number",
            "status",
            "ward_directives",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ─── RegistrationDrive ────────────────────────────────────────────────────────

class RegistrationDriveSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source="ward.name", read_only=True)

    class Meta:
        model = RegistrationDrive
        fields = [
            "id",
            "title",
            "ward",
            "ward_name",
            "start_date",
            "end_date",
            "target_count",
            "actual_count",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ─── Batch Sync ───────────────────────────────────────────────────────────────

class SyncItemSerializer(serializers.Serializer):
    entity_type = serializers.CharField()
    operation = serializers.ChoiceField(choices=["CREATE", "UPDATE", "DELETE"])
    local_id = serializers.CharField()
    server_id = serializers.IntegerField(required=False, allow_null=True)
    payload = serializers.DictField()


class BatchSyncSerializer(serializers.Serializer):
    items = SyncItemSerializer(many=True)
