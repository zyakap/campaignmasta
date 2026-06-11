package com.campaignmasta.di

import android.content.Context
import androidx.room.Room
import com.campaignmasta.data.local.AppDatabase
import com.campaignmasta.data.local.dao.*
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase =
        Room.databaseBuilder(context, AppDatabase::class.java, "campaignmasta.db")
            .fallbackToDestructiveMigration()
            .build()

    @Provides fun supporterDao(db: AppDatabase): SupporterDao = db.supporterDao()
    @Provides fun callLogDao(db: AppDatabase): CallLogDao = db.callLogDao()
    @Provides fun messageDao(db: AppDatabase): MessageDao = db.messageDao()
    @Provides fun teamMemberDao(db: AppDatabase): TeamMemberDao = db.teamMemberDao()
    @Provides fun influencerDao(db: AppDatabase): InfluencerDao = db.influencerDao()
    @Provides fun wardProfileDao(db: AppDatabase): WardProfileDao = db.wardProfileDao()
    @Provides fun communityGroupDao(db: AppDatabase): CommunityGroupDao = db.communityGroupDao()
    @Provides fun pollingLocationDao(db: AppDatabase): PollingLocationDao = db.pollingLocationDao()
    @Provides fun syncQueueDao(db: AppDatabase): SyncQueueDao = db.syncQueueDao()
}
