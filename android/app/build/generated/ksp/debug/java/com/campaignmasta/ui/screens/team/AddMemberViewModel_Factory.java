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
public final class AddMemberViewModel_Factory implements Factory<AddMemberViewModel> {
  private final Provider<TeamRepository> teamRepositoryProvider;

  public AddMemberViewModel_Factory(Provider<TeamRepository> teamRepositoryProvider) {
    this.teamRepositoryProvider = teamRepositoryProvider;
  }

  @Override
  public AddMemberViewModel get() {
    return newInstance(teamRepositoryProvider.get());
  }

  public static AddMemberViewModel_Factory create(Provider<TeamRepository> teamRepositoryProvider) {
    return new AddMemberViewModel_Factory(teamRepositoryProvider);
  }

  public static AddMemberViewModel newInstance(TeamRepository teamRepository) {
    return new AddMemberViewModel(teamRepository);
  }
}
