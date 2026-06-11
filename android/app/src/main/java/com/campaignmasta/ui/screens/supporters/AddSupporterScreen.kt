package com.campaignmasta.ui.screens.supporters

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.campaignmasta.ui.theme.PNGRed

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddSupporterScreen(
    onBack: () -> Unit,
    onSaved: () -> Unit,
    viewModel: SupporterViewModel = hiltViewModel()
) {
    val addState by viewModel.addState.collectAsStateWithLifecycle()

    LaunchedEffect(addState.saved) {
        if (addState.saved) {
            viewModel.resetAddForm()
            onSaved()
        }
    }

    val enrollmentOptions = listOf("UNKNOWN" to "Unknown", "VERIFIED_ENROLLED" to "Verified Enrolled", "NEEDS_RE_ENROLMENT" to "Needs Re-enrolment")
    val supportOptions = listOf("UNKNOWN" to "Unknown", "STRONG" to "Strong Supporter", "LEANING" to "Leaning", "UNDECIDED" to "Undecided", "NOT_SUPPORTIVE" to "Not Supportive")

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Add Supporter") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                actions = {
                    IconButton(
                        onClick = viewModel::saveSupporter,
                        enabled = !addState.isSaving
                    ) {
                        if (addState.isSaving) {
                            CircularProgressIndicator(
                                modifier = Modifier.size(20.dp),
                                color = Color.White,
                                strokeWidth = 2.dp
                            )
                        } else {
                            Icon(Icons.Default.Check, contentDescription = "Save", tint = Color.White)
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PNGRed,
                    titleContentColor = Color.White
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            addState.errorMessage?.let {
                Card(
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)
                ) {
                    Text(
                        text = it,
                        modifier = Modifier.padding(12.dp),
                        color = MaterialTheme.colorScheme.onErrorContainer,
                        style = MaterialTheme.typography.bodySmall
                    )
                }
            }

            SectionHeader("Personal Details")

            OutlinedTextField(
                value = addState.fullName,
                onValueChange = viewModel::onFullNameChange,
                label = { Text("Full Name *") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            OutlinedTextField(
                value = addState.phone,
                onValueChange = viewModel::onPhoneChange,
                label = { Text("Phone Number") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            SectionHeader("Location")

            OutlinedTextField(
                value = addState.ward,
                onValueChange = viewModel::onWardChange,
                label = { Text("Ward Name") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            OutlinedTextField(
                value = addState.clan,
                onValueChange = viewModel::onClanChange,
                label = { Text("Clan / Family Group") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            SectionHeader("Status")

            Text("Enrollment Status", style = MaterialTheme.typography.labelMedium)
            enrollmentOptions.forEach { (value, label) ->
                Row(
                    verticalAlignment = androidx.compose.ui.Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    RadioButton(
                        selected = addState.enrollmentStatus == value,
                        onClick = { viewModel.onEnrollmentStatusChange(value) }
                    )
                    Text(label, style = MaterialTheme.typography.bodyMedium)
                }
            }

            Spacer(modifier = Modifier.height(4.dp))

            Text("Support Status", style = MaterialTheme.typography.labelMedium)
            supportOptions.forEach { (value, label) ->
                Row(
                    verticalAlignment = androidx.compose.ui.Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    RadioButton(
                        selected = addState.supportStatus == value,
                        onClick = { viewModel.onSupportStatusChange(value) }
                    )
                    Text(label, style = MaterialTheme.typography.bodyMedium)
                }
            }

            SectionHeader("Notes")

            OutlinedTextField(
                value = addState.notes,
                onValueChange = viewModel::onNotesChange,
                label = { Text("Notes") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(100.dp),
                maxLines = 4
            )

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = viewModel::saveSupporter,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(52.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PNGRed),
                enabled = !addState.isSaving
            ) {
                Text("Save Supporter (Offline)", color = Color.White)
            }

            Text(
                text = "This supporter will be saved locally and synced when you reconnect.",
                style = MaterialTheme.typography.bodySmall,
                color = Color.Gray
            )

            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

@Composable
private fun SectionHeader(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleSmall,
        color = MaterialTheme.colorScheme.primary,
        modifier = Modifier.padding(top = 8.dp, bottom = 4.dp)
    )
    HorizontalDivider()
}
