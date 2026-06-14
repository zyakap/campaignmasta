package com.campaignmasta.data.repository

import com.campaignmasta.data.remote.ApiService
import com.campaignmasta.data.remote.dto.ApprovalActionRequest
import com.campaignmasta.data.remote.dto.CreatableRoleDto
import com.campaignmasta.data.remote.dto.CreateTeamMemberRequest
import com.campaignmasta.data.remote.dto.CreateVillageRequest
import com.campaignmasta.data.remote.dto.GeoItemDto
import com.campaignmasta.data.remote.dto.PerformanceResponse
import com.campaignmasta.data.remote.dto.TeamMemberDto
import com.campaignmasta.data.remote.dto.VillageDto
import retrofit2.Response
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Network-backed access to the team hierarchy, approvals, cascading geography
 * and village requests. Team data is read live (small lists, must reflect the
 * caller's scope), with friendly error messages for the field UI.
 */
@Singleton
class TeamRepository @Inject constructor(
    private val api: ApiService
) {
    suspend fun getTeam(): Result<List<TeamMemberDto>> =
        safe { api.getTeamMembers() }.map { it.results }

    suspend fun getPendingMembers(): Result<List<TeamMemberDto>> =
        safe { api.getPendingTeamMembers() }.map { it.results }

    suspend fun getCreatableRoles(): Result<List<CreatableRoleDto>> =
        safe { api.getCreatableRoles() }.map { it.results }

    suspend fun getGeography(level: String, parent: Int? = null): Result<List<GeoItemDto>> =
        safe { api.getGeography(level, parent) }.map { it.results }

    suspend fun createMember(request: CreateTeamMemberRequest): Result<TeamMemberDto> =
        safe { api.createTeamMember(request) }

    suspend fun approveMember(id: Int, reject: Boolean = false): Result<TeamMemberDto> =
        safe { api.approveTeamMember(id, ApprovalActionRequest(reject)) }

    suspend fun getPerformance(): Result<PerformanceResponse> =
        safe { api.getPerformance() }

    suspend fun getPendingVillages(): Result<List<VillageDto>> =
        safe { api.getPendingVillages() }.map { it.results }

    suspend fun createVillage(ward: Int, name: String): Result<VillageDto> =
        safe { api.createVillage(CreateVillageRequest(ward, name)) }

    suspend fun approveVillage(id: Int, reject: Boolean = false): Result<Unit> =
        safe { api.approveVillage(id, ApprovalActionRequest(reject)) }.map { }

    /** Wrap a Retrofit call: success on 2xx, otherwise a readable message. */
    private inline fun <T> safe(call: () -> Response<T>): Result<T> = try {
        val response = call()
        val body = response.body()
        if (response.isSuccessful && body != null) {
            Result.success(body)
        } else {
            Result.failure(Exception(humanError(response.code(), response.errorBody()?.string())))
        }
    } catch (e: Exception) {
        Result.failure(Exception("No connection. Check your internet and try again."))
    }

    private fun humanError(code: Int, raw: String?): String {
        val detail = raw
            ?.substringAfter("\"detail\":\"", "")
            ?.substringBefore("\"")
            ?.takeIf { it.isNotBlank() }
        return when {
            detail != null -> detail
            code == 403 -> "You do not have permission for this action."
            code == 401 -> "Your session has expired. Please sign in again."
            else -> "Something went wrong (error $code). Please try again."
        }
    }
}
