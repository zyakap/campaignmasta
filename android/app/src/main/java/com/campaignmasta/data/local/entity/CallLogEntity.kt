package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "call_logs",
    indices = [Index("serverId"), Index("syncStatus")]
)
data class CallLogEntity(
    @PrimaryKey val localId: String,
    val serverId: Int? = null,
    val personCalled: String,
    val personType: String = "Influencer",
    val phoneNumber: String = "",
    val callDatetime: String,
    val callOutcome: String = "ANSWERED",
    val discussionSummary: String = "",
    val issuesRaised: String = "",
    val commitmentsMade: String = "",
    val followUpRequired: Boolean = false,
    val followUpDate: String? = null,
    val influencerId: Int? = null,
    val supporterId: Int? = null,
    val callerId: Int? = null,
    val updatedAt: String = "",
    val syncStatus: String = "PENDING",
    val createdLocallyAt: Long = System.currentTimeMillis()
)
