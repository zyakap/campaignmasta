package com.campaignmasta.ui.screens.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.campaignmasta.data.preferences.UserPreferences
import com.campaignmasta.data.remote.ApiService
import com.campaignmasta.data.repository.AuthRepository
import com.campaignmasta.data.repository.SupporterRepository
import com.campaignmasta.data.repository.SyncRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class DashboardUiState(
    val candidateName: String = "",
    val userRole: String = "",
    val supporterCount: Int = 0,
    val callsDueCount: Int = 0,
    val messagesUnreadCount: Int = 0,
    val wardBriefsCount: Int = 0,
    val pollingLocationsCount: Int = 0,
    val teamCount: Int = 0,
    val pendingSyncCount: Int = 0,
    val isOnline: Boolean = false,
    val isRefreshing: Boolean = false,
    val errorMessage: String? = null
)

@HiltViewModel
class DashboardViewModel @Inject constructor(
    private val apiService: ApiService,
    private val supporterRepository: SupporterRepository,
    private val syncRepository: SyncRepository,
    private val userPreferences: UserPreferences,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(DashboardUiState())
    val uiState: StateFlow<DashboardUiState> = _uiState.asStateFlow()

    init {
        observePrefs()
        observeLocalData()
        refreshFromServer()
    }

    private fun observePrefs() {
        viewModelScope.launch {
            combine(
                userPreferences.candidateName,
                userPreferences.userRole
            ) { name, role -> Pair(name, role) }
                .collect { (name, role) ->
                    _uiState.update {
                        it.copy(
                            candidateName = name ?: "",
                            userRole = role ?: ""
                        )
                    }
                }
        }
    }

    private fun observeLocalData() {
        viewModelScope.launch {
            combine(
                supporterRepository.supporters.map { it.size },
                syncRepository.pendingCount
            ) { count, pending -> Pair(count, pending) }
                .collect { (count, pending) ->
                    _uiState.update {
                        it.copy(
                            supporterCount = count,
                            pendingSyncCount = pending
                        )
                    }
                }
        }
    }

    fun refreshFromServer() {
        viewModelScope.launch {
            _uiState.update { it.copy(isRefreshing = true) }
            try {
                val response = apiService.getDashboard()
                if (response.isSuccessful) {
                    val body = response.body()!!
                    _uiState.update {
                        it.copy(
                            supporterCount = body.supporterCount,
                            callsDueCount = body.callsDueCount,
                            messagesUnreadCount = body.messagesUnreadCount,
                            wardBriefsCount = body.wardBriefsCount,
                            pollingLocationsCount = body.pollingLocationsCount,
                            teamCount = body.teamCount,
                            isOnline = true,
                            isRefreshing = false,
                            errorMessage = null
                        )
                    }
                } else {
                    _uiState.update { it.copy(isRefreshing = false, isOnline = false) }
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(isRefreshing = false, isOnline = false) }
            }
        }
    }

    fun logout() {
        viewModelScope.launch { authRepository.logout() }
    }
}
