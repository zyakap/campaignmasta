package com.campaignmasta.data.remote.dto

import com.google.gson.annotations.SerializedName

data class PollingLocationDto(
    val id: Int,
    val name: String,
    @SerializedName("ward_name") val wardName: String = "",
    val ward: Int? = null,
    @SerializedName("gps_coordinates") val gpsCoordinates: String = "",
    @SerializedName("scrutineer_name") val scrutineerName: String = "",
    @SerializedName("assigned_scrutineer") val assignedScrutineer: Int? = null,
    @SerializedName("scrutineer_checked_in") val scrutineerCheckedIn: Boolean = false,
    @SerializedName("security_risk") val securityRisk: String = "LOW",
    @SerializedName("expected_turnout") val expectedTurnout: Int? = null,
    val status: String = "Pending",
    val notes: String = "",
    @SerializedName("updated_at") val updatedAt: String = ""
)

data class CommunityGroupDto(
    val id: Int,
    val name: String,
    @SerializedName("group_type") val groupType: String = "OTHER",
    @SerializedName("ward_name") val wardName: String = "",
    val ward: Int? = null,
    @SerializedName("estimated_voting_members") val estimatedVotingMembers: Int? = null,
    val alignment: String = "UNKNOWN",
    val notes: String = "",
    @SerializedName("updated_at") val updatedAt: String = ""
)

data class PreferenceDealDto(
    val id: Int,
    @SerializedName("partner_candidate_name") val partnerCandidateName: String,
    @SerializedName("partner_party") val partnerParty: String = "",
    @SerializedName("partner_seat") val partnerSeat: String = "",
    @SerializedName("preference_number") val preferenceNumber: Int = 2,
    val status: String = "VERBAL",
    @SerializedName("ward_directives") val wardDirectives: String = "",
    val notes: String = "",
    @SerializedName("updated_at") val updatedAt: String = ""
)

data class RegistrationDriveDto(
    val id: Int,
    val title: String,
    @SerializedName("ward_name") val wardName: String = "",
    @SerializedName("start_date") val startDate: String = "",
    @SerializedName("end_date") val endDate: String? = null,
    @SerializedName("target_count") val targetCount: Int = 0,
    @SerializedName("actual_count") val actualCount: Int = 0,
    val status: String = "PLANNED",
    val notes: String = "",
    @SerializedName("updated_at") val updatedAt: String = ""
)
