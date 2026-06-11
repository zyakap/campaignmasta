package com.campaignmasta.data.local.entity

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "community_groups",
    indices = [Index("serverId"), Index("syncStatus")]
)
data class CommunityGroupEntity(
    @PrimaryKey val localId: String,
    val serverId: Int? = null,
    val name: String,
    val groupType: String = "OTHER",
    val wardName: String = "",
    val wardId: Int? = null,
    val estimatedVotingMembers: Int? = null,
    val alignment: String = "UNKNOWN",
    val notes: String = "",
    val updatedAt: String = "",
    val syncStatus: String = "SYNCED"
)
