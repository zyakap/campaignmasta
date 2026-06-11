package com.campaignmasta.data.repository;

import com.campaignmasta.data.local.dao.MessageDao;
import com.campaignmasta.data.preferences.UserPreferences;
import com.campaignmasta.data.remote.ApiService;
import dagger.internal.DaggerGenerated;
import dagger.internal.Factory;
import dagger.internal.QualifierMetadata;
import dagger.internal.ScopeMetadata;
import javax.annotation.processing.Generated;
import javax.inject.Provider;

@ScopeMetadata("javax.inject.Singleton")
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
public final class MessageRepository_Factory implements Factory<MessageRepository> {
  private final Provider<MessageDao> messageDaoProvider;

  private final Provider<ApiService> apiServiceProvider;

  private final Provider<UserPreferences> userPreferencesProvider;

  public MessageRepository_Factory(Provider<MessageDao> messageDaoProvider,
      Provider<ApiService> apiServiceProvider, Provider<UserPreferences> userPreferencesProvider) {
    this.messageDaoProvider = messageDaoProvider;
    this.apiServiceProvider = apiServiceProvider;
    this.userPreferencesProvider = userPreferencesProvider;
  }

  @Override
  public MessageRepository get() {
    return newInstance(messageDaoProvider.get(), apiServiceProvider.get(), userPreferencesProvider.get());
  }

  public static MessageRepository_Factory create(Provider<MessageDao> messageDaoProvider,
      Provider<ApiService> apiServiceProvider, Provider<UserPreferences> userPreferencesProvider) {
    return new MessageRepository_Factory(messageDaoProvider, apiServiceProvider, userPreferencesProvider);
  }

  public static MessageRepository newInstance(MessageDao messageDao, ApiService apiService,
      UserPreferences userPreferences) {
    return new MessageRepository(messageDao, apiService, userPreferences);
  }
}
