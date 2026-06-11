package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "messages",
    indices = [Index("serverId")]
)
data class MessageEntity(
    @PrimaryKey val localId: String,
    val serverId: Int? = null,
    val subject: String,
    val body: String,
    val messageType: String = "STANDARD",
    val priority: String = "NORMAL",
    val senderName: String = "",
    val deliveryChannel: String = "IN_APP",
    val status: String = "SENT",
    val sentAt: String? = null,
    val isRead: Boolean = false,
    val isAcknowledged: Boolean = false,
    val readReceiptRequired: Boolean = false,
    val acknowledgementRequired: Boolean = false,
    val updatedAt: String = "",
    val readSyncStatus: String = "SYNCED",    // PENDING when read/ack needs sync
    val ackSyncStatus: String = "SYNCED"
)
