package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.CommunityGroupEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface CommunityGroupDao {

    @Query("SELECT * FROM community_groups ORDER BY wardName ASC, name ASC")
    fun getAllFlow(): Flow<List<CommunityGroupEntity>>

    @Query("SELECT * FROM community_groups WHERE syncStatus = 'PENDING'")
    suspend fun getPending(): List<CommunityGroupEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entities: List<CommunityGroupEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(entity: CommunityGroupEntity)

    @Query("UPDATE community_groups SET serverId = :serverId, syncStatus = 'SYNCED' WHERE localId = :localId")
    suspend fun markSynced(localId: String, serverId: Int)
}
