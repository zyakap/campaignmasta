package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.SupporterEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface SupporterDao {

    @Query("SELECT * FROM supporters ORDER BY fullName ASC")
    fun getAllFlow(): Flow<List<SupporterEntity>>

    @Query("SELECT * FROM supporters WHERE syncStatus = 'PENDING' ORDER BY createdLocallyAt ASC")
    suspend fun getPending(): List<SupporterEntity>

    @Query("SELECT * FROM supporters WHERE localId = :localId")
    suspend fun getByLocalId(localId: String): SupporterEntity?

    @Query("SELECT * FROM supporters WHERE localId = :localId")
    fun observeByLocalId(localId: String): Flow<SupporterEntity?>

    @Query("SELECT * FROM supporters WHERE serverId = :serverId")
    suspend fun getByServerId(serverId: Int): SupporterEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: SupporterEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entities: List<SupporterEntity>)

    @Update
    suspend fun update(entity: SupporterEntity)

    @Query("UPDATE supporters SET serverId = :serverId, syncStatus = 'SYNCED' WHERE localId = :localId")
    suspend fun markSynced(localId: String, serverId: Int)

    @Query("UPDATE supporters SET syncStatus = 'FAILED' WHERE localId = :localId")
    suspend fun markFailed(localId: String)

    @Query("SELECT COUNT(*) FROM supporters")
    suspend fun count(): Int

    @Query("DELETE FROM supporters WHERE localId = :localId")
    suspend fun delete(localId: String)
}
