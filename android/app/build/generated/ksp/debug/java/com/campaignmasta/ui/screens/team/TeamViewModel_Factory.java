package com.campaignmasta.ui.screens.team;

import com.campaignmasta.data.repository.TeamRepository;
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
public final class TeamViewModel_Factory implements Factory<TeamViewModel> {
  private final Provider<TeamRepository> teamRepositoryProvider;

  public TeamViewModel_Factory(Provider<TeamRepository> teamRepositoryProvider) {
    this.teamRepositoryProvider = teamRepositoryProvider;
  }

  @Override
  public TeamViewModel get() {
    return newInstance(teamRepositoryProvider.get());
  }

  public static TeamViewModel_Factory create(Provider<TeamRepository> teamRepositoryProvider) {
    return new TeamViewModel_Factory(teamRepositoryProvider);
  }

  public static TeamViewModel newInstance(TeamRepository teamRepository) {
    return new TeamViewModel(teamRepository);
  }
}
