package com.campaignmasta.data.remote.dto

import com.google.gson.annotations.SerializedName

data class LoginRequest(
    val username: String,
    val password: String
)

data class LoginResponse(
    val token: String,
    @SerializedName("user_id") val userId: Int,
    @SerializedName("candidate_id") val candidateId: Int,
    @SerializedName("candidate_name") val candidateName: String,
    @SerializedName("subscription_plan") val subscriptionPlan: String,
    val role: String
)

data class DashboardResponse(
    @SerializedName("supporter_count") val supporterCount: Int,
    @SerializedName("calls_due_count") val callsDueCount: Int,
    @SerializedName("messages_unread_count") val messagesUnreadCount: Int,
    @SerializedName("sync_timestamp") val syncTimestamp: String
)
