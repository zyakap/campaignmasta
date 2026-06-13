from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
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


class StandardPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200


def _get_candidate(request):
    """Resolve the Candidate from the authenticated user's TeamMember."""
    team_member = TeamMember.objects.filter(user=request.user).select_related("candidate").first()
    if not team_member:
        return None
    return team_member.candidate


def _updated_after_filter(queryset, request):
    updated_after = request.query_params.get("updated_after")
    if updated_after:
        try:
            from django.utils.dateparse import parse_datetime
            dt = parse_datetime(updated_after)
            if dt:
                queryset = queryset.filter(updated_at__gte=dt)
        except Exception:
            pass
    return queryset


# ─── Login ────────────────────────────────────────────────────────────────────

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_scope = "login"

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        team_member = TeamMember.objects.filter(user=user).select_related("candidate").first()
        if not team_member:
            return Response(
                {"detail": "No campaign team role found for this account."},
                status=status.HTTP_403_FORBIDDEN,
            )
        candidate = team_member.candidate
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "candidate_id": candidate.pk,
                "candidate_name": candidate.name,
                "subscription_plan": candidate.subscription_plan,
                "role": team_member.role,
            }
        )


# ─── Dashboard ────────────────────────────────────────────────────────────────

class DashboardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
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
    pagination_class = StandardPagination

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
        qs = Supporter.objects.filter(candidate=candidate).select_related(
            "province", "district", "llg", "ward", "village"
        ).order_by("full_name")
        qs = _updated_after_filter(qs, request)
        paginator = StandardPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = SupporterSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SupporterSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        supporter = serializer.save()
        return Response(SupporterSerializer(supporter, context={"request": request}).data, status=status.HTTP_201_CREATED)


# ─── TeamMembers ──────────────────────────────────────────────────────────────

class TeamMemberListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
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

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
        qs = Influencer.objects.filter(candidate=candidate).select_related("ward").order_by("full_name")
        qs = _updated_after_filter(qs, request)
        serializer = InfluencerSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


# ─── Messages ─────────────────────────────────────────────────────────────────

class MessageListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
        qs = Message.objects.filter(candidate=candidate, status="SENT").order_by("-sent_at")
        qs = _updated_after_filter(qs, request)
        serializer = MessageSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


class MessageReadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
        try:
            message = Message.objects.get(pk=pk, candidate=candidate)
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        team_member = TeamMember.objects.filter(user=request.user).first()
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

    def post(self, request, pk):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
        try:
            message = Message.objects.get(pk=pk, candidate=candidate)
        except Message.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        team_member = TeamMember.objects.filter(user=request.user).first()
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

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
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

    def post(self, request):
        serializer = CallLogSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        call_log = serializer.save()
        return Response(CallLogSerializer(call_log, context={"request": request}).data, status=status.HTTP_201_CREATED)


# ─── CommunityGroups ──────────────────────────────────────────────────────────

class CommunityGroupListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
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

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
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

    def post(self, request):
        serializer = PollingStatusSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        ps = serializer.save()
        return Response(PollingStatusSerializer(ps, context={"request": request}).data, status=status.HTTP_201_CREATED)


# ─── CompetitorActivity ───────────────────────────────────────────────────────

class CompetitorActivityCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompetitorActivitySerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()
        return Response(CompetitorActivitySerializer(activity, context={"request": request}).data, status=status.HTTP_201_CREATED)


# ─── PreferenceDeals ──────────────────────────────────────────────────────────

class PreferenceDealListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
        qs = PreferenceDeal.objects.filter(candidate=candidate).order_by("-created_at")
        qs = _updated_after_filter(qs, request)
        serializer = PreferenceDealSerializer(qs, many=True, context={"request": request})
        return Response({"results": serializer.data, "count": qs.count()})


# ─── RegistrationDrives ───────────────────────────────────────────────────────

class RegistrationDriveListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)
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
    throttle_scope = "sync"

    def post(self, request):
        batch_serializer = BatchSyncSerializer(data=request.data)
        batch_serializer.is_valid(raise_exception=True)
        items = batch_serializer.validated_data["items"]
        candidate = _get_candidate(request)
        if not candidate:
            return Response({"detail": "No candidate found."}, status=status.HTTP_403_FORBIDDEN)

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
            except Exception as exc:
                results.append({"local_id": local_id, "server_id": server_id, "status": f"ERROR: {exc}"})

        return Response({"results": results})
