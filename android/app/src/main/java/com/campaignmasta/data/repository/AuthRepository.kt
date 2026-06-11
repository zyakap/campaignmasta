package com.campaignmasta.data.repository

import com.campaignmasta.data.preferences.UserPreferences
import com.campaignmasta.data.remote.ApiService
import com.campaignmasta.data.remote.dto.LoginRequest
import com.campaignmasta.data.remote.dto.LoginResponse
import javax.inject.Inject
import javax.inject.Singleton

sealed class AuthResult {
    data class Success(val response: LoginResponse) : AuthResult()
    data class Error(val message: String) : AuthResult()
}

@Singleton
class AuthRepository @Inject constructor(
    private val apiService: ApiService,
    private val userPreferences: UserPreferences
) {
    suspend fun login(username: String, password: String): AuthResult {
        return try {
            val response = apiService.login(LoginRequest(username, password))
            if (response.isSuccessful) {
                val body = response.body()!!
                userPreferences.saveLoginData(
                    token = body.token,
                    userId = body.userId,
                    candidateId = body.candidateId,
                    candidateName = body.candidateName,
                    subscriptionPlan = body.subscriptionPlan,
                    role = body.role
                )
                AuthResult.Success(body)
            } else {
                val errorBody = response.errorBody()?.string() ?: "Login failed"
                AuthResult.Error(errorBody)
            }
        } catch (e: Exception) {
            AuthResult.Error(e.message ?: "Network error")
        }
    }

    suspend fun logout() {
        userPreferences.clearAll()
    }
}
