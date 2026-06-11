package com.campaignmasta.ui.screens.calls;

import com.campaignmasta.data.local.dao.CallLogDao;
import com.campaignmasta.data.local.dao.InfluencerDao;
import com.campaignmasta.data.local.dao.SyncQueueDao;
import com.google.gson.Gson;
import dagger.internal.DaggerGenerated;
import dagger.internal.Factory;
import dagger.internal.QualifierMetadata;
import dagger.internal.ScopeMetadata;
import javax.annotation.processing.Generated;
import javax.inject.Provider;

@ScopeMetadata
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
public final class CallViewModel_Factory implements Factory<CallViewModel> {
  private final Provider<InfluencerDao> influencerDaoProvider;

  private final Provider<CallLogDao> callLogDaoProvider;

  private final Provider<SyncQueueDao> syncQueueDaoProvider;

  private final Provider<Gson> gsonProvider;

  public CallViewModel_Factory(Provider<InfluencerDao> influencerDaoProvider,
      Provider<CallLogDao> callLogDaoProvider, Provider<SyncQueueDao> syncQueueDaoProvider,
      Provider<Gson> gsonProvider) {
    this.influencerDaoProvider = influencerDaoProvider;
    this.callLogDaoProvider = callLogDaoProvider;
    this.syncQueueDaoProvider = syncQueueDaoProvider;
    this.gsonProvider = gsonProvider;
  }

  @Override
  public CallViewModel get() {
    return newInstance(influencerDaoProvider.get(), callLogDaoProvider.get(), syncQueueDaoProvider.get(), gsonProvider.get());
  }

  public static CallViewModel_Factory create(Provider<InfluencerDao> influencerDaoProvider,
      Provider<CallLogDao> callLogDaoProvider, Provider<SyncQueueDao> syncQueueDaoProvider,
      Provider<Gson> gsonProvider) {
    return new CallViewModel_Factory(influencerDaoProvider, callLogDaoProvider, syncQueueDaoProvider, gsonProvider);
  }

  public static CallViewModel newInstance(InfluencerDao influencerDao, CallLogDao callLogDao,
      SyncQueueDao syncQueueDao, Gson gson) {
    return new CallViewModel(influencerDao, callLogDao, syncQueueDao, gson);
  }
}
