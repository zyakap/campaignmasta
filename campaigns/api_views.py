import logging

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

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
from .serializers import (
    BatchSyncSerializer,
    CallLogSerializer,
    CommunityGroupSerializer,
    CompetitorActivitySerializer,
    InfluencerSerializer,
    LoginSerializer,
    MessageSerializer,
    PollingLocationSerializer,
    PollingStatusSerializer,
    PreferenceDealSerializer,
    RegistrationDriveSerializer,
    SupporterSerializer,
    TeamMemberSerializer,
    WardProfileSerializer,
)

logger = logging.getLogger(__name__)


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


class LoginRateThrottle(AnonRateThrottle):
    rate = "10/minute"
    scope = "login"


def _get_candidate(request):
    """Resolve the Candidate from the authenticated user's TeamMember."""
    team_member = TeamMember.objects.filter(user=request.user, is_active=True).select_related("candidate").first()
    if not team_member:
        return None, None
    return team_member.candidate, team_member


def _updated_after_filter(queryset, request):
    updated_after = request.query_params.get("updated_after")
    if not updated_after:
        return queryset
    dt = parse_datetime(updated_after)
    if dt is None:
        logger.warning("Invalid updated_after value: %s", updated_after)
        return queryset
    return queryset.filter(updated_at__gte=dt)


def _candidate_or_403(request):
    """Return (candidate, team_member) or raise a 403 Response."""
    candidate, member = _get_candidate(request)
    if not candidate:
        return None, None, Response({"detail": "No active campaign team role found."}, status=status.HTTP_403_FORBIDDEN)
    return candidate, member, None


# ─── Login ────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        team_member = TeamMember.objects.filter(user=user, is_active=True).select_related("candidate").first()
        if not team_member:
            return Response(
                {"detail": "No active campaign team role found for this account."},
                status=status.HTTP_403_FORBIDDEN,
            )
        candidate = team_member.candidate
        logger.info("API login: user=%s candidate=%s role=%s", user.username, candidate.name, team_member.role)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "candidate_id": candidate.pk,
                "candidate_name": candidate.name,
                "candidate_type": candidate.candidate_type,
                "subscription_plan": candidate.subscription_plan,
                "role": team_member.role,
                "team_member_id": team_member.pk,
                "full_name": team_member.full_name,
                "province": candidate.province.name if candidate.province_id else None,
                "district": candidate.district.name if candidate.district_id else None,
            }
        )


# ─── Dashboard ────────────────────────────────────────────────────────────────

class DashboardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, member, err = _candidate_or_403(request)
        if err:
            return err
        supporter_count = Supporter.objects.filter(candidate=candidate).count()
        today = timezone.localdate()
        calls_due_count = Influencer.objects.filter(
            candidate=candidate, next_contact_due_date__lte=today
        ).count()
        messages_unread_count = (
            Message.objects.filter(candidate=candidate, status="SENT")
            .exclude(
                recipients__team_member__user=request.user,
                recipients__read_at__isnull=False,
            )
            .count()
        )
        return Response(
            {
                "supporter_count": supporter_count,
                "calls_due_count": calls_due_count,
                "messages_unread_count": messages_unread_count,
                "sync_timestamp": timezone.now().isoformat(),
            }
        )


# ─── Supporters ───────────────────────────────────────────────────────────────

class SupporterListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    pagination_class = StandardPagination

    def get(self, request):
        candidate, member, err = _candidate_or_403(request)
        if err:
            return err
        qs = Supporter.objects.filter(candidate=candidate).select_related(
            "province", "district", "llg", "ward", "village"
        ).order_by("full_name")
        # Enforce geographic scope for non-superuser team members
        if member and not request.user.is_superuser:
            qs = _apply_geographic_filter(qs, member)
        qs = _updated_after_filter(qs, request)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = SupporterSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        candidate, member, err = _candidate_or_403(request)
        if err:
            return err
        serializer = SupporterSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        supporter = serializer.save()
        return Response(SupporterSerializer(supporter, context={"request": request}).data, status=status.HTTP_201_CREATED)


def _apply_geographic_filter(queryset, member):
    """Restrict queryset to the geographic area of a non-admin team member."""
    from .models import Role
    if member.role in (Role.WARD_COORDINATOR, Role.VILLAGE_COORDINATOR, Role.SCRUTINEER, Role.VOLUNTEER):
        if member.ward_id:
            return queryset.filter(ward_id=member.ward_id)
    if member.role == Role.LLG_COORDINATOR and member.llg_id:
        return queryset.filter(llg_id=member.llg_id)
    if member.role == Role.DISTRICT_COORDINATOR and member.district_id:
        return queryset.filter(district_id=member.district_id)
    return queryset


# ─── TeamMembers ──────────────────────────────────────────────────────────────

class TeamMemberListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        qs = TeamMember.objects.filter(candidate=candidate, is_active=True).select_related(
            "province", "district", "llg", "ward"
        ).order_by("full_name")
        qs = _updated_after_filter(qs, request)
        serializer = TeamMemberSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


# ─── Influencers ──────────────────────────────────────────────────────────────

class InfluencerListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, member, err = _candidate_or_403(request)
        if err:
            return err
        qs = Influencer.objects.filter(candidate=candidate).select_related("ward").order_by("full_name")
        if member and not request.user.is_superuser:
            qs = _apply_geographic_filter(qs, member)
        qs = _updated_after_filter(qs, request)
        serializer = InfluencerSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


# ─── Messages ─────────────────────────────────────────────────────────────────

class MessageListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        qs = Message.objects.filter(candidate=candidate, status="SENT").order_by("-sent_at")
        qs = _updated_after_filter(qs, request)
        serializer = MessageSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


class MessageReadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, pk):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        try:
            message = Message.objects.get(pk=pk, candidate=candidate)
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        team_member = TeamMember.objects.filter(user=request.user, is_active=True).first()
        if team_member:
            recipient, _ = MessageRecipient.objects.get_or_create(
                message=message,
                team_member=team_member,
                defaults={"display_name": team_member.full_name},
            )
            if not recipient.read_at:
                recipient.read_at = timezone.now()
                recipient.save(update_fields=["read_at"])
        return Response({"status": "ok"})


class MessageAcknowledgeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, pk):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        try:
            message = Message.objects.get(pk=pk, candidate=candidate)
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        team_member = TeamMember.objects.filter(user=request.user, is_active=True).first()
        if team_member:
            recipient, _ = MessageRecipient.objects.get_or_create(
                message=message,
                team_member=team_member,
                defaults={"display_name": team_member.full_name},
            )
            if not recipient.acknowledged_at:
                recipient.acknowledged_at = timezone.now()
                if not recipient.read_at:
                    recipient.read_at = timezone.now()
                recipient.save(update_fields=["acknowledged_at", "read_at"])
        return Response({"status": "ok"})


# ─── WardProfiles ─────────────────────────────────────────────────────────────

class WardProfileListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        qs = WardProfile.objects.filter(candidate=candidate).select_related(
            "ward", "ward__llg"
        ).order_by("ward__name")
        qs = _updated_after_filter(qs, request)
        serializer = WardProfileSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


# ─── CallLogs ─────────────────────────────────────────────────────────────────

class CallLogCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = CallLogSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        call_log = serializer.save()
        return Response(CallLogSerializer(call_log, context={"request": request}).data, status=status.HTTP_201_CREATED)


# ─── CommunityGroups ──────────────────────────────────────────────────────────

class CommunityGroupListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        qs = CommunityGroup.objects.filter(candidate=candidate).select_related("ward").order_by("name")
        qs = _updated_after_filter(qs, request)
        serializer = CommunityGroupSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})

    def post(self, request):
        serializer = CommunityGroupSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        return Response(CommunityGroupSerializer(group, context={"request": request}).data, status=status.HTTP_201_CREATED)


# ─── PollingLocations ─────────────────────────────────────────────────────────

class PollingLocationListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        qs = PollingLocation.objects.filter(candidate=candidate).select_related(
            "ward", "assigned_scrutineer"
        ).order_by("name")
        qs = _updated_after_filter(qs, request)
        serializer = PollingLocationSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


# ─── PollingStatus ────────────────────────────────────────────────────────────

class PollingStatusCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = PollingStatusSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        ps = serializer.save()
        return Response(PollingStatusSerializer(ps, context={"request": request}).data, status=status.HTTP_201_CREATED)


# ─── CompetitorActivity ───────────────────────────────────────────────────────

class CompetitorActivityCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = CompetitorActivitySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()
        return Response(CompetitorActivitySerializer(activity, context={"request": request}).data, status=status.HTTP_201_CREATED)


# ─── PreferenceDeals ──────────────────────────────────────────────────────────

class PreferenceDealListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        qs = PreferenceDeal.objects.filter(candidate=candidate).order_by("-created_at")
        qs = _updated_after_filter(qs, request)
        serializer = PreferenceDealSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


# ─── RegistrationDrives ───────────────────────────────────────────────────────

class RegistrationDriveListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err
        qs = RegistrationDrive.objects.filter(candidate=candidate).select_related("ward").order_by("-start_date")
        qs = _updated_after_filter(qs, request)
        serializer = RegistrationDriveSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


# ─── Batch Sync Push ──────────────────────────────────────────────────────────

ENTITY_SERIALIZER_MAP = {
    "supporter": (Supporter, SupporterSerializer),
    "call_log": (CallLog, CallLogSerializer),
    "polling_status": (PollingStatus, PollingStatusSerializer),
    "competitor_activity": (CompetitorActivity, CompetitorActivitySerializer),
    "community_group": (CommunityGroup, CommunityGroupSerializer),
}


class SyncPushView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        batch_serializer = BatchSyncSerializer(data=request.data)
        batch_serializer.is_valid(raise_exception=True)
        items = batch_serializer.validated_data["items"]
        candidate, _, err = _candidate_or_403(request)
        if err:
            return err

        results = []
        for item in items:
            entity_type = item["entity_type"]
            operation = item["operation"]
            local_id = item["local_id"]
            server_id = item.get("server_id")
            payload = item["payload"]

            if entity_type not in ENTITY_SERIALIZER_MAP:
                results.append({"local_id": local_id, "server_id": None, "status": "UNKNOWN_ENTITY"})
                continue

            model_cls, serializer_cls = ENTITY_SERIALIZER_MAP[entity_type]

            try:
                if operation == "CREATE":
                    ser = serializer_cls(data=payload, context={"request": request})
                    ser.is_valid(raise_exception=True)
                    obj = ser.save()
                    results.append({"local_id": local_id, "server_id": obj.pk, "status": "OK"})

                elif operation == "UPDATE" and server_id:
                    obj = model_cls.objects.get(pk=server_id, candidate=candidate)
                    ser = serializer_cls(obj, data=payload, partial=True, context={"request": request})
                    ser.is_valid(raise_exception=True)
                    ser.save()
                    results.append({"local_id": local_id, "server_id": server_id, "status": "OK"})

                elif operation == "DELETE" and server_id:
                    model_cls.objects.filter(pk=server_id, candidate=candidate).delete()
                    results.append({"local_id": local_id, "server_id": server_id, "status": "OK"})
                else:
                    results.append({"local_id": local_id, "server_id": server_id, "status": "INVALID"})

            except model_cls.DoesNotExist:
                results.append({"local_id": local_id, "server_id": server_id, "status": "NOT_FOUND"})
            except Exception as exc:
                logger.exception("SyncPush error: entity=%s op=%s local_id=%s", entity_type, operation, local_id)
                results.append({"local_id": local_id, "server_id": server_id, "status": f"ERROR: {exc}"})

        return Response({"results": results, "processed": len(results)})
