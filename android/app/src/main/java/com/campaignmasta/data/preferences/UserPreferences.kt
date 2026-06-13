package com.campaignmasta.data.preferences

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "user_prefs")

@Singleton
class UserPreferences @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val dataStore = context.dataStore

    companion object {
        val AUTH_TOKEN = stringPreferencesKey("auth_token")
        val USER_ID = intPreferencesKey("user_id")
        val CANDIDATE_ID = intPreferencesKey("candidate_id")
        val CANDIDATE_NAME = stringPreferencesKey("candidate_name")
        val SUBSCRIPTION_PLAN = stringPreferencesKey("subscription_plan")
        val USER_ROLE = stringPreferencesKey("user_role")
        val PROVINCE_ID = intPreferencesKey("province_id")

        // Last sync timestamps per entity type (ISO-8601 strings)
        val LAST_SYNC_SUPPORTERS = stringPreferencesKey("last_sync_supporters")
        val LAST_SYNC_TEAM_MEMBERS = stringPreferencesKey("last_sync_team_members")
        val LAST_SYNC_INFLUENCERS = stringPreferencesKey("last_sync_influencers")
        val LAST_SYNC_MESSAGES = stringPreferencesKey("last_sync_messages")
        val LAST_SYNC_WARD_PROFILES = stringPreferencesKey("last_sync_ward_profiles")
        val LAST_SYNC_COMMUNITY_GROUPS = stringPreferencesKey("last_sync_community_groups")
        val LAST_SYNC_POLLING_LOCATIONS = stringPreferencesKey("last_sync_polling_locations")
        val LAST_SYNC_PREFERENCE_DEALS = stringPreferencesKey("last_sync_preference_deals")
        val LAST_SYNC_REGISTRATION_DRIVES = stringPreferencesKey("last_sync_registration_drives")
    }

    val authToken: Flow<String?> = dataStore.data.map { it[AUTH_TOKEN] }
    val userId: Flow<Int?> = dataStore.data.map { it[USER_ID] }
    val candidateId: Flow<Int?> = dataStore.data.map { it[CANDIDATE_ID] }
    val candidateName: Flow<String?> = dataStore.data.map { it[CANDIDATE_NAME] }
    val subscriptionPlan: Flow<String?> = dataStore.data.map { it[SUBSCRIPTION_PLAN] }
    val userRole: Flow<String?> = dataStore.data.map { it[USER_ROLE] }
    val provinceId: Flow<Int?> = dataStore.data.map { it[PROVINCE_ID] }

    val lastSyncSupporters: Flow<String?> = dataStore.data.map { it[LAST_SYNC_SUPPORTERS] }
    val lastSyncTeamMembers: Flow<String?> = dataStore.data.map { it[LAST_SYNC_TEAM_MEMBERS] }
    val lastSyncInfluencers: Flow<String?> = dataStore.data.map { it[LAST_SYNC_INFLUENCERS] }
    val lastSyncMessages: Flow<String?> = dataStore.data.map { it[LAST_SYNC_MESSAGES] }
    val lastSyncWardProfiles: Flow<String?> = dataStore.data.map { it[LAST_SYNC_WARD_PROFILES] }
    val lastSyncCommunityGroups: Flow<String?> = dataStore.data.map { it[LAST_SYNC_COMMUNITY_GROUPS] }
    val lastSyncPollingLocations: Flow<String?> = dataStore.data.map { it[LAST_SYNC_POLLING_LOCATIONS] }
    val lastSyncPreferenceDeals: Flow<String?> = dataStore.data.map { it[LAST_SYNC_PREFERENCE_DEALS] }
    val lastSyncRegistrationDrives: Flow<String?> = dataStore.data.map { it[LAST_SYNC_REGISTRATION_DRIVES] }

    suspend fun saveLoginData(
        token: String,
        userId: Int,
        candidateId: Int,
        candidateName: String,
        subscriptionPlan: String,
        role: String
    ) {
        dataStore.edit { prefs ->
            prefs[AUTH_TOKEN] = token
            prefs[USER_ID] = userId
            prefs[CANDIDATE_ID] = candidateId
            prefs[CANDIDATE_NAME] = candidateName
            prefs[SUBSCRIPTION_PLAN] = subscriptionPlan
            prefs[USER_ROLE] = role
        }
    }

    suspend fun updateLastSync(key: Preferences.Key<String>, timestamp: String) {
        dataStore.edit { prefs -> prefs[key] = timestamp }
    }

    suspend fun clearAll() {
        dataStore.edit { it.clear() }
    }

    suspend fun isLoggedIn(): Boolean {
        // Use first() — collecting a DataStore flow never completes and would suspend forever.
        val token = authToken.first()
        return !token.isNullOrBlank()
    }
}
