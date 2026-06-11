package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.MessageEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface MessageDao {

    @Query("SELECT * FROM messages ORDER BY sentAt DESC")
    fun getAllFlow(): Flow<List<MessageEntity>>

    @Query("SELECT * FROM messages WHERE isRead = 0 ORDER BY sentAt DESC")
    fun getUnreadFlow(): Flow<List<MessageEntity>>

    @Query("SELECT COUNT(*) FROM messages WHERE isRead = 0")
    fun unreadCountFlow(): Flow<Int>

    @Query("SELECT * FROM messages WHERE localId = :localId")
    suspend fun getByLocalId(localId: String): MessageEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: MessageEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entities: List<MessageEntity>)

    @Query("UPDATE messages SET isRead = 1, readSyncStatus = 'PENDING' WHERE localId = :localId")
    suspend fun markRead(localId: String)

    @Query("UPDATE messages SET isAcknowledged = 1, ackSyncStatus = 'PENDING' WHERE localId = :localId")
    suspend fun markAcknowledged(localId: String)

    @Query("UPDATE messages SET readSyncStatus = 'SYNCED' WHERE localId = :localId")
    suspend fun markReadSynced(localId: String)

    @Query("UPDATE messages SET ackSyncStatus = 'SYNCED' WHERE localId = :localId")
    suspend fun markAckSynced(localId: String)

    @Query("SELECT * FROM messages WHERE readSyncStatus = 'PENDING'")
    suspend fun getPendingReadSync(): List<MessageEntity>

    @Query("SELECT * FROM messages WHERE ackSyncStatus = 'PENDING'")
    suspend fun getPendingAckSync(): List<MessageEntity>
}
