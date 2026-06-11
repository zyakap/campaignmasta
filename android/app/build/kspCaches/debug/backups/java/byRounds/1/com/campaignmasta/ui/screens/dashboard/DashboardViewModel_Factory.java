package com.campaignmasta.ui.screens.dashboard;

import com.campaignmasta.data.preferences.UserPreferences;
import com.campaignmasta.data.remote.ApiService;
import com.campaignmasta.data.repository.AuthRepository;
import com.campaignmasta.data.repository.SupporterRepository;
import com.campaignmasta.data.repository.SyncRepository;
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
public final class DashboardViewModel_Factory implements Factory<DashboardViewModel> {
  private final Provider<ApiService> apiServiceProvider;

  private final Provider<SupporterRepository> supporterRepositoryProvider;

  private final Provider<SyncRepository> syncRepositoryProvider;

  private final Provider<UserPreferences> userPreferencesProvider;

  private final Provider<AuthRepository> authRepositoryProvider;

  public DashboardViewModel_Factory(Provider<ApiService> apiServiceProvider,
      Provider<SupporterRepository> supporterRepositoryProvider,
      Provider<SyncRepository> syncRepositoryProvider,
      Provider<UserPreferences> userPreferencesProvider,
      Provider<AuthRepository> authRepositoryProvider) {
    this.apiServiceProvider = apiServiceProvider;
    this.supporterRepositoryProvider = supporterRepositoryProvider;
    this.syncRepositoryProvider = syncRepositoryProvider;
    this.userPreferencesProvider = userPreferencesProvider;
    this.authRepositoryProvider = authRepositoryProvider;
  }

  @Override
  public DashboardViewModel get() {
    return newInstance(apiServiceProvider.get(), supporterRepositoryProvider.get(), syncRepositoryProvider.get(), userPreferencesProvider.get(), authRepositoryProvider.get());
  }

  public static DashboardViewModel_Factory create(Provider<ApiService> apiServiceProvider,
      Provider<SupporterRepository> supporterRepositoryProvider,
      Provider<SyncRepository> syncRepositoryProvider,
      Provider<UserPreferences> userPreferencesProvider,
      Provider<AuthRepository> authRepositoryProvider) {
    return new DashboardViewModel_Factory(apiServiceProvider, supporterRepositoryProvider, syncRepositoryProvider, userPreferencesProvider, authRepositoryProvider);
  }

  public static DashboardViewModel newInstance(ApiService apiService,
      SupporterRepository supporterRepository, SyncRepository syncRepository,
      UserPreferences userPreferences, AuthRepository authRepository) {
    return new DashboardViewModel(apiService, supporterRepository, syncRepository, userPreferences, authRepository);
  }
}
