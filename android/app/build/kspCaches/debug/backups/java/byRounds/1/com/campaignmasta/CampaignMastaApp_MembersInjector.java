package com.campaignmasta;

import androidx.hilt.work.HiltWorkerFactory;
import dagger.MembersInjector;
import dagger.internal.DaggerGenerated;
import dagger.internal.InjectedFieldSignature;
import dagger.internal.QualifierMetadata;
import javax.annotation.processing.Generated;
import javax.inject.Provider;

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
public final class CampaignMastaApp_MembersInjector implements MembersInjector<CampaignMastaApp> {
  private final Provider<HiltWorkerFactory> workerFactoryProvider;

  public CampaignMastaApp_MembersInjector(Provider<HiltWorkerFactory> workerFactoryProvider) {
    this.workerFactoryProvider = workerFactoryProvider;
  }

  public static MembersInjector<CampaignMastaApp> create(
      Provider<HiltWorkerFactory> workerFactoryProvider) {
    return new CampaignMastaApp_MembersInjector(workerFactoryProvider);
  }

  @Override
  public void injectMembers(CampaignMastaApp instance) {
    injectWorkerFactory(instance, workerFactoryProvider.get());
  }

  @InjectedFieldSignature("com.campaignmasta.CampaignMastaApp.workerFactory")
  public static void injectWorkerFactory(CampaignMastaApp instance,
      HiltWorkerFactory workerFactory) {
    instance.workerFactory = workerFactory;
  }
}
