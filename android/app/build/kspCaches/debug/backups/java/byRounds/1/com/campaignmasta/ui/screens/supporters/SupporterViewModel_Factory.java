package com.campaignmasta.ui.screens.supporters;

import com.campaignmasta.data.repository.SupporterRepository;
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
public final class SupporterViewModel_Factory implements Factory<SupporterViewModel> {
  private final Provider<SupporterRepository> supporterRepositoryProvider;

  public SupporterViewModel_Factory(Provider<SupporterRepository> supporterRepositoryProvider) {
    this.supporterRepositoryProvider = supporterRepositoryProvider;
  }

  @Override
  public SupporterViewModel get() {
    return newInstance(supporterRepositoryProvider.get());
  }

  public static SupporterViewModel_Factory create(
      Provider<SupporterRepository> supporterRepositoryProvider) {
    return new SupporterViewModel_Factory(supporterRepositoryProvider);
  }

  public static SupporterViewModel newInstance(SupporterRepository supporterRepository) {
    return new SupporterViewModel(supporterRepository);
  }
}
