package com.campaignmasta.di;

import com.campaignmasta.data.local.AppDatabase;
import com.campaignmasta.data.local.dao.CallLogDao;
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
public final class DatabaseModule_CallLogDaoFactory implements Factory<CallLogDao> {
  private final Provider<AppDatabase> dbProvider;

  public DatabaseModule_CallLogDaoFactory(Provider<AppDatabase> dbProvider) {
    this.dbProvider = dbProvider;
  }

  @Override
  public CallLogDao get() {
    return callLogDao(dbProvider.get());
  }

  public static DatabaseModule_CallLogDaoFactory create(Provider<AppDatabase> dbProvider) {
    return new DatabaseModule_CallLogDaoFactory(dbProvider);
  }

  public static CallLogDao callLogDao(AppDatabase db) {
    return Preconditions.checkNotNullFromProvides(DatabaseModule.INSTANCE.callLogDao(db));
  }
}
