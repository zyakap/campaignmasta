package com.campaignmasta.di;

import com.campaignmasta.data.local.AppDatabase;
import com.campaignmasta.data.local.dao.InfluencerDao;
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
public final class DatabaseModule_InfluencerDaoFactory implements Factory<InfluencerDao> {
  private final Provider<AppDatabase> dbProvider;

  public DatabaseModule_InfluencerDaoFactory(Provider<AppDatabase> dbProvider) {
    this.dbProvider = dbProvider;
  }

  @Override
  public InfluencerDao get() {
    return influencerDao(dbProvider.get());
  }

  public static DatabaseModule_InfluencerDaoFactory create(Provider<AppDatabase> dbProvider) {
    return new DatabaseModule_InfluencerDaoFactory(dbProvider);
  }

  public static InfluencerDao influencerDao(AppDatabase db) {
    return Preconditions.checkNotNullFromProvides(DatabaseModule.INSTANCE.influencerDao(db));
  }
}
