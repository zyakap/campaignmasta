package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "influencers",
    indices = [Index("serverId")]
)
data class InfluencerEntity(
    @PrimaryKey val localId: String,
    val serverId: Int,
    val fullName: String,
    val phone: String = "",
    val communityRole: String = "",
    val influenceLevel: String = "MEDIUM",
    val relationshipStatus: String = "UNKNOWN",
    val contactFrequencyDays: Int = 14,
    val lastCallDate: String? = null,
    val nextContactDueDate: String? = null,
    val wardName: String = "",
    val wardId: Int? = null,
    val notes: String = "",
    val updatedAt: String = ""
)
