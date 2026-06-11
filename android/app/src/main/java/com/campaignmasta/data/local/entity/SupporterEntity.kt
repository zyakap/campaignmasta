package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "supporters",
    indices = [Index("serverId"), Index("syncStatus")]
)
data class SupporterEntity(
    @PrimaryKey val localId: String,          // UUID generated on device
    val serverId: Int? = null,                // null until synced
    val fullName: String,
    val gender: String = "",
    val ageRange: String = "",
    val phone: String = "",
    val ward: String = "",                    // ward name for display
    val wardId: Int? = null,
    val village: String = "",
    val villageId: Int? = null,
    val clan: String = "",
    val enrollmentStatus: String = "UNKNOWN",
    val supportStatus: String = "UNKNOWN",
    val notes: String = "",
    val followUpRequired: Boolean = false,
    val followUpDate: String? = null,
    val consentToMessages: Boolean = false,
    val updatedAt: String = "",
    val syncStatus: String = "PENDING",       // PENDING / SYNCED / FAILED
    val createdLocallyAt: Long = System.currentTimeMillis()
)
