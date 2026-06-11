package com.campaignmasta.ui.screens.messages

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.campaignmasta.data.local.entity.MessageEntity
import com.campaignmasta.ui.theme.PNGRed
import com.campaignmasta.ui.theme.SupportStrong
import com.campaignmasta.ui.theme.SupportWeak

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MessagesScreen(
    onBack: () -> Unit,
    viewModel: MessageViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    if (uiState.selectedMessage != null) {
        MessageDetailScreen(
            message = uiState.selectedMessage!!,
            onBack = viewModel::closeMessage,
            onAcknowledge = { viewModel.acknowledgeMessage(uiState.selectedMessage!!) }
        )
        return
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("Messages")
                        if (uiState.unreadCount > 0) {
                            Spacer(modifier = Modifier.width(8.dp))
                            Badge { Text("${uiState.unreadCount}") }
                        }
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PNGRed,
                    titleContentColor = Color.White
                )
            )
        }
    ) { padding ->
        if (uiState.messages.isEmpty()) {
            Box(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.Inbox, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.LightGray)
                    Spacer(modifier = Modifier.height(16.dp))
                    Text("No messages yet", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                }
            }
        } else {
            LazyColumn(modifier = Modifier.padding(padding)) {
                items(uiState.messages, key = { it.localId }) { message ->
                    MessageListItem(
                        message = message,
                        onClick = { viewModel.openMessage(message) }
                    )
                    HorizontalDivider()
                }
            }
        }
    }
}

@Composable
fun MessageListItem(message: MessageEntity, onClick: () -> Unit) {
    val priorityColor = when (message.priority) {
        "URGENT" -> SupportWeak
        "IMPORTANT" -> Color(0xFFE65100)
        else -> Color.Gray
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(horizontal = 16.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = if (message.isRead) Icons.Default.MailOutline else Icons.Default.Mail,
            contentDescription = null,
            tint = if (message.isRead) Color.Gray else PNGRed,
            modifier = Modifier.size(24.dp)
        )
        Spacer(modifier = Modifier.width(12.dp))
        Column(modifier = Modifier.weight(1f)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                Text(
                    text = message.subject,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = if (message.isRead) FontWeight.Normal else FontWeight.SemiBold
                )
                if (message.priority != "NORMAL") {
                    Surface(
                        color = priorityColor.copy(alpha = 0.1f),
                        shape = MaterialTheme.shapes.extraSmall
                    ) {
                        Text(
                            text = message.priority,
                            style = MaterialTheme.typography.labelSmall,
                            color = priorityColor,
                            modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp)
                        )
                    }
                }
            }
            Text(
                text = "${message.senderName.ifBlank { "Campaign HQ" }} • ${message.sentAt?.take(10) ?: ""}",
                style = MaterialTheme.typography.bodySmall,
                color = Color.Gray
            )
            if (message.acknowledgementRequired && !message.isAcknowledged) {
                Text(
                    text = "Acknowledgement required",
                    style = MaterialTheme.typography.bodySmall,
                    color = SupportWeak,
                    fontWeight = FontWeight.Medium
                )
            }
        }
        if (!message.isRead) {
            Box(
                modifier = Modifier.size(10.dp),
                contentAlignment = Alignment.Center
            ) {
                Surface(
                    modifier = Modifier.size(8.dp),
                    shape = MaterialTheme.shapes.extraSmall,
                    color = PNGRed
                ) {}
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MessageDetailScreen(
    message: MessageEntity,
    onBack: () -> Unit,
    onAcknowledge: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(message.subject, maxLines = 1) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PNGRed,
                    titleContentColor = Color.White
                )
            )
        },
        bottomBar = {
            if (message.acknowledgementRequired && !message.isAcknowledged) {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    shadowElevation = 8.dp
                ) {
                    Button(
                        onClick = onAcknowledge,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = SupportStrong)
                    ) {
                        Icon(Icons.Default.CheckCircle, contentDescription = null)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("Mark as Acknowledged")
                    }
                }
            }
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            // Metadata
            Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) {
                Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    MetaRow("From", message.senderName.ifBlank { "Campaign HQ" })
                    MetaRow("Priority", message.priority)
                    MetaRow("Sent", message.sentAt?.take(16)?.replace("T", " ") ?: "—")
                    if (message.isAcknowledged) {
                        MetaRow("Status", "Acknowledged", SupportStrong)
                    } else if (message.isRead) {
                        MetaRow("Status", "Read")
                    } else {
                        MetaRow("Status", "Unread")
                    }
                }
            }
            // Body
            Text(
                text = message.body,
                style = MaterialTheme.typography.bodyLarge
            )
        }
    }
}

@Composable
private fun MetaRow(label: String, value: String, valueColor: Color = Color.Unspecified) {
    Row {
        Text(
            text = "$label: ",
            style = MaterialTheme.typography.bodySmall,
            fontWeight = FontWeight.SemiBold,
            color = Color.Gray
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodySmall,
            color = if (valueColor == Color.Unspecified) MaterialTheme.colorScheme.onSurface else valueColor
        )
    }
}
