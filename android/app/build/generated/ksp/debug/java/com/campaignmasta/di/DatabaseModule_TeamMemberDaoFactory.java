package com.campaignmasta.di;

import com.campaignmasta.data.local.AppDatabase;
import com.campaignmasta.data.local.dao.TeamMemberDao;
import dagger.internal.DaggerGenerated;
import dagger.internal.Factory;
import dagger.internal.Preconditions;
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
public final class DatabaseModule_TeamMemberDaoFactory implements Factory<TeamMemberDao> {
  private final Provider<AppDatabase> dbProvider;

  public DatabaseModule_TeamMemberDaoFactory(Provider<AppDatabase> dbProvider) {
    this.dbProvider = dbProvider;
  }

  @Override
  public TeamMemberDao get() {
    return teamMemberDao(dbProvider.get());
  }

  public static DatabaseModule_TeamMemberDaoFactory create(Provider<AppDatabase> dbProvider) {
    return new DatabaseModule_TeamMemberDaoFactory(dbProvider);
  }

  public static TeamMemberDao teamMemberDao(AppDatabase db) {
    return Preconditions.checkNotNullFromProvides(DatabaseModule.INSTANCE.teamMemberDao(db));
  }
}
