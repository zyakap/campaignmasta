package com.campaignmasta.data.remote.dto

import com.google.gson.annotations.SerializedName

/** One selectable role the current user is allowed to create. */
data class CreatableRoleDto(
    val value: String,
    val label: String
)

data class CreatableRolesResponse(
    val results: List<CreatableRoleDto>
)

/** A geography item returned by the cascading /geography/ endpoint. */
data class GeoItemDto(
    val id: Int,
    val name: String,
    val district: Int? = null,
    val llg: Int? = null,
    val ward: Int? = null
)

data class GeoResponse(
    val results: List<GeoItemDto>
)

/** Payload for creating a team member. Geography fields are optional so a
 *  coordinator only sends the levels relevant to the role being created. */
data class CreateTeamMemberRequest(
    @SerializedName("full_name") val fullName: String,
    val role: String,
    val phone: String = "",
    val gender: String = "",
    val district: Int? = null,
    val llg: Int? = null,
    val ward: Int? = null,
    val village: Int? = null,
    val notes: String = ""
)

/** A village awaiting approval (returned by GET /villages/). */
data class VillageDto(
    val id: Int,
    val name: String,
    val ward: Int,
    @SerializedName("ward_name") val wardName: String = "",
    @SerializedName("llg_name") val llgName: String? = null,
    @SerializedName("approval_status") val approvalStatus: String = "PENDING",
    @SerializedName("created_by") val createdBy: String? = null
)

data class VillageListResponse(
    val results: List<VillageDto>,
    val count: Int = 0
)

data class CreateVillageRequest(
    val ward: Int,
    val name: String
)

/** Body for approve/reject actions (reject=true to reject). */
data class ApprovalActionRequest(
    val reject: Boolean = false
)

/** Incentive numbers for the signed-in member. */
data class MePerformanceDto(
    @SerializedName("supporters_registered") val supportersRegistered: Int = 0,
    @SerializedName("team_total") val teamTotal: Int = 0,
    @SerializedName("volunteers_created") val volunteersCreated: Int = 0
)

data class LeaderboardEntryDto(
    val id: Int,
    @SerializedName("full_name") val fullName: String,
    val role: String = "",
    @SerializedName("role_display") val roleDisplay: String = "",
    val count: Int = 0
)

data class PerformanceResponse(
    val me: MePerformanceDto = MePerformanceDto(),
    val leaderboard: List<LeaderboardEntryDto> = emptyList()
)
