package com.campaignmasta.data.repository;

import com.campaignmasta.data.local.dao.CallLogDao;
import com.campaignmasta.data.local.dao.CommunityGroupDao;
import com.campaignmasta.data.local.dao.InfluencerDao;
import com.campaignmasta.data.local.dao.MessageDao;
import com.campaignmasta.data.local.dao.PollingLocationDao;
import com.campaignmasta.data.local.dao.SupporterDao;
import com.campaignmasta.data.local.dao.SyncQueueDao;
import com.campaignmasta.data.local.dao.TeamMemberDao;
import com.campaignmasta.data.local.dao.WardProfileDao;
import com.campaignmasta.data.preferences.UserPreferences;
import com.campaignmasta.data.remote.ApiService;
import com.google.gson.Gson;
import dagger.internal.DaggerGenerated;
import dagger.internal.Factory;
import dagger.internal.QualifierMetadata;
import dagger.internal.ScopeMetadata;
import javax.annotation.processing.Generated;
import javax.inject.Provider;

@ScopeMetadata("javax.inject.Singleton")
@QualifierMetadata
@DaggerGenerated
@Generated(
    value = "dagger.internal.codegen.ComponentProcessor",
    comments = "https://dagger.dev"
)
@SuppressWarnings({
    "unchecked",
    "rawtypes",
    "KotlinInternal",
    "KotlinInternalInJava",
    "cast"
})
public final class SyncRepository_Factory implements Factory<SyncRepository> {
  private final Provider<SyncQueueDao> syncQueueDaoProvider;

  private final Provider<SupporterDao> supporterDaoProvider;

  private final Provider<CallLogDao> callLogDaoProvider;

  private final Provider<TeamMemberDao> teamMemberDaoProvider;

  private final Provider<InfluencerDao> influencerDaoProvider;

  private final Provider<WardProfileDao> wardProfileDaoProvider;

  private final Provider<CommunityGroupDao> communityGroupDaoProvider;

  private final Provider<PollingLocationDao> pollingLocationDaoProvider;

  private final Provider<MessageDao> messageDaoProvider;

  private final Provider<ApiService> apiServiceProvider;

  private final Provider<UserPreferences> userPreferencesProvider;

  private final Provider<Gson> gsonProvider;

  public SyncRepository_Factory(Provider<SyncQueueDao> syncQueueDaoProvider,
      Provider<SupporterDao> supporterDaoProvider, Provider<CallLogDao> callLogDaoProvider,
      Provider<TeamMemberDao> teamMemberDaoProvider, Provider<InfluencerDao> influencerDaoProvider,
      Provider<WardProfileDao> wardProfileDaoProvider,
      Provider<CommunityGroupDao> communityGroupDaoProvider,
      Provider<PollingLocationDao> pollingLocationDaoProvider,
      Provider<MessageDao> messageDaoProvider, Provider<ApiService> apiServiceProvider,
      Provider<UserPreferences> userPreferencesProvider, Provider<Gson> gsonProvider) {
    this.syncQueueDaoProvider = syncQueueDaoProvider;
    this.supporterDaoProvider = supporterDaoProvider;
    this.callLogDaoProvider = callLogDaoProvider;
    this.teamMemberDaoProvider = teamMemberDaoProvider;
    this.influencerDaoProvider = influencerDaoProvider;
    this.wardProfileDaoProvider = wardProfileDaoProvider;
    this.communityGroupDaoProvider = communityGroupDaoProvider;
    this.pollingLocationDaoProvider = pollingLocationDaoProvider;
    this.messageDaoProvider = messageDaoProvider;
    this.apiServiceProvider = apiServiceProvider;
    this.userPreferencesProvider = userPreferencesProvider;
    this.gsonProvider = gsonProvider;
  }

  @Override
  public SyncRepository get() {
    return newInstance(syncQueueDaoProvider.get(), supporterDaoProvider.get(), callLogDaoProvider.get(), teamMemberDaoProvider.get(), influencerDaoProvider.get(), wardProfileDaoProvider.get(), communityGroupDaoProvider.get(), pollingLocationDaoProvider.get(), messageDaoProvider.get(), apiServiceProvider.get(), userPreferencesProvider.get(), gsonProvider.get());
  }

  public static SyncRepository_Factory create(Provider<SyncQueueDao> syncQueueDaoProvider,
      Provider<SupporterDao> supporterDaoProvider, Provider<CallLogDao> callLogDaoProvider,
      Provider<TeamMemberDao> teamMemberDaoProvider, Provider<InfluencerDao> influencerDaoProvider,
      Provider<WardProfileDao> wardProfileDaoProvider,
      Provider<CommunityGroupDao> communityGroupDaoProvider,
      Provider<PollingLocationDao> pollingLocationDaoProvider,
      Provider<MessageDao> messageDaoProvider, Provider<ApiService> apiServiceProvider,
      Provider<UserPreferences> userPreferencesProvider, Provider<Gson> gsonProvider) {
    return new SyncRepository_Factory(syncQueueDaoProvider, supporterDaoProvider, callLogDaoProvider, teamMemberDaoProvider, influencerDaoProvider, wardProfileDaoProvider, communityGroupDaoProvider, pollingLocationDaoProvider, messageDaoProvider, apiServiceProvider, userPreferencesProvider, gsonProvider);
  }

  public static SyncRepository newInstance(SyncQueueDao syncQueueDao, SupporterDao supporterDao,
      CallLogDao callLogDao, TeamMemberDao teamMemberDao, InfluencerDao influencerDao,
      WardProfileDao wardProfileDao, CommunityGroupDao communityGroupDao,
      PollingLocationDao pollingLocationDao, MessageDao messageDao, ApiService apiService,
      UserPreferences userPreferences, Gson gson) {
    return new SyncRepository(syncQueueDao, supporterDao, callLogDao, teamMemberDao, influencerDao, wardProfileDao, communityGroupDao, pollingLocationDao, messageDao, apiService, userPreferences, gson);
  }
}
