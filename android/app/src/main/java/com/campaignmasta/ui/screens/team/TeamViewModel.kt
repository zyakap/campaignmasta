package com.campaignmasta.ui.screens.team

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.campaignmasta.data.remote.dto.GeoItemDto
import com.campaignmasta.data.remote.dto.TeamMemberDto
import com.campaignmasta.data.remote.dto.VillageDto
import com.campaignmasta.data.repository.TeamRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class TeamUiState(
    val team: List<TeamMemberDto> = emptyList(),
    val pendingMembers: List<TeamMemberDto> = emptyList(),
    val pendingVillages: List<VillageDto> = emptyList(),
    val canAddMembers: Boolean = false,
    val canAddVillage: Boolean = false,
    val isLoading: Boolean = true,
    val isRefreshing: Boolean = false,
    val errorMessage: String? = null,
    val actionMessage: String? = null,
    // id currently being approved/rejected, so the row can show a spinner
    val busyMemberId: Int? = null,
    val busyVillageId: Int? = null,
    // Add-village dialog
    val villageDialogOpen: Boolean = false,
    val villageWards: List<GeoItemDto> = emptyList(),
    val villageSavingName: Boolean = false
)

@HiltViewModel
class TeamViewModel @Inject constructor(
    private val teamRepository: TeamRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(TeamUiState())
    val uiState: StateFlow<TeamUiState> = _uiState.asStateFlow()

    init {
        load()
    }

    fun load(isRefresh: Boolean = false) {
        _uiState.update {
            it.copy(isLoading = !isRefresh, isRefreshing = isRefresh, errorMessage = null)
        }
        viewModelScope.launch {
            val teamResult = teamRepository.getTeam()
            val pendingResult = teamRepository.getPendingMembers()
            val villageResult = teamRepository.getPendingVillages()
            val rolesResult = teamRepository.getCreatableRoles()

            val error = teamResult.exceptionOrNull()?.message
            _uiState.update {
                it.copy(
                    team = teamResult.getOrDefault(it.team),
                    pendingMembers = pendingResult.getOrDefault(emptyList()),
                    pendingVillages = villageResult.getOrDefault(emptyList()),
                    canAddMembers = rolesResult.getOrNull()?.isNotEmpty() ?: it.canAddMembers,
                    canAddVillage = rolesResult.getOrNull()?.isNotEmpty() ?: it.canAddVillage,
                    isLoading = false,
                    isRefreshing = false,
                    errorMessage = if (it.team.isEmpty()) error else null
                )
            }
        }
    }

    fun approveMember(id: Int, reject: Boolean) {
        _uiState.update { it.copy(busyMemberId = id) }
        viewModelScope.launch {
            val result = teamRepository.approveMember(id, reject)
            result.onSuccess {
                _uiState.update { s ->
                    s.copy(
                        busyMemberId = null,
                        pendingMembers = s.pendingMembers.filterNot { it.id == id },
                        actionMessage = if (reject) "Member rejected." else "Member approved."
                    )
                }
                load(isRefresh = true)
            }.onFailure { e ->
                _uiState.update { it.copy(busyMemberId = null, actionMessage = e.message) }
            }
        }
    }

    fun approveVillage(id: Int, reject: Boolean) {
        _uiState.update { it.copy(busyVillageId = id) }
        viewModelScope.launch {
            val result = teamRepository.approveVillage(id, reject)
            result.onSuccess {
                _uiState.update { s ->
                    s.copy(
                        busyVillageId = null,
                        pendingVillages = s.pendingVillages.filterNot { it.id == id },
                        actionMessage = if (reject) "Village rejected." else "Village approved."
                    )
                }
            }.onFailure { e ->
                _uiState.update { it.copy(busyVillageId = null, actionMessage = e.message) }
            }
        }
    }

    fun openVillageDialog() {
        _uiState.update { it.copy(villageDialogOpen = true) }
        viewModelScope.launch {
            val wards = teamRepository.getGeography("wards").getOrDefault(emptyList())
            _uiState.update { it.copy(villageWards = wards) }
        }
    }

    fun closeVillageDialog() = _uiState.update { it.copy(villageDialogOpen = false) }

    fun createVillage(wardId: Int, name: String) {
        _uiState.update { it.copy(villageSavingName = true) }
        viewModelScope.launch {
            teamRepository.createVillage(wardId, name.trim())
                .onSuccess {
                    _uiState.update {
                        it.copy(
                            villageSavingName = false,
                            villageDialogOpen = false,
                            actionMessage = if (it.canAddVillage) "Village submitted for approval." else "Village added."
                        )
                    }
                    load(isRefresh = true)
                }
                .onFailure { e ->
                    _uiState.update { it.copy(villageSavingName = false, actionMessage = e.message) }
                }
        }
    }

    fun clearActionMessage() = _uiState.update { it.copy(actionMessage = null) }
}
