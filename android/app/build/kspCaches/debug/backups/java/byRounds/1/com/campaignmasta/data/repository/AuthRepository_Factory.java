package com.campaignmasta.data.repository;

import com.campaignmasta.data.preferences.UserPreferences;
import com.campaignmasta.data.remote.ApiService;
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
public final class AuthRepository_Factory implements Factory<AuthRepository> {
  private final Provider<ApiService> apiServiceProvider;

  private final Provider<UserPreferences> userPreferencesProvider;

  public AuthRepository_Factory(Provider<ApiService> apiServiceProvider,
      Provider<UserPreferences> userPreferencesProvider) {
    this.apiServiceProvider = apiServiceProvider;
    this.userPreferencesProvider = userPreferencesProvider;
  }

  @Override
  public AuthRepository get() {
    return newInstance(apiServiceProvider.get(), userPreferencesProvider.get());
  }

  public static AuthRepository_Factory create(Provider<ApiService> apiServiceProvider,
      Provider<UserPreferences> userPreferencesProvider) {
    return new AuthRepository_Factory(apiServiceProvider, userPreferencesProvider);
  }

  public static AuthRepository newInstance(ApiService apiService, UserPreferences userPreferences) {
    return new AuthRepository(apiService, userPreferences);
  }
}
