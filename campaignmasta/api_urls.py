from django.urls import path

from campaigns.api_views import (
    CallLogCreateView,
    CommunityGroupListCreateView,
    CompetitorActivityCreateView,
    CreatableRolesView,
    DashboardView,
    GeographyView,
    InfluencerListView,
    LoginView,
    PerformanceView,
    MessageAcknowledgeView,
    MessageListView,
    MessageReadView,
    PollingLocationListView,
    PollingStatusCreateView,
    PreferenceDealListView,
    RegistrationDriveListView,
    SupporterDetailView,
    SupporterListCreateView,
    SyncPushView,
    TeamMemberApproveView,
    TeamMemberListView,
    TeamMemberPendingView,
    VillageApproveView,
    VillageListCreateView,
    WardProfileListView,
)

urlpatterns = [
    # Auth
    path("auth/login/", LoginView.as_view(), name="api_login"),

    # Dashboard
    path("dashboard/", DashboardView.as_view(), name="api_dashboard"),

    # Supporters
    path("supporters/", SupporterListCreateView.as_view(), name="api_supporters"),
    path("supporters/<int:pk>/", SupporterDetailView.as_view(), name="api_supporter_detail"),

    # Team Members & hierarchy
    path("team-members/", TeamMemberListView.as_view(), name="api_team_members"),
    path("team-members/pending/", TeamMemberPendingView.as_view(), name="api_team_members_pending"),
    path("team-members/creatable-roles/", CreatableRolesView.as_view(), name="api_creatable_roles"),
    path("team-members/<int:pk>/approve/", TeamMemberApproveView.as_view(), name="api_team_member_approve"),

    # Performance / incentives
    path("performance/", PerformanceView.as_view(), name="api_performance"),

    # Geography (cascading pickers) & villages
    path("geography/", GeographyView.as_view(), name="api_geography"),
    path("villages/", VillageListCreateView.as_view(), name="api_villages"),
    path("villages/<int:pk>/approve/", VillageApproveView.as_view(), name="api_village_approve"),

    # Influencers
    path("influencers/", InfluencerListView.as_view(), name="api_influencers"),

    # Messages
    path("messages/", MessageListView.as_view(), name="api_messages"),
    path("messages/<int:pk>/read/", MessageReadView.as_view(), name="api_message_read"),
    path("messages/<int:pk>/acknowledge/", MessageAcknowledgeView.as_view(), name="api_message_acknowledge"),

    # Ward Profiles
    path("ward-profiles/", WardProfileListView.as_view(), name="api_ward_profiles"),

    # Call Logs
    path("call-logs/", CallLogCreateView.as_view(), name="api_call_logs"),

    # Community Groups
    path("community-groups/", CommunityGroupListCreateView.as_view(), name="api_community_groups"),

    # Polling
    path("polling-locations/", PollingLocationListView.as_view(), name="api_polling_locations"),
    path("polling-status/", PollingStatusCreateView.as_view(), name="api_polling_status"),

    # Intelligence
    path("competitor-activities/", CompetitorActivityCreateView.as_view(), name="api_competitor_activities"),
    path("preference-deals/", PreferenceDealListView.as_view(), name="api_preference_deals"),
    path("registration-drives/", RegistrationDriveListView.as_view(), name="api_registration_drives"),

    # Sync
    path("sync/push/", SyncPushView.as_view(), name="api_sync_push"),
]
