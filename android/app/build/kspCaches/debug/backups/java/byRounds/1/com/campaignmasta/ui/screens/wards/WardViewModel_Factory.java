package com.campaignmasta.ui.screens.wards;

import com.campaignmasta.data.local.dao.WardProfileDao;
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
public final class WardViewModel_Factory implements Factory<WardViewModel> {
  private final Provider<WardProfileDao> wardProfileDaoProvider;

  public WardViewModel_Factory(Provider<WardProfileDao> wardProfileDaoProvider) {
    this.wardProfileDaoProvider = wardProfileDaoProvider;
  }

  @Override
  public WardViewModel get() {
    return newInstance(wardProfileDaoProvider.get());
  }

  public static WardViewModel_Factory create(Provider<WardProfileDao> wardProfileDaoProvider) {
    return new WardViewModel_Factory(wardProfileDaoProvider);
  }

  public static WardViewModel newInstance(WardProfileDao wardProfileDao) {
    return new WardViewModel(wardProfileDao);
  }
}
