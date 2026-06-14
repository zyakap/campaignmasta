package com.campaignmasta.data.repository;

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
public final class TeamRepository_Factory implements Factory<TeamRepository> {
  private final Provider<ApiService> apiProvider;

  public TeamRepository_Factory(Provider<ApiService> apiProvider) {
    this.apiProvider = apiProvider;
  }

  @Override
  public TeamRepository get() {
    return newInstance(apiProvider.get());
  }

  public static TeamRepository_Factory create(Provider<ApiService> apiProvider) {
    return new TeamRepository_Factory(apiProvider);
  }

  public static TeamRepository newInstance(ApiService api) {
    return new TeamRepository(api);
  }
}
