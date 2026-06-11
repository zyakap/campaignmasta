package com.campaignmasta.di;

import com.campaignmasta.data.local.AppDatabase;
import com.campaignmasta.data.local.dao.CommunityGroupDao;
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
public final class DatabaseModule_CommunityGroupDaoFactory implements Factory<CommunityGroupDao> {
  private final Provider<AppDatabase> dbProvider;

  public DatabaseModule_CommunityGroupDaoFactory(Provider<AppDatabase> dbProvider) {
    this.dbProvider = dbProvider;
  }

  @Override
  public CommunityGroupDao get() {
    return communityGroupDao(dbProvider.get());
  }

  public static DatabaseModule_CommunityGroupDaoFactory create(Provider<AppDatabase> dbProvider) {
    return new DatabaseModule_CommunityGroupDaoFactory(dbProvider);
  }

  public static CommunityGroupDao communityGroupDao(AppDatabase db) {
    return Preconditions.checkNotNullFromProvides(DatabaseModule.INSTANCE.communityGroupDao(db));
  }
}
