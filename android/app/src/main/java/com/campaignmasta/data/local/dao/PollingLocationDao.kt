package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.PollingLocationEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface PollingLocationDao {

    @Query("SELECT * FROM polling_locations ORDER BY name ASC")
    fun getAllFlow(): Flow<List<PollingLocationEntity>>

    @Query("SELECT * FROM polling_locations WHERE localId = :localId")
    suspend fun getByLocalId(localId: String): PollingLocationEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entities: List<PollingLocationEntity>)

    @Update
    suspend fun update(entity: PollingLocationEntity)

    @Query("UPDATE polling_locations SET ourTally = :tally WHERE localId = :localId")
    suspend fun updateTally(localId: String, tally: Int)

    @Query("DELETE FROM polling_locations")
    suspend fun deleteAll()
}
