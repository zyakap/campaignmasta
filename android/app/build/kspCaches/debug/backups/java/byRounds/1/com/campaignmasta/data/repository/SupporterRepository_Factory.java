package com.campaignmasta.data.repository;

import com.campaignmasta.data.local.dao.SupporterDao;
import com.campaignmasta.data.local.dao.SyncQueueDao;
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
public final class SupporterRepository_Factory implements Factory<SupporterRepository> {
  private final Provider<SupporterDao> supporterDaoProvider;

  private final Provider<SyncQueueDao> syncQueueDaoProvider;

  private final Provider<ApiService> apiServiceProvider;

  private final Provider<UserPreferences> userPreferencesProvider;

  private final Provider<Gson> gsonProvider;

  public SupporterRepository_Factory(Provider<SupporterDao> supporterDaoProvider,
      Provider<SyncQueueDao> syncQueueDaoProvider, Provider<ApiService> apiServiceProvider,
      Provider<UserPreferences> userPreferencesProvider, Provider<Gson> gsonProvider) {
    this.supporterDaoProvider = supporterDaoProvider;
    this.syncQueueDaoProvider = syncQueueDaoProvider;
    this.apiServiceProvider = apiServiceProvider;
    this.userPreferencesProvider = userPreferencesProvider;
    this.gsonProvider = gsonProvider;
  }

  @Override
  public SupporterRepository get() {
    return newInstance(supporterDaoProvider.get(), syncQueueDaoProvider.get(), apiServiceProvider.get(), userPreferencesProvider.get(), gsonProvider.get());
  }

  public static SupporterRepository_Factory create(Provider<SupporterDao> supporterDaoProvider,
      Provider<SyncQueueDao> syncQueueDaoProvider, Provider<ApiService> apiServiceProvider,
      Provider<UserPreferences> userPreferencesProvider, Provider<Gson> gsonProvider) {
    return new SupporterRepository_Factory(supporterDaoProvider, syncQueueDaoProvider, apiServiceProvider, userPreferencesProvider, gsonProvider);
  }

  public static SupporterRepository newInstance(SupporterDao supporterDao,
      SyncQueueDao syncQueueDao, ApiService apiService, UserPreferences userPreferences,
      Gson gson) {
    return new SupporterRepository(supporterDao, syncQueueDao, apiService, userPreferences, gson);
  }
}
