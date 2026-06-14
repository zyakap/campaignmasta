package com.campaignmasta.data.remote

import com.campaignmasta.data.remote.dto.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    // ── Auth ──────────────────────────────────────────────────────────────────

    @POST("api/auth/login/")
    suspend fun login(@Body request: LoginRequest): Response<LoginResponse>

    // ── Dashboard ─────────────────────────────────────────────────────────────

    @GET("api/dashboard/")
    suspend fun getDashboard(): Response<DashboardResponse>

    // ── Supporters ────────────────────────────────────────────────────────────

    @GET("api/supporters/")
    suspend fun getSupporters(
        @Query("updated_after") updatedAfter: String? = null,
        @Query("page") page: Int = 1
    ): Response<PaginatedResponse<SupporterDto>>

    @POST("api/supporters/")
    suspend fun createSupporter(@Body request: Map<String, Any?>): Response<SupporterDto>

    // ── Team Members & hierarchy ──────────────────────────────────────────────

    @GET("api/team-members/")
    suspend fun getTeamMembers(
        @Query("updated_after") updatedAfter: String? = null
    ): Response<ListResponse<TeamMemberDto>>

    @POST("api/team-members/")
    suspend fun createTeamMember(@Body request: CreateTeamMemberRequest): Response<TeamMemberDto>

    @GET("api/team-members/pending/")
    suspend fun getPendingTeamMembers(): Response<ListResponse<TeamMemberDto>>

    @GET("api/team-members/creatable-roles/")
    suspend fun getCreatableRoles(): Response<CreatableRolesResponse>

    @POST("api/team-members/{id}/approve/")
    suspend fun approveTeamMember(
        @Path("id") id: Int,
        @Body request: ApprovalActionRequest
    ): Response<TeamMemberDto>

    // ── Geography (cascading pickers) ─────────────────────────────────────────

    @GET("api/geography/")
    suspend fun getGeography(
        @Query("level") level: String,
        @Query("parent") parent: Int? = null
    ): Response<GeoResponse>

    // ── Villages (create on request + approval) ───────────────────────────────

    @GET("api/villages/")
    suspend fun getPendingVillages(): Response<VillageListResponse>

    @POST("api/villages/")
    suspend fun createVillage(@Body request: CreateVillageRequest): Response<VillageDto>

    @POST("api/villages/{id}/approve/")
    suspend fun approveVillage(
        @Path("id") id: Int,
        @Body request: ApprovalActionRequest
    ): Response<Map<String, Any?>>

    // ── Influencers ───────────────────────────────────────────────────────────

    @GET("api/influencers/")
    suspend fun getInfluencers(
        @Query("updated_after") updatedAfter: String? = null
    ): Response<ListResponse<InfluencerDto>>

    // ── Messages ──────────────────────────────────────────────────────────────

    @GET("api/messages/")
    suspend fun getMessages(
        @Query("updated_after") updatedAfter: String? = null
    ): Response<ListResponse<MessageDto>>

    @POST("api/messages/{id}/read/")
    suspend fun markMessageRead(@Path("id") id: Int): Response<Map<String, String>>

    @POST("api/messages/{id}/acknowledge/")
    suspend fun acknowledgeMessage(@Path("id") id: Int): Response<Map<String, String>>

    // ── Ward Profiles ─────────────────────────────────────────────────────────

    @GET("api/ward-profiles/")
    suspend fun getWardProfiles(
        @Query("updated_after") updatedAfter: String? = null
    ): Response<ListResponse<WardProfileDto>>

    // ── Call Logs ─────────────────────────────────────────────────────────────

    @POST("api/call-logs/")
    suspend fun createCallLog(@Body request: Map<String, Any?>): Response<Map<String, Any>>

    // ── Community Groups ──────────────────────────────────────────────────────

    @GET("api/community-groups/")
    suspend fun getCommunityGroups(
        @Query("updated_after") updatedAfter: String? = null
    ): Response<ListResponse<CommunityGroupDto>>

    @POST("api/community-groups/")
    suspend fun createCommunityGroup(@Body request: Map<String, Any?>): Response<CommunityGroupDto>

    // ── Polling ───────────────────────────────────────────────────────────────

    @GET("api/polling-locations/")
    suspend fun getPollingLocations(
        @Query("updated_after") updatedAfter: String? = null
    ): Response<ListResponse<PollingLocationDto>>

    @POST("api/polling-status/")
    suspend fun createPollingStatus(@Body request: Map<String, Any?>): Response<Map<String, Any>>

    // ── Intelligence ──────────────────────────────────────────────────────────

    @POST("api/competitor-activities/")
    suspend fun createCompetitorActivity(@Body request: Map<String, Any?>): Response<Map<String, Any>>

    @GET("api/preference-deals/")
    suspend fun getPreferenceDeals(
        @Query("updated_after") updatedAfter: String? = null
    ): Response<ListResponse<PreferenceDealDto>>

    @GET("api/registration-drives/")
    suspend fun getRegistrationDrives(
        @Query("updated_after") updatedAfter: String? = null
    ): Response<ListResponse<RegistrationDriveDto>>

    // ── Batch Sync ────────────────────────────────────────────────────────────

    @POST("api/sync/push/")
    suspend fun syncPush(@Body request: SyncPushRequest): Response<SyncPushResponse>
}
