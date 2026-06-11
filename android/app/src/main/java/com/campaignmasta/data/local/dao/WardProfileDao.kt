package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.WardProfileEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface WardProfileDao {

    @Query("SELECT * FROM ward_profiles ORDER BY wardName ASC")
    fun getAllFlow(): Flow<List<WardProfileEntity>>

    @Query("SELECT * FROM ward_profiles WHERE localId = :localId")
    suspend fun getByLocalId(localId: String): WardProfileEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entities: List<WardProfileEntity>)

    @Query("DELETE FROM ward_profiles")
    suspend fun deleteAll()
}
