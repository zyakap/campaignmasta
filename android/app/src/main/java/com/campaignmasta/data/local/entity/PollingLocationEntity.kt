package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "polling_locations",
    indices = [Index("serverId")]
)
data class PollingLocationEntity(
    @PrimaryKey val localId: String,
    val serverId: Int,
    val name: String,
    val wardName: String = "",
    val wardId: Int? = null,
    val gpsCoordinates: String = "",
    val scrutineerName: String = "",
    val scrutineerCheckedIn: Boolean = false,
    val securityRisk: String = "LOW",
    val expectedTurnout: Int? = null,
    val status: String = "Pending",
    val notes: String = "",
    val ourTally: Int? = null,
    val updatedAt: String = ""
)
