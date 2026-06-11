package com.campaignmasta.ui.screens.messages

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.campaignmasta.data.local.entity.MessageEntity
import com.campaignmasta.data.repository.MessageRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class MessagesUiState(
    val messages: List<MessageEntity> = emptyList(),
    val unreadCount: Int = 0,
    val selectedMessage: MessageEntity? = null,
    val isLoading: Boolean = false
)

@HiltViewModel
class MessageViewModel @Inject constructor(
    private val messageRepository: MessageRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(MessagesUiState())
    val uiState: StateFlow<MessagesUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            combine(
                messageRepository.messages,
                messageRepository.unreadCount
            ) { msgs, unread -> Pair(msgs, unread) }
                .collect { (msgs, unread) ->
                    _uiState.update { it.copy(messages = msgs, unreadCount = unread) }
                }
        }
    }

    fun openMessage(message: MessageEntity) {
        _uiState.update { it.copy(selectedMessage = message) }
        // Mark as read locally (push will happen in background sync)
        if (!message.isRead) {
            viewModelScope.launch {
                messageRepository.markReadLocally(message.localId)
            }
        }
    }

    fun closeMessage() {
        _uiState.update { it.copy(selectedMessage = null) }
    }

    fun acknowledgeMessage(message: MessageEntity) {
        viewModelScope.launch {
            messageRepository.markAcknowledgedLocally(message.localId)
        }
    }
}
