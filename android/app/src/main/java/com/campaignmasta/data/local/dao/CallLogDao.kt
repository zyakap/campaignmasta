package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.CallLogEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface CallLogDao {

    @Query("SELECT * FROM call_logs ORDER BY callDatetime DESC")
    fun getAllFlow(): Flow<List<CallLogEntity>>

    @Query("SELECT * FROM call_logs WHERE syncStatus = 'PENDING' ORDER BY createdLocallyAt ASC")
    suspend fun getPending(): List<CallLogEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: CallLogEntity)

    @Query("UPDATE call_logs SET serverId = :serverId, syncStatus = 'SYNCED' WHERE localId = :localId")
    suspend fun markSynced(localId: String, serverId: Int)

    @Query("UPDATE call_logs SET syncStatus = 'FAILED' WHERE localId = :localId")
    suspend fun markFailed(localId: String)

    @Query("SELECT COUNT(*) FROM call_logs")
    suspend fun count(): Int
}
