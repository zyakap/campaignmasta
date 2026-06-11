package com.campaignmasta.data.remote;

import com.campaignmasta.data.preferences.UserPreferences;
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
public final class AuthInterceptor_Factory implements Factory<AuthInterceptor> {
  private final Provider<UserPreferences> userPreferencesProvider;

  public AuthInterceptor_Factory(Provider<UserPreferences> userPreferencesProvider) {
    this.userPreferencesProvider = userPreferencesProvider;
  }

  @Override
  public AuthInterceptor get() {
    return newInstance(userPreferencesProvider.get());
  }

  public static AuthInterceptor_Factory create(Provider<UserPreferences> userPreferencesProvider) {
    return new AuthInterceptor_Factory(userPreferencesProvider);
  }

  public static AuthInterceptor newInstance(UserPreferences userPreferences) {
    return new AuthInterceptor(userPreferences);
  }
}
