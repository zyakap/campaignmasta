package com.campaignmasta.data.repository

import com.campaignmasta.data.local.dao.*
import com.campaignmasta.data.local.entity.*
import com.campaignmasta.data.preferences.UserPreferences
import com.campaignmasta.data.remote.ApiService
import com.campaignmasta.data.remote.dto.*
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import java.time.Instant
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SyncRepository @Inject constructor(
    private val syncQueueDao: SyncQueueDao,
    private val supporterDao: SupporterDao,
    private val callLogDao: CallLogDao,
    private val teamMemberDao: TeamMemberDao,
    private val influencerDao: InfluencerDao,
    private val wardProfileDao: WardProfileDao,
    private val communityGroupDao: CommunityGroupDao,
    private val pollingLocationDao: PollingLocationDao,
    private val messageDao: MessageDao,
    private val apiService: ApiService,
    private val userPreferences: UserPreferences,
    private val gson: Gson
) {
    val pendingCount: Flow<Int> = syncQueueDao.pendingCountFlow()

    /** Push all PENDING items from the sync queue in batches of 20. */
    suspend fun pushPending(): Boolean {
        val pending = syncQueueDao.getPending()
        if (pending.isEmpty()) return true

        val mapType = object : TypeToken<Map<String, Any?>>() {}.type

        val batches = pending.chunked(20)
        var allOk = true
        for (batch in batches) {
            // Mark in-flight
            batch.forEach { syncQueueDao.markInFlight(it.id) }

            val items = batch.map { item ->
                val payload: Map<String, Any?> = gson.fromJson(item.payload, mapType)
                SyncPushItem(
                    entityType = item.entityType,
                    operation = item.operation,
                    localId = item.localId,
                    serverId = item.serverId,
                    payload = payload
                )
            }

            try {
                val response = apiService.syncPush(SyncPushRequest(items))
                if (response.isSuccessful) {
                    val results = response.body()?.results ?: emptyList()
                    for (result in results) {
                        val queueItem = batch.find { it.localId == result.localId } ?: continue
                        if (result.status == "OK") {
                            syncQueueDao.markDone(queueItem.id)
                            // Update local entity with server ID
                            val serverId = result.serverId
                            if (serverId != null) {
                                when (queueItem.entityType) {
                                    "supporter" -> supporterDao.markSynced(queueItem.localId, serverId)
                                    "call_log" -> callLogDao.markSynced(queueItem.localId, serverId)
                                    "community_group" -> communityGroupDao.markSynced(queueItem.localId, serverId)
                                }
                            }
                        } else {
                            syncQueueDao.markFailed(queueItem.id, result.status)
                            allOk = false
                        }
                    }
                } else {
                    batch.forEach { syncQueueDao.markFailed(it.id, "HTTP ${response.code()}") }
                    allOk = false
                }
            } catch (e: Exception) {
                batch.forEach { syncQueueDao.markFailed(it.id, e.message ?: "exception") }
                allOk = false
            }
        }

        syncQueueDao.clearCompleted()
        return allOk
    }

    /** Pull all entity types from server using incremental sync. */
    suspend fun pullAll(): Boolean {
        var allOk = true
        allOk = allOk && pullTeamMembers()
        allOk = allOk && pullInfluencers()
        allOk = allOk && pullWardProfiles()
        allOk = allOk && pullCommunityGroups()
        allOk = allOk && pullPollingLocations()
        allOk = allOk && pullMessages()
        return allOk
    }

    private suspend fun pullTeamMembers(): Boolean {
        return try {
            val updatedAfter = userPreferences.lastSyncTeamMembers.first()
            val response = apiService.getTeamMembers(updatedAfter)
            if (response.isSuccessful) {
                val results = response.body()?.results ?: return false
                val entities = results.map {
                    TeamMemberEntity(
                        localId = "server_${it.id}",
                        serverId = it.id,
                        fullName = it.fullName,
                        gender = it.gender,
                        phone = it.phone,
                        email = it.email,
                        role = it.role,
                        wardName = it.wardName,
                        wardId = it.ward,
                        isActive = it.isActive,
                        notes = it.notes,
                        updatedAt = it.updatedAt
                    )
                }
                teamMemberDao.insertAll(entities)
                userPreferences.updateLastSync(UserPreferences.LAST_SYNC_TEAM_MEMBERS, Instant.now().toString())
                true
            } else false
        } catch (e: Exception) { false }
    }

    private suspend fun pullInfluencers(): Boolean {
        return try {
            val updatedAfter = userPreferences.lastSyncInfluencers.first()
            val response = apiService.getInfluencers(updatedAfter)
            if (response.isSuccessful) {
                val results = response.body()?.results ?: return false
                val entities = results.map {
                    InfluencerEntity(
                        localId = "server_${it.id}",
                        serverId = it.id,
                        fullName = it.fullName,
                        phone = it.phone,
                        communityRole = it.communityRole,
                        influenceLevel = it.influenceLevel,
                        relationshipStatus = it.relationshipStatus,
                        contactFrequencyDays = it.contactFrequencyDays,
                        lastCallDate = it.lastCallDate,
                        nextContactDueDate = it.nextContactDueDate,
                        wardName = it.wardName,
                        wardId = it.ward,
                        notes = it.notes,
                        updatedAt = it.updatedAt
                    )
                }
                influencerDao.insertAll(entities)
                userPreferences.updateLastSync(UserPreferences.LAST_SYNC_INFLUENCERS, Instant.now().toString())
                true
            } else false
        } catch (e: Exception) { false }
    }

    private suspend fun pullWardProfiles(): Boolean {
        return try {
            val updatedAfter = userPreferences.lastSyncWardProfiles.first()
            val response = apiService.getWardProfiles(updatedAfter)
            if (response.isSuccessful) {
                val results = response.body()?.results ?: return false
                val entities = results.map {
                    WardProfileEntity(
                        localId = "server_${it.id}",
                        serverId = it.id,
                        wardId = it.ward,
                        wardName = it.wardName,
                        wardNumber = it.wardNumber,
                        llgName = it.llgName,
                        councillorName = it.councillorName,
                        supportStrength = it.supportStrength,
                        populationEstimate = it.populationEstimate,
                        estimatedVotingPopulation = it.estimatedVotingPopulation,
                        keyClans = it.keyClans,
                        keyChurches = it.keyChurches,
                        mainCommunityIssues = it.mainCommunityIssues,
                        notesForCandidate = it.notesForCandidate,
                        securityConcerns = it.securityConcerns,
                        updatedAt = it.updatedAt
                    )
                }
                wardProfileDao.insertAll(entities)
                userPreferences.updateLastSync(UserPreferences.LAST_SYNC_WARD_PROFILES, Instant.now().toString())
                true
            } else false
        } catch (e: Exception) { false }
    }

    private suspend fun pullCommunityGroups(): Boolean {
        return try {
            val updatedAfter = userPreferences.lastSyncCommunityGroups.first()
            val response = apiService.getCommunityGroups(updatedAfter)
            if (response.isSuccessful) {
                val results = response.body()?.results ?: return false
                val entities = results.map {
                    CommunityGroupEntity(
                        localId = "server_${it.id}",
                        serverId = it.id,
                        name = it.name,
                        groupType = it.groupType,
                        wardName = it.wardName,
                        wardId = it.ward,
                        estimatedVotingMembers = it.estimatedVotingMembers,
                        alignment = it.alignment,
                        notes = it.notes,
                        updatedAt = it.updatedAt,
                        syncStatus = "SYNCED"
                    )
                }
                communityGroupDao.insertAll(entities)
                userPreferences.updateLastSync(UserPreferences.LAST_SYNC_COMMUNITY_GROUPS, Instant.now().toString())
                true
            } else false
        } catch (e: Exception) { false }
    }

    private suspend fun pullPollingLocations(): Boolean {
        return try {
            val updatedAfter = userPreferences.lastSyncPollingLocations.first()
            val response = apiService.getPollingLocations(updatedAfter)
            if (response.isSuccessful) {
                val results = response.body()?.results ?: return false
                val entities = results.map {
                    PollingLocationEntity(
                        localId = "server_${it.id}",
                        serverId = it.id,
                        name = it.name,
                        wardName = it.wardName,
                        wardId = it.ward,
                        gpsCoordinates = it.gpsCoordinates,
                        scrutineerName = it.scrutineerName,
                        scrutineerCheckedIn = it.scrutineerCheckedIn,
                        securityRisk = it.securityRisk,
                        expectedTurnout = it.expectedTurnout,
                        status = it.status,
                        notes = it.notes,
                        updatedAt = it.updatedAt
                    )
                }
                pollingLocationDao.insertAll(entities)
                userPreferences.updateLastSync(UserPreferences.LAST_SYNC_POLLING_LOCATIONS, Instant.now().toString())
                true
            } else false
        } catch (e: Exception) { false }
    }

    private suspend fun pullMessages(): Boolean {
        return try {
            val updatedAfter = userPreferences.lastSyncMessages.first()
            val response = apiService.getMessages(updatedAfter)
            if (response.isSuccessful) {
                val results = response.body()?.results ?: return false
                val entities = results.map { it.toEntity() }
                messageDao.insertAll(entities)
                userPreferences.updateLastSync(UserPreferences.LAST_SYNC_MESSAGES, Instant.now().toString())
                true
            } else false
        } catch (e: Exception) { false }
    }
}
