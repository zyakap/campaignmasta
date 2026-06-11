package com.campaignmasta.ui.screens.calls

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.campaignmasta.data.local.dao.CallLogDao
import com.campaignmasta.data.local.dao.InfluencerDao
import com.campaignmasta.data.local.dao.SyncQueueDao
import com.campaignmasta.data.local.entity.CallLogEntity
import com.campaignmasta.data.local.entity.InfluencerEntity
import com.campaignmasta.data.local.entity.SyncQueueEntity
import com.google.gson.Gson
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.UUID
import javax.inject.Inject

data class CallsUiState(
    val dueInfluencers: List<InfluencerEntity> = emptyList(),
    val recentCalls: List<CallLogEntity> = emptyList(),
    val isLoggingCall: Boolean = false,
    val logCallError: String? = null,
    val callLogged: Boolean = false
)

@HiltViewModel
class CallViewModel @Inject constructor(
    private val influencerDao: InfluencerDao,
    private val callLogDao: CallLogDao,
    private val syncQueueDao: SyncQueueDao,
    private val gson: Gson
) : ViewModel() {

    private val _uiState = MutableStateFlow(CallsUiState())
    val uiState: StateFlow<CallsUiState> = _uiState.asStateFlow()

    init {
        val today = LocalDate.now().toString()
        viewModelScope.launch {
            combine(
                influencerDao.getDueFlow(today),
                callLogDao.getAllFlow()
            ) { due, calls -> Pair(due, calls.take(20)) }
                .collect { (due, calls) ->
                    _uiState.update { it.copy(dueInfluencers = due, recentCalls = calls) }
                }
        }
    }

    fun logCall(
        influencerId: Int?,
        personCalled: String,
        phoneNumber: String,
        outcome: String,
        summary: String
    ) {
        if (personCalled.isBlank()) {
            _uiState.update { it.copy(logCallError = "Person name is required.") }
            return
        }
        _uiState.update { it.copy(isLoggingCall = true, logCallError = null) }
        viewModelScope.launch {
            val localId = UUID.randomUUID().toString()
            val callDatetime = LocalDateTime.now().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME)
            val entity = CallLogEntity(
                localId = localId,
                personCalled = personCalled,
                phoneNumber = phoneNumber,
                callDatetime = callDatetime,
                callOutcome = outcome,
                discussionSummary = summary,
                influencerId = influencerId,
                syncStatus = "PENDING"
            )
            callLogDao.insert(entity)

            val payload = mapOf(
                "person_called" to personCalled,
                "phone_number" to phoneNumber,
                "call_datetime" to callDatetime,
                "call_outcome" to outcome,
                "discussion_summary" to summary,
                "influencer" to influencerId
            )
            syncQueueDao.insert(
                SyncQueueEntity(
                    entityType = "call_log",
                    operation = "CREATE",
                    localId = localId,
                    payload = gson.toJson(payload)
                )
            )
            _uiState.update { it.copy(isLoggingCall = false, callLogged = true) }
        }
    }

    fun resetCallLogged() {
        _uiState.update { it.copy(callLogged = false) }
    }
}
