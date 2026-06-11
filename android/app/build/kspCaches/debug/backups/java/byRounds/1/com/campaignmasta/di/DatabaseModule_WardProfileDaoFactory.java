package com.campaignmasta.di;

import com.campaignmasta.data.local.AppDatabase;
import com.campaignmasta.data.local.dao.WardProfileDao;
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
public final class DatabaseModule_WardProfileDaoFactory implements Factory<WardProfileDao> {
  private final Provider<AppDatabase> dbProvider;

  public DatabaseModule_WardProfileDaoFactory(Provider<AppDatabase> dbProvider) {
    this.dbProvider = dbProvider;
  }

  @Override
  public WardProfileDao get() {
    return wardProfileDao(dbProvider.get());
  }

  public static DatabaseModule_WardProfileDaoFactory create(Provider<AppDatabase> dbProvider) {
    return new DatabaseModule_WardProfileDaoFactory(dbProvider);
  }

  public static WardProfileDao wardProfileDao(AppDatabase db) {
    return Preconditions.checkNotNullFromProvides(DatabaseModule.INSTANCE.wardProfileDao(db));
  }
}
