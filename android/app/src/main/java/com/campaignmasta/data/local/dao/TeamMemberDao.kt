package com.campaignmasta.data.local.dao

import androidx.room.*
import com.campaignmasta.data.local.entity.TeamMemberEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface TeamMemberDao {

    @Query("SELECT * FROM team_members WHERE isActive = 1 ORDER BY fullName ASC")
    fun getAllActiveFlow(): Flow<List<TeamMemberEntity>>

    @Query("SELECT * FROM team_members ORDER BY fullName ASC")
    suspend fun getAll(): List<TeamMemberEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entities: List<TeamMemberEntity>)

    @Query("DELETE FROM team_members")
    suspend fun deleteAll()

    @Query("SELECT COUNT(*) FROM team_members")
    suspend fun count(): Int
}
