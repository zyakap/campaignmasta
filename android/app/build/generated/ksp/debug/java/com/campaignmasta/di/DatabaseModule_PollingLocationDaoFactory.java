package com.campaignmasta.di;

import com.campaignmasta.data.local.AppDatabase;
import com.campaignmasta.data.local.dao.PollingLocationDao;
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
public final class DatabaseModule_PollingLocationDaoFactory implements Factory<PollingLocationDao> {
  private final Provider<AppDatabase> dbProvider;

  public DatabaseModule_PollingLocationDaoFactory(Provider<AppDatabase> dbProvider) {
    this.dbProvider = dbProvider;
  }

  @Override
  public PollingLocationDao get() {
    return pollingLocationDao(dbProvider.get());
  }

  public static DatabaseModule_PollingLocationDaoFactory create(Provider<AppDatabase> dbProvider) {
    return new DatabaseModule_PollingLocationDaoFactory(dbProvider);
  }

  public static PollingLocationDao pollingLocationDao(AppDatabase db) {
    return Preconditions.checkNotNullFromProvides(DatabaseModule.INSTANCE.pollingLocationDao(db));
  }
}
