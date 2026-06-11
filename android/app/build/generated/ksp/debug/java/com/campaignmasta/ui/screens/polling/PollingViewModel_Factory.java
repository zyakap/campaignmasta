package com.campaignmasta.ui.screens.polling;

import com.campaignmasta.data.local.dao.PollingLocationDao;
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
public final class PollingViewModel_Factory implements Factory<PollingViewModel> {
  private final Provider<PollingLocationDao> pollingLocationDaoProvider;

  private final Provider<SyncQueueDao> syncQueueDaoProvider;

  private final Provider<Gson> gsonProvider;

  public PollingViewModel_Factory(Provider<PollingLocationDao> pollingLocationDaoProvider,
      Provider<SyncQueueDao> syncQueueDaoProvider, Provider<Gson> gsonProvider) {
    this.pollingLocationDaoProvider = pollingLocationDaoProvider;
    this.syncQueueDaoProvider = syncQueueDaoProvider;
    this.gsonProvider = gsonProvider;
  }

  @Override
  public PollingViewModel get() {
    return newInstance(pollingLocationDaoProvider.get(), syncQueueDaoProvider.get(), gsonProvider.get());
  }

  public static PollingViewModel_Factory create(
      Provider<PollingLocationDao> pollingLocationDaoProvider,
      Provider<SyncQueueDao> syncQueueDaoProvider, Provider<Gson> gsonProvider) {
    return new PollingViewModel_Factory(pollingLocationDaoProvider, syncQueueDaoProvider, gsonProvider);
  }

  public static PollingViewModel newInstance(PollingLocationDao pollingLocationDao,
      SyncQueueDao syncQueueDao, Gson gson) {
    return new PollingViewModel(pollingLocationDao, syncQueueDao, gson);
  }
}
