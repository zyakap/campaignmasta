package com.campaignmasta.sync;

import android.content.Context;
import androidx.work.WorkerParameters;
import com.campaignmasta.data.repository.MessageRepository;
import com.campaignmasta.data.repository.SupporterRepository;
import com.campaignmasta.data.repository.SyncRepository;
import dagger.internal.DaggerGenerated;
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
public final class SyncWorker_Factory {
  private final Provider<SyncRepository> syncRepositoryProvider;

  private final Provider<SupporterRepository> supporterRepositoryProvider;

  private final Provider<MessageRepository> messageRepositoryProvider;

  public SyncWorker_Factory(Provider<SyncRepository> syncRepositoryProvider,
      Provider<SupporterRepository> supporterRepositoryProvider,
      Provider<MessageRepository> messageRepositoryProvider) {
    this.syncRepositoryProvider = syncRepositoryProvider;
    this.supporterRepositoryProvider = supporterRepositoryProvider;
    this.messageRepositoryProvider = messageRepositoryProvider;
  }

  public SyncWorker get(Context context, WorkerParameters workerParams) {
    return newInstance(context, workerParams, syncRepositoryProvider.get(), supporterRepositoryProvider.get(), messageRepositoryProvider.get());
  }

  public static SyncWorker_Factory create(Provider<SyncRepository> syncRepositoryProvider,
      Provider<SupporterRepository> supporterRepositoryProvider,
      Provider<MessageRepository> messageRepositoryProvider) {
    return new SyncWorker_Factory(syncRepositoryProvider, supporterRepositoryProvider, messageRepositoryProvider);
  }

  public static SyncWorker newInstance(Context context, WorkerParameters workerParams,
      SyncRepository syncRepository, SupporterRepository supporterRepository,
      MessageRepository messageRepository) {
    return new SyncWorker(context, workerParams, syncRepository, supporterRepository, messageRepository);
  }
}
