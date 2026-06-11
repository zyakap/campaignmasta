package com.campaignmasta.data.remote.dto

import com.google.gson.annotations.SerializedName

data class SupporterDto(
    val id: Int,
    @SerializedName("full_name") val fullName: String,
    val gender: String = "",
    @SerializedName("age_range") val ageRange: String = "",
    val phone: String = "",
    val ward: Int? = null,
    @SerializedName("ward_name") val wardName: String = "",
    val village: Int? = null,
    @SerializedName("village_name") val villageName: String = "",
    val clan: String = "",
    @SerializedName("enrollment_status") val enrollmentStatus: String = "UNKNOWN",
    @SerializedName("support_status") val supportStatus: String = "UNKNOWN",
    @SerializedName("influence_level") val influenceLevel: String = "LOW",
    @SerializedName("follow_up_required") val followUpRequired: Boolean = false,
    @SerializedName("follow_up_date") val followUpDate: String? = null,
    @SerializedName("consent_to_messages") val consentToMessages: Boolean = false,
    val notes: String = "",
    @SerializedName("updated_at") val updatedAt: String = ""
)

data class CreateSupporterRequest(
    @SerializedName("full_name") val fullName: String,
    val gender: String = "",
    val phone: String = "",
    val ward: Int? = null,
    val village: Int? = null,
    val clan: String = "",
    @SerializedName("enrollment_status") val enrollmentStatus: String = "UNKNOWN",
    @SerializedName("support_status") val supportStatus: String = "UNKNOWN",
    val notes: String = "",
    val province: Int
)
