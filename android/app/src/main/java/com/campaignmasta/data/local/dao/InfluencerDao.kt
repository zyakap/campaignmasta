package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.InfluencerEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface InfluencerDao {

    @Query("SELECT * FROM influencers ORDER BY fullName ASC")
    fun getAllFlow(): Flow<List<InfluencerEntity>>

    @Query("SELECT * FROM influencers WHERE nextContactDueDate <= :today ORDER BY nextContactDueDate ASC")
    fun getDueFlow(today: String): Flow<List<InfluencerEntity>>

    @Query("SELECT COUNT(*) FROM influencers WHERE nextContactDueDate <= :today")
    suspend fun countDue(today: String): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entities: List<InfluencerEntity>)

    @Query("DELETE FROM influencers")
    suspend fun deleteAll()
}
