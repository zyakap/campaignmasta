package com.campaignmasta.data.remote.dto

import com.google.gson.annotations.SerializedName

data class LoginRequest(
    val username: String,
    val password: String
)

data class LoginResponse(
    val token: String,
    @SerializedName("user_id") val userId: Int,
    @SerializedName("email") val email: String = "",
    @SerializedName("candidate_id") val candidateId: Int,
    @SerializedName("candidate_name") val candidateName: String,
    @SerializedName("candidate_type") val candidateType: String = "",
    @SerializedName("subscription_plan") val subscriptionPlan: String,
    val role: String,
    @SerializedName("team_member_id") val teamMemberId: Int = 0,
    @SerializedName("full_name") val fullName: String = "",
    val province: String? = null,
    val district: String? = null
)

data class DashboardResponse(
    @SerializedName("supporter_count") val supporterCount: Int,
    @SerializedName("calls_due_count") val callsDueCount: Int,
    @SerializedName("messages_unread_count") val messagesUnreadCount: Int,
    @SerializedName("sync_timestamp") val syncTimestamp: String
)
