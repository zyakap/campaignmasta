package com.campaignmasta.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import androidx.room.TypeConverters
import com.campaignmasta.data.local.dao.*
import com.campaignmasta.data.local.entity.*

@Database(
    entities = [
        SupporterEntity::class,
        CallLogEntity::class,
        MessageEntity::class,
        TeamMemberEntity::class,
        InfluencerEntity::class,
        WardProfileEntity::class,
        CommunityGroupEntity::class,
        PollingLocationEntity::class,
        SyncQueueEntity::class,
    ],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class AppDatabase : RoomDatabase() {
    abstract fun supporterDao(): SupporterDao
    abstract fun callLogDao(): CallLogDao
    abstract fun messageDao(): MessageDao
    abstract fun teamMemberDao(): TeamMemberDao
    abstract fun influencerDao(): InfluencerDao
    abstract fun wardProfileDao(): WardProfileDao
    abstract fun communityGroupDao(): CommunityGroupDao
    abstract fun pollingLocationDao(): PollingLocationDao
    abstract fun syncQueueDao(): SyncQueueDao
}
