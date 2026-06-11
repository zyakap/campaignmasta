package com.campaignmasta.data.remote.dto

import com.google.gson.annotations.SerializedName

data class WardProfileDto(
    val id: Int,
    val ward: Int,
    @SerializedName("ward_name") val wardName: String = "",
    @SerializedName("ward_number") val wardNumber: String = "",
    @SerializedName("llg_name") val llgName: String = "",
    @SerializedName("councillor_name") val councillorName: String = "",
    @SerializedName("support_strength") val supportStrength: String = "UNKNOWN",
    @SerializedName("population_estimate") val populationEstimate: Int? = null,
    @SerializedName("estimated_voting_population") val estimatedVotingPopulation: Int? = null,
    @SerializedName("key_clans") val keyClans: String = "",
    @SerializedName("key_churches") val keyChurches: String = "",
    @SerializedName("main_community_issues") val mainCommunityIssues: String = "",
    @SerializedName("notes_for_candidate") val notesForCandidate: String = "",
    @SerializedName("security_concerns") val securityConcerns: String = "",
    @SerializedName("updated_at") val updatedAt: String = ""
)

data class TeamMemberDto(
    val id: Int,
    @SerializedName("full_name") val fullName: String,
    val gender: String = "",
    val phone: String = "",
    val email: String = "",
    val role: String = "",
    @SerializedName("ward_name") val wardName: String = "",
    val ward: Int? = null,
    @SerializedName("is_active") val isActive: Boolean = true,
    val notes: String = "",
    @SerializedName("updated_at") val updatedAt: String = ""
)

data class InfluencerDto(
    val id: Int,
    @SerializedName("full_name") val fullName: String,
    val phone: String = "",
    @SerializedName("community_role") val communityRole: String = "",
    @SerializedName("influence_level") val influenceLevel: String = "MEDIUM",
    @SerializedName("relationship_status") val relationshipStatus: String = "UNKNOWN",
    @SerializedName("contact_frequency_days") val contactFrequencyDays: Int = 14,
    @SerializedName("last_call_date") val lastCallDate: String? = null,
    @SerializedName("next_contact_due_date") val nextContactDueDate: String? = null,
    @SerializedName("ward_name") val wardName: String = "",
    val ward: Int? = null,
    val notes: String = "",
    @SerializedName("updated_at") val updatedAt: String = ""
)
