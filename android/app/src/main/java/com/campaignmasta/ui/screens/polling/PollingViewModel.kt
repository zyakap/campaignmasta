package com.campaignmasta.ui.screens.polling

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.campaignmasta.data.local.dao.PollingLocationDao
import com.campaignmasta.data.local.dao.SyncQueueDao
import com.campaignmasta.data.local.entity.PollingLocationEntity
import com.campaignmasta.data.local.entity.SyncQueueEntity
import com.google.gson.Gson
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.UUID
import javax.inject.Inject

data class PollingUiState(
    val booths: List<PollingLocationEntity> = emptyList(),
    val selectedBooth: PollingLocationEntity? = null,
    val tallyInput: String = "",
    val isSubmitting: Boolean = false,
    val submitError: String? = null,
    val submitSuccess: Boolean = false
)

@HiltViewModel
class PollingViewModel @Inject constructor(
    private val pollingLocationDao: PollingLocationDao,
    private val syncQueueDao: SyncQueueDao,
    private val gson: Gson
) : ViewModel() {

    private val _uiState = MutableStateFlow(PollingUiState())
    val uiState: StateFlow<PollingUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            pollingLocationDao.getAllFlow().collect { booths ->
                _uiState.update { it.copy(booths = booths) }
            }
        }
    }

    fun selectBooth(booth: PollingLocationEntity) {
        _uiState.update { it.copy(selectedBooth = booth, tallyInput = booth.ourTally?.toString() ?: "", submitSuccess = false) }
    }

    fun closeBooth() {
        _uiState.update { it.copy(selectedBooth = null) }
    }

    fun onTallyInput(v: String) {
        _uiState.update { it.copy(tallyInput = v, submitError = null) }
    }

    fun submitPollingStatus(
        boothLocalId: String,
        scrutineerPresent: Boolean,
        boothOpen: Boolean,
        notes: String
    ) {
        val booth = _uiState.value.selectedBooth ?: return
        val tally = _uiState.value.tallyInput.toIntOrNull()
        _uiState.update { it.copy(isSubmitting = true, submitError = null) }
        viewModelScope.launch {
            val localId = UUID.randomUUID().toString()
            val now = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)
            val payload = mapOf(
                "polling_location" to booth.serverId,
                "status_time" to now,
                "scrutineer_present" to scrutineerPresent,
                "booth_open" to boothOpen,
                "our_tally" to tally,
                "notes" to notes
            )
            syncQueueDao.insert(
                SyncQueueEntity(
                    entityType = "polling_status",
                    operation = "CREATE",
                    localId = localId,
                    payload = gson.toJson(payload)
                )
            )
            // Update local tally
            if (tally != null) {
                pollingLocationDao.updateTally(booth.localId, tally)
            }
            _uiState.update { it.copy(isSubmitting = false, submitSuccess = true) }
        }
    }

    fun resetSubmit() {
        _uiState.update { it.copy(submitSuccess = false) }
    }
}
