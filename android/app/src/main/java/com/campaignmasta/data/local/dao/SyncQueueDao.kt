package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.SyncQueueEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface SyncQueueDao {

    @Query("SELECT * FROM sync_queue WHERE status = 'PENDING' AND retryCount < 5 ORDER BY createdAt ASC")
    suspend fun getPending(): List<SyncQueueEntity>

    @Query("SELECT COUNT(*) FROM sync_queue WHERE status = 'PENDING'")
    fun pendingCountFlow(): Flow<Int>

    @Query("SELECT COUNT(*) FROM sync_queue WHERE status = 'PENDING'")
    suspend fun pendingCount(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: SyncQueueEntity): Long

    @Query("UPDATE sync_queue SET status = 'IN_FLIGHT' WHERE id = :id")
    suspend fun markInFlight(id: Long)

    @Query("UPDATE sync_queue SET status = 'DONE' WHERE id = :id")
    suspend fun markDone(id: Long)

    @Query("UPDATE sync_queue SET status = 'FAILED', retryCount = retryCount + 1, lastError = :error WHERE id = :id")
    suspend fun markFailed(id: Long, error: String)

    @Query("UPDATE sync_queue SET status = 'PENDING', retryCount = retryCount + 1 WHERE id = :id")
    suspend fun markPendingRetry(id: Long)

    @Query("DELETE FROM sync_queue WHERE status = 'DONE'")
    suspend fun clearCompleted()

    @Query("DELETE FROM sync_queue WHERE id = :id")
    suspend fun delete(id: Long)
}
