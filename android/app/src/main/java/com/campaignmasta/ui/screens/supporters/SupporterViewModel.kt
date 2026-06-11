package com.campaignmasta.ui.screens.supporters

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.campaignmasta.data.local.entity.SupporterEntity
import com.campaignmasta.data.repository.SupporterRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SupportersUiState(
    val supporters: List<SupporterEntity> = emptyList(),
    val searchQuery: String = "",
    val isLoading: Boolean = false,
    val errorMessage: String? = null
)

data class AddSupporterUiState(
    val fullName: String = "",
    val phone: String = "",
    val ward: String = "",
    val wardId: Int? = null,
    val clan: String = "",
    val enrollmentStatus: String = "UNKNOWN",
    val supportStatus: String = "UNKNOWN",
    val notes: String = "",
    val isSaving: Boolean = false,
    val saved: Boolean = false,
    val errorMessage: String? = null
)

@HiltViewModel
class SupporterViewModel @Inject constructor(
    private val supporterRepository: SupporterRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(SupportersUiState())
    val uiState: StateFlow<SupportersUiState> = _uiState.asStateFlow()

    private val _addState = MutableStateFlow(AddSupporterUiState())
    val addState: StateFlow<AddSupporterUiState> = _addState.asStateFlow()

    private val searchQuery = MutableStateFlow("")

    init {
        viewModelScope.launch {
            supporterRepository.supporters
                .combine(searchQuery) { list, query ->
                    if (query.isBlank()) list
                    else list.filter {
                        it.fullName.contains(query, ignoreCase = true) ||
                        it.phone.contains(query) ||
                        it.ward.contains(query, ignoreCase = true) ||
                        it.clan.contains(query, ignoreCase = true)
                    }
                }
                .collect { filtered ->
                    _uiState.update { it.copy(supporters = filtered) }
                }
        }
    }

    fun onSearchChange(query: String) {
        searchQuery.value = query
        _uiState.update { it.copy(searchQuery = query) }
    }

    // Add supporter form fields
    fun onFullNameChange(v: String) = _addState.update { it.copy(fullName = v, errorMessage = null) }
    fun onPhoneChange(v: String) = _addState.update { it.copy(phone = v) }
    fun onWardChange(v: String) = _addState.update { it.copy(ward = v) }
    fun onClanChange(v: String) = _addState.update { it.copy(clan = v) }
    fun onEnrollmentStatusChange(v: String) = _addState.update { it.copy(enrollmentStatus = v) }
    fun onSupportStatusChange(v: String) = _addState.update { it.copy(supportStatus = v) }
    fun onNotesChange(v: String) = _addState.update { it.copy(notes = v) }

    fun saveSupporter() {
        val state = _addState.value
        if (state.fullName.isBlank()) {
            _addState.update { it.copy(errorMessage = "Full name is required.") }
            return
        }
        _addState.update { it.copy(isSaving = true) }
        viewModelScope.launch {
            try {
                supporterRepository.createOffline(
                    fullName = state.fullName.trim(),
                    phone = state.phone.trim(),
                    ward = state.ward.trim(),
                    wardId = state.wardId,
                    clan = state.clan.trim(),
                    enrollmentStatus = state.enrollmentStatus,
                    supportStatus = state.supportStatus,
                    notes = state.notes.trim()
                )
                _addState.update { it.copy(isSaving = false, saved = true) }
            } catch (e: Exception) {
                _addState.update { it.copy(isSaving = false, errorMessage = e.message ?: "Save failed.") }
            }
        }
    }

    fun resetAddForm() {
        _addState.value = AddSupporterUiState()
    }
}
