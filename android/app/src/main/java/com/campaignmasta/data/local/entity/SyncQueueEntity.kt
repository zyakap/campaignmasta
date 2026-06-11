package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "sync_queue",
    indices = [Index("status"), Index("entityType")]
)
data class SyncQueueEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val entityType: String,                   // supporter, call_log, polling_status, etc.
    val operation: String,                    // CREATE, UPDATE, DELETE
    val serverId: Int? = null,                // null for CREATE
    val localId: String,                      // UUID to correlate with local record
    val payload: String,                      // JSON string of entity fields
    val createdAt: Long = System.currentTimeMillis(),
    val status: String = "PENDING",           // PENDING, IN_FLIGHT, FAILED, DONE
    val retryCount: Int = 0,
    val lastError: String = ""
)
