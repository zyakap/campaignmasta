package com.campaignmasta.ui.screens.polling

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
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.campaignmasta.data.local.entity.PollingLocationEntity
import com.campaignmasta.ui.theme.PNGRed
import com.campaignmasta.ui.theme.SupportStrong
import com.campaignmasta.ui.theme.SupportMedium
import com.campaignmasta.ui.theme.SupportWeak

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PollingScreen(
    onBack: () -> Unit,
    viewModel: PollingViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    if (uiState.selectedBooth != null) {
        PollingBoothDetailScreen(
            booth = uiState.selectedBooth!!,
            tallyInput = uiState.tallyInput,
            isSubmitting = uiState.isSubmitting,
            submitError = uiState.submitError,
            submitSuccess = uiState.submitSuccess,
            onTallyChange = viewModel::onTallyInput,
            onSubmit = { scrutineerPresent, boothOpen, notes ->
                viewModel.submitPollingStatus(
                    boothLocalId = uiState.selectedBooth!!.localId,
                    scrutineerPresent = scrutineerPresent,
                    boothOpen = boothOpen,
                    notes = notes
                )
            },
            onBack = viewModel::closeBooth,
            onResetSubmit = viewModel::resetSubmit
        )
        return
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Polling Day") },
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
        if (uiState.booths.isEmpty()) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Default.HowToVote, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.LightGray)
                    Spacer(Modifier.height(16.dp))
                    Text("No polling booths loaded. Sync to pull data.", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                }
            }
        } else {
            // Summary row
            Column(modifier = Modifier.padding(padding)) {
                val checkedIn = uiState.booths.count { it.scrutineerCheckedIn }
                Surface(
                    modifier = Modifier.fillMaxWidth(),
                    color = MaterialTheme.colorScheme.surfaceVariant
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceEvenly
                    ) {
                        PollingStatCard("Total Booths", uiState.booths.size.toString())
                        PollingStatCard("Scrutineers In", "$checkedIn", SupportStrong)
                        val totalTally = uiState.booths.mapNotNull { it.ourTally }.sum()
                        PollingStatCard("Our Tally", "$totalTally", PNGRed)
                    }
                }
                LazyColumn {
                    items(uiState.booths, key = { it.localId }) { booth ->
                        PollingBoothItem(booth = booth, onClick = { viewModel.selectBooth(booth) })
                        HorizontalDivider()
                    }
                }
            }
        }
    }
}

@Composable
fun PollingStatCard(label: String, value: String, valueColor: Color = MaterialTheme.colorScheme.onSurface) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(value, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = valueColor)
        Text(label, style = MaterialTheme.typography.labelSmall, color = Color.Gray)
    }
}

@Composable
fun PollingBoothItem(booth: PollingLocationEntity, onClick: () -> Unit) {
    val riskColor = when (booth.securityRisk) {
        "HIGH" -> SupportWeak
        "MODERATE" -> SupportMedium
        "REFUSED" -> Color(0xFF6A1B9A)
        else -> SupportStrong
    }
    Row(
        modifier = Modifier.fillMaxWidth().clickable(onClick = onClick).padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            imageVector = if (booth.scrutineerCheckedIn) Icons.Default.CheckCircle else Icons.Default.RadioButtonUnchecked,
            contentDescription = null,
            tint = if (booth.scrutineerCheckedIn) SupportStrong else Color.Gray,
            modifier = Modifier.size(24.dp)
        )
        Spacer(Modifier.width(12.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(booth.name, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
            Text(
                "${booth.wardName}${if (booth.scrutineerName.isNotBlank()) " • ${booth.scrutineerName}" else ""}",
                style = MaterialTheme.typography.bodySmall,
                color = Color.Gray
            )
            if (booth.ourTally != null) {
                Text("Our tally: ${booth.ourTally}", style = MaterialTheme.typography.bodySmall, color = PNGRed, fontWeight = FontWeight.SemiBold)
            }
        }
        Surface(color = riskColor.copy(alpha = 0.12f), shape = MaterialTheme.shapes.small) {
            Text(
                text = booth.securityRisk,
                style = MaterialTheme.typography.labelSmall,
                color = riskColor,
                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
            )
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.LightGray)
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PollingBoothDetailScreen(
    booth: PollingLocationEntity,
    tallyInput: String,
    isSubmitting: Boolean,
    submitError: String?,
    submitSuccess: Boolean,
    onTallyChange: (String) -> Unit,
    onSubmit: (Boolean, Boolean, String) -> Unit,
    onBack: () -> Unit,
    onResetSubmit: () -> Unit
) {
    var scrutineerPresent by remember { mutableStateOf(booth.scrutineerCheckedIn) }
    var boothOpen by remember { mutableStateOf(false) }
    var notes by remember { mutableStateOf("") }

    LaunchedEffect(submitSuccess) {
        if (submitSuccess) {
            onResetSubmit()
            onBack()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(booth.name) },
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
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item {
                Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)) {
                    Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Text("Booth Information", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                        Text("Ward: ${booth.wardName}", style = MaterialTheme.typography.bodyMedium)
                        if (booth.scrutineerName.isNotBlank()) Text("Scrutineer: ${booth.scrutineerName}", style = MaterialTheme.typography.bodyMedium)
                        if (booth.gpsCoordinates.isNotBlank()) Text("GPS: ${booth.gpsCoordinates}", style = MaterialTheme.typography.bodySmall, color = Color.Gray)
                        Text("Security Risk: ${booth.securityRisk}", style = MaterialTheme.typography.bodyMedium)
                        if (booth.expectedTurnout != null) Text("Expected Turnout: ${booth.expectedTurnout}", style = MaterialTheme.typography.bodyMedium)
                    }
                }
            }

            item {
                Text("Status Update", style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                HorizontalDivider()
            }

            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Scrutineer Present", style = MaterialTheme.typography.bodyMedium)
                    Switch(checked = scrutineerPresent, onCheckedChange = { scrutineerPresent = it })
                }
            }
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text("Booth Open", style = MaterialTheme.typography.bodyMedium)
                    Switch(checked = boothOpen, onCheckedChange = { boothOpen = it })
                }
            }

            item {
                OutlinedTextField(
                    value = tallyInput,
                    onValueChange = onTallyChange,
                    label = { Text("Our Tally (votes observed)") },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth(),
                    leadingIcon = { Icon(Icons.Default.HowToVote, contentDescription = null) }
                )
            }

            item {
                OutlinedTextField(
                    value = notes,
                    onValueChange = { notes = it },
                    label = { Text("Notes / Issues") },
                    modifier = Modifier.fillMaxWidth().height(80.dp),
                    maxLines = 3
                )
            }

            submitError?.let {
                item {
                    Text(it, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                }
            }

            item {
                Button(
                    onClick = { onSubmit(scrutineerPresent, boothOpen, notes) },
                    modifier = Modifier.fillMaxWidth().height(52.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = PNGRed),
                    enabled = !isSubmitting
                ) {
                    if (isSubmitting) {
                        CircularProgressIndicator(modifier = Modifier.size(20.dp), color = Color.White, strokeWidth = 2.dp)
                    } else {
                        Text("Submit Status Update", color = Color.White)
                    }
                }
            }

            item {
                Text(
                    text = "Status will be synced to command centre when connected.",
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Gray
                )
            }
        }
    }
}
