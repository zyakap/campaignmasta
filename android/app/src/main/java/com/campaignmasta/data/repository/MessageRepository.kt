package com.campaignmasta.data.repository

import com.campaignmasta.data.local.dao.MessageDao
import com.campaignmasta.data.local.entity.MessageEntity
import com.campaignmasta.data.preferences.UserPreferences
import com.campaignmasta.data.remote.ApiService
import com.campaignmasta.data.remote.dto.MessageDto
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class MessageRepository @Inject constructor(
    private val messageDao: MessageDao,
    private val apiService: ApiService,
    private val userPreferences: UserPreferences
) {
    val messages: Flow<List<MessageEntity>> = messageDao.getAllFlow()
    val unreadCount: Flow<Int> = messageDao.unreadCountFlow()

    suspend fun markReadLocally(localId: String) {
        messageDao.markRead(localId)
    }

    suspend fun markAcknowledgedLocally(localId: String) {
        messageDao.markAcknowledged(localId)
    }

    /** Push pending read receipts and acks to server. */
    suspend fun pushReadAcks(): Boolean {
        return try {
            val pendingRead = messageDao.getPendingReadSync()
            for (msg in pendingRead) {
                val serverId = msg.serverId ?: continue
                val resp = apiService.markMessageRead(serverId)
                if (resp.isSuccessful) {
                    messageDao.markReadSynced(msg.localId)
                }
            }
            val pendingAck = messageDao.getPendingAckSync()
            for (msg in pendingAck) {
                val serverId = msg.serverId ?: continue
                val resp = apiService.acknowledgeMessage(serverId)
                if (resp.isSuccessful) {
                    messageDao.markAckSynced(msg.localId)
                }
            }
            true
        } catch (e: Exception) {
            false
        }
    }

    /** Pull messages from server and upsert locally. */
    suspend fun pullFromServer(): Boolean {
        return try {
            val updatedAfter = userPreferences.lastSyncMessages.first()
            val response = apiService.getMessages(updatedAfter = updatedAfter)
            if (response.isSuccessful) {
                val body = response.body() ?: return false
                val entities = body.results.map { it.toEntity() }
                messageDao.insertAll(entities)
                val now = java.time.Instant.now().toString()
                userPreferences.updateLastSync(UserPreferences.LAST_SYNC_MESSAGES, now)
                true
            } else {
                false
            }
        } catch (e: Exception) {
            false
        }
    }
}

fun MessageDto.toEntity(): MessageEntity = MessageEntity(
    localId = "server_$id",
    serverId = id,
    subject = subject,
    body = body,
    messageType = messageType,
    priority = priority,
    senderName = senderName,
    deliveryChannel = deliveryChannel,
    status = status,
    sentAt = sentAt,
    isRead = isRead,
    isAcknowledged = isAcknowledged,
    readReceiptRequired = readReceiptRequired,
    acknowledgementRequired = acknowledgementRequired,
    updatedAt = updatedAt,
    readSyncStatus = "SYNCED",
    ackSyncStatus = "SYNCED"
)
