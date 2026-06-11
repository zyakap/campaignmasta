package com.campaignmasta.di;

import com.campaignmasta.data.local.AppDatabase;
import com.campaignmasta.data.local.dao.SyncQueueDao;
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
public final class DatabaseModule_SyncQueueDaoFactory implements Factory<SyncQueueDao> {
  private final Provider<AppDatabase> dbProvider;

  public DatabaseModule_SyncQueueDaoFactory(Provider<AppDatabase> dbProvider) {
    this.dbProvider = dbProvider;
  }

  @Override
  public SyncQueueDao get() {
    return syncQueueDao(dbProvider.get());
  }

  public static DatabaseModule_SyncQueueDaoFactory create(Provider<AppDatabase> dbProvider) {
    return new DatabaseModule_SyncQueueDaoFactory(dbProvider);
  }

  public static SyncQueueDao syncQueueDao(AppDatabase db) {
    return Preconditions.checkNotNullFromProvides(DatabaseModule.INSTANCE.syncQueueDao(db));
  }
}
