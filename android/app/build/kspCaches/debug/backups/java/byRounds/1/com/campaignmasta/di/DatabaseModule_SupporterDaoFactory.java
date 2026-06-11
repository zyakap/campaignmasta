package com.campaignmasta.di;

import com.campaignmasta.data.local.AppDatabase;
import com.campaignmasta.data.local.dao.SupporterDao;
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
public final class DatabaseModule_SupporterDaoFactory implements Factory<SupporterDao> {
  private final Provider<AppDatabase> dbProvider;

  public DatabaseModule_SupporterDaoFactory(Provider<AppDatabase> dbProvider) {
    this.dbProvider = dbProvider;
  }

  @Override
  public SupporterDao get() {
    return supporterDao(dbProvider.get());
  }

  public static DatabaseModule_SupporterDaoFactory create(Provider<AppDatabase> dbProvider) {
    return new DatabaseModule_SupporterDaoFactory(dbProvider);
  }

  public static SupporterDao supporterDao(AppDatabase db) {
    return Preconditions.checkNotNullFromProvides(DatabaseModule.INSTANCE.supporterDao(db));
  }
}
