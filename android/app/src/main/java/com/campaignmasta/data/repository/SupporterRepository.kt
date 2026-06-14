package com.campaignmasta.data.repository

import com.campaignmasta.data.local.dao.SupporterDao
import com.campaignmasta.data.local.dao.SyncQueueDao
import com.campaignmasta.data.local.entity.SupporterEntity
import com.campaignmasta.data.local.entity.SyncQueueEntity
import com.campaignmasta.data.preferences.UserPreferences
import com.campaignmasta.data.remote.ApiService
import com.campaignmasta.data.remote.dto.SupporterDto
import com.google.gson.Gson
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import java.util.UUID
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SupporterRepository @Inject constructor(
    private val supporterDao: SupporterDao,
    private val syncQueueDao: SyncQueueDao,
    private val apiService: ApiService,
    private val userPreferences: UserPreferences,
    private val gson: Gson
) {
    val supporters: Flow<List<SupporterEntity>> = supporterDao.getAllFlow()

    fun observeSupporter(localId: String): Flow<SupporterEntity?> = supporterDao.observeByLocalId(localId)

    /** Create a supporter offline — queues for sync. */
    suspend fun createOffline(
        fullName: String,
        phone: String,
        ward: String,
        wardId: Int?,
        clan: String,
        enrollmentStatus: String,
        supportStatus: String,
        notes: String
    ): SupporterEntity {
        val localId = UUID.randomUUID().toString()
        val entity = SupporterEntity(
            localId = localId,
            fullName = fullName,
            phone = phone,
            ward = ward,
            wardId = wardId,
            clan = clan,
            enrollmentStatus = enrollmentStatus,
            supportStatus = supportStatus,
            notes = notes,
            syncStatus = "PENDING"
        )
        supporterDao.insert(entity)

        // Enqueue sync
        val provinceId = userPreferences.provinceId.first() ?: 1
        val payload = mapOf(
            "full_name" to fullName,
            "phone" to phone,
            "ward" to wardId,
            "clan" to clan,
            "enrollment_status" to enrollmentStatus,
            "support_status" to supportStatus,
            "notes" to notes,
            "province" to provinceId
        )
        syncQueueDao.insert(
            SyncQueueEntity(
                entityType = "supporter",
                operation = "CREATE",
                localId = localId,
                payload = gson.toJson(payload)
            )
        )
        return entity
    }

    /** Pull supporters from server and upsert locally. Returns true on success. */
    suspend fun pullFromServer(): Boolean {
        return try {
            val updatedAfter = userPreferences.lastSyncSupporters.first()
            var page = 1
            var hasMore = true
            while (hasMore) {
                val response = apiService.getSupporters(updatedAfter = updatedAfter, page = page)
                if (response.isSuccessful) {
                    val body = response.body() ?: break
                    val entities = body.results.map { it.toEntity() }
                    supporterDao.insertAll(entities)
                    hasMore = body.next != null
                    page++
                } else {
                    return false
                }
            }
            // Update last sync timestamp
            val now = java.time.Instant.now().toString()
            userPreferences.updateLastSync(UserPreferences.LAST_SYNC_SUPPORTERS, now)
            true
        } catch (e: Exception) {
            false
        }
    }

    suspend fun count(): Int = supporterDao.count()
}

fun SupporterDto.toEntity(): SupporterEntity = SupporterEntity(
    localId = "server_$id",
    serverId = id,
    fullName = fullName,
    phone = phone,
    ward = wardName,
    wardId = ward,
    clan = clan,
    enrollmentStatus = enrollmentStatus,
    supportStatus = supportStatus,
    notes = notes,
    followUpRequired = followUpRequired,
    followUpDate = followUpDate,
    consentToMessages = consentToMessages,
    updatedAt = updatedAt,
    syncStatus = "SYNCED"
)
