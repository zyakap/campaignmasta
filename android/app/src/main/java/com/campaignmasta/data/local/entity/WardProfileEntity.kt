package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "ward_profiles",
    indices = [Index("serverId")]
)
data class WardProfileEntity(
    @PrimaryKey val localId: String,
    val serverId: Int,
    val wardId: Int,
    val wardName: String,
    val wardNumber: String = "",
    val llgName: String = "",
    val councillorName: String = "",
    val supportStrength: String = "UNKNOWN",
    val populationEstimate: Int? = null,
    val estimatedVotingPopulation: Int? = null,
    val keyClans: String = "",
    val keyChurches: String = "",
    val mainCommunityIssues: String = "",
    val notesForCandidate: String = "",
    val securityConcerns: String = "",
    val updatedAt: String = ""
)
