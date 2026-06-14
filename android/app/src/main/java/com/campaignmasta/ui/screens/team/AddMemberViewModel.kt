package com.campaignmasta.ui.screens.team

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.campaignmasta.data.remote.dto.CreatableRoleDto
import com.campaignmasta.data.remote.dto.CreateTeamMemberRequest
import com.campaignmasta.data.remote.dto.GeoItemDto
import com.campaignmasta.data.repository.TeamRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/** Which geography level a role needs the user to choose. */
private val ROLE_DEPTH = mapOf(
    "DISTRICT_COORDINATOR" to 1,
    "LLG_COORDINATOR" to 2,
    "WARD_COORDINATOR" to 3,
    "VILLAGE_COORDINATOR" to 4,
    "VOLUNTEER" to 4,
    "SCRUTINEER" to 3
)

data class AddMemberUiState(
    val fullName: String = "",
    val phone: String = "",
    val roles: List<CreatableRoleDto> = emptyList(),
    val selectedRole: CreatableRoleDto? = null,

    val districts: List<GeoItemDto> = emptyList(),
    val llgs: List<GeoItemDto> = emptyList(),
    val wards: List<GeoItemDto> = emptyList(),
    val villages: List<GeoItemDto> = emptyList(),
    val selectedDistrict: GeoItemDto? = null,
    val selectedLlg: GeoItemDto? = null,
    val selectedWard: GeoItemDto? = null,
    val selectedVillage: GeoItemDto? = null,

    val isLoading: Boolean = true,
    val isSaving: Boolean = false,
    val saved: Boolean = false,
    val errorMessage: String? = null
) {
    /** How deep the geography picker must go for the chosen role. */
    val requiredDepth: Int get() = ROLE_DEPTH[selectedRole?.value] ?: 0
}

@HiltViewModel
class AddMemberViewModel @Inject constructor(
    private val teamRepository: TeamRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(AddMemberUiState())
    val uiState: StateFlow<AddMemberUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            val roles = teamRepository.getCreatableRoles().getOrDefault(emptyList())
            val districts = teamRepository.getGeography("districts").getOrDefault(emptyList())
            _uiState.update { it.copy(roles = roles, districts = districts, isLoading = false) }
        }
    }

    fun onFullNameChange(v: String) = _uiState.update { it.copy(fullName = v, errorMessage = null) }
    fun onPhoneChange(v: String) = _uiState.update { it.copy(phone = v) }

    fun onRoleSelected(role: CreatableRoleDto) {
        _uiState.update {
            it.copy(
                selectedRole = role,
                // Reset geography below district when the role changes.
                selectedLlg = null, selectedWard = null, selectedVillage = null,
                llgs = emptyList(), wards = emptyList(), villages = emptyList()
            )
        }
    }

    fun onDistrictSelected(item: GeoItemDto) {
        _uiState.update {
            it.copy(
                selectedDistrict = item,
                selectedLlg = null, selectedWard = null, selectedVillage = null,
                llgs = emptyList(), wards = emptyList(), villages = emptyList()
            )
        }
        viewModelScope.launch {
            val llgs = teamRepository.getGeography("llgs", item.id).getOrDefault(emptyList())
            _uiState.update { it.copy(llgs = llgs) }
        }
    }

    fun onLlgSelected(item: GeoItemDto) {
        _uiState.update {
            it.copy(
                selectedLlg = item,
                selectedWard = null, selectedVillage = null,
                wards = emptyList(), villages = emptyList()
            )
        }
        viewModelScope.launch {
            val wards = teamRepository.getGeography("wards", item.id).getOrDefault(emptyList())
            _uiState.update { it.copy(wards = wards) }
        }
    }

    fun onWardSelected(item: GeoItemDto) {
        _uiState.update {
            it.copy(selectedWard = item, selectedVillage = null, villages = emptyList())
        }
        viewModelScope.launch {
            val villages = teamRepository.getGeography("villages", item.id).getOrDefault(emptyList())
            _uiState.update { it.copy(villages = villages) }
        }
    }

    fun onVillageSelected(item: GeoItemDto) = _uiState.update { it.copy(selectedVillage = item) }

    fun save() {
        val s = _uiState.value
        when {
            s.fullName.isBlank() -> return fail("Please enter the person's full name.")
            s.selectedRole == null -> return fail("Please choose a role.")
            s.requiredDepth >= 1 && s.selectedDistrict == null -> return fail("Please choose a district.")
            s.requiredDepth >= 2 && s.selectedLlg == null -> return fail("Please choose an LLG.")
            s.requiredDepth >= 3 && s.selectedWard == null -> return fail("Please choose a ward.")
            s.requiredDepth >= 4 && s.selectedVillage == null -> return fail("Please choose a village / area.")
        }
        _uiState.update { it.copy(isSaving = true, errorMessage = null) }
        viewModelScope.launch {
            val request = CreateTeamMemberRequest(
                fullName = s.fullName.trim(),
                role = s.selectedRole!!.value,
                phone = s.phone.trim(),
                district = s.selectedDistrict?.id,
                llg = s.selectedLlg?.id,
                ward = s.selectedWard?.id,
                village = s.selectedVillage?.id
            )
            teamRepository.createMember(request)
                .onSuccess { _uiState.update { it.copy(isSaving = false, saved = true) } }
                .onFailure { e -> _uiState.update { it.copy(isSaving = false, errorMessage = e.message) } }
        }
    }

    private fun fail(message: String) {
        _uiState.update { it.copy(errorMessage = message) }
    }
}
