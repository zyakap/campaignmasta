package com.campaignmasta.ui.screens.calls

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
import com.campaignmasta.data.local.entity.InfluencerEntity
import com.campaignmasta.ui.theme.PNGRed
import com.campaignmasta.ui.theme.SupportStrong
import com.campaignmasta.ui.theme.SupportWeak

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CallsScreen(
    onBack: () -> Unit,
    viewModel: CallViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    var showLogDialog by remember { mutableStateOf(false) }
    var selectedInfluencer by remember { mutableStateOf<InfluencerEntity?>(null) }

    LaunchedEffect(uiState.callLogged) {
        if (uiState.callLogged) {
            showLogDialog = false
            viewModel.resetCallLogged()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Calls Checklist") },
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
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = {
                    selectedInfluencer = null
                    showLogDialog = true
                },
                containerColor = PNGRed,
                contentColor = Color.White
            ) {
                Icon(Icons.Default.Phone, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Log Call")
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(bottom = 80.dp)
        ) {
            item {
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.surfaceVariant
                ) {
                    Text(
                        text = "${uiState.dueInfluencers.size} influencers due for contact",
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.padding(16.dp),
                        color = if (uiState.dueInfluencers.isEmpty()) SupportStrong else SupportWeak
                    )
                }
            }

            if (uiState.dueInfluencers.isEmpty()) {
                item {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(32.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Icon(
                                Icons.Default.CheckCircle,
                                contentDescription = null,
                                tint = SupportStrong,
                                modifier = Modifier.size(48.dp)
                            )
                            Spacer(modifier = Modifier.height(12.dp))
                            Text(
                                "All caught up! No calls due today.",
                                style = MaterialTheme.typography.bodyMedium,
                                color = Color.Gray
                            )
                        }
                    }
                }
            } else {
                items(uiState.dueInfluencers, key = { it.localId }) { influencer ->
                    InfluencerCallItem(
                        influencer = influencer,
                        onLogCall = {
                            selectedInfluencer = influencer
                            showLogDialog = true
                        }
                    )
                    HorizontalDivider()
                }
            }

            if (uiState.recentCalls.isNotEmpty()) {
                item {
                    Text(
                        text = "Recent Calls",
                        style = MaterialTheme.typography.titleSmall,
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
                        fontWeight = FontWeight.SemiBold
                    )
                }
                items(uiState.recentCalls, key = { "call_${it.localId}" }) { call ->
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = 16.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.Phone,
                            contentDescription = null,
                            tint = Color.Gray,
                            modifier = Modifier.size(20.dp)
                        )
                        Spacer(modifier = Modifier.width(12.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(call.personCalled, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
                            Text(
                                "${call.callOutcome} • ${call.callDatetime.take(10)}",
                                style = MaterialTheme.typography.bodySmall,
                                color = Color.Gray
                            )
                        }
                        if (call.syncStatus == "PENDING") {
                            Icon(Icons.Default.CloudUpload, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(14.dp))
                        }
                    }
                    HorizontalDivider()
                }
            }
        }
    }

    if (showLogDialog) {
        LogCallDialog(
            influencer = selectedInfluencer,
            isLoading = uiState.isLoggingCall,
            errorMessage = uiState.logCallError,
            onDismiss = { showLogDialog = false },
            onConfirm = { personCalled, phone, outcome, summary ->
                viewModel.logCall(
                    influencerId = selectedInfluencer?.serverId,
                    personCalled = personCalled,
                    phoneNumber = phone,
                    outcome = outcome,
                    summary = summary
                )
            }
        )
    }
}

@Composable
fun InfluencerCallItem(influencer: InfluencerEntity, onLogCall: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(influencer.fullName, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
            Text(
                "${influencer.communityRole} ${if (influencer.wardName.isNotBlank()) "• ${influencer.wardName}" else ""}",
                style = MaterialTheme.typography.bodySmall,
                color = Color.Gray
            )
            if (influencer.nextContactDueDate != null) {
                Text(
                    "Due: ${influencer.nextContactDueDate}",
                    style = MaterialTheme.typography.bodySmall,
                    color = SupportWeak
                )
            }
        }
        OutlinedButton(
            onClick = onLogCall,
            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
        ) {
            Icon(Icons.Default.Phone, contentDescription = null, modifier = Modifier.size(16.dp))
            Spacer(modifier = Modifier.width(4.dp))
            Text("Log", style = MaterialTheme.typography.labelMedium)
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun LogCallDialog(
    influencer: InfluencerEntity?,
    isLoading: Boolean,
    errorMessage: String?,
    onDismiss: () -> Unit,
    onConfirm: (String, String, String, String) -> Unit
) {
    var personCalled by remember { mutableStateOf(influencer?.fullName ?: "") }
    var phone by remember { mutableStateOf(influencer?.phone ?: "") }
    var outcome by remember { mutableStateOf("ANSWERED") }
    var summary by remember { mutableStateOf("") }

    val outcomeOptions = listOf("ANSWERED", "MISSED", "CALL_BACK", "SWITCHED_OFF", "WRONG_NUMBER")

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Log Call") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                errorMessage?.let {
                    Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                }
                OutlinedTextField(
                    value = personCalled,
                    onValueChange = { personCalled = it },
                    label = { Text("Person Called") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = phone,
                    onValueChange = { phone = it },
                    label = { Text("Phone Number") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                var expanded by remember { mutableStateOf(false) }
                ExposedDropdownMenuBox(
                    expanded = expanded,
                    onExpandedChange = { expanded = !expanded }
                ) {
                    OutlinedTextField(
                        value = outcome,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Outcome") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded) },
                        modifier = Modifier.menuAnchor().fillMaxWidth()
                    )
                    ExposedDropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                        outcomeOptions.forEach { opt ->
                            DropdownMenuItem(
                                text = { Text(opt.replace("_", " ")) },
                                onClick = { outcome = opt; expanded = false }
                            )
                        }
                    }
                }
                OutlinedTextField(
                    value = summary,
                    onValueChange = { summary = it },
                    label = { Text("Summary") },
                    modifier = Modifier.fillMaxWidth().height(80.dp),
                    maxLines = 3
                )
            }
        },
        confirmButton = {
            Button(
                onClick = { onConfirm(personCalled, phone, outcome, summary) },
                enabled = !isLoading
            ) {
                if (isLoading) {
                    CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                } else {
                    Text("Save")
                }
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}
