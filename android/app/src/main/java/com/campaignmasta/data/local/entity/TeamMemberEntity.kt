package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "team_members",
    indices = [Index("serverId")]
)
data class TeamMemberEntity(
    @PrimaryKey val localId: String,
    val serverId: Int,
    val fullName: String,
    val gender: String = "",
    val phone: String = "",
    val email: String = "",
    val role: String,
    val wardName: String = "",
    val wardId: Int? = null,
    val isActive: Boolean = true,
    val notes: String = "",
    val updatedAt: String = ""
)
