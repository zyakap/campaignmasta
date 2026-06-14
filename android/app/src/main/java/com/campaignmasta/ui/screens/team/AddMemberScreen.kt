package com.campaignmasta.ui.screens.team

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Info
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.campaignmasta.ui.theme.PNGRed

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddMemberScreen(
    onBack: () -> Unit,
    onSaved: () -> Unit,
    viewModel: AddMemberViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    LaunchedEffect(state.saved) { if (state.saved) onSaved() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Add Team Member") },
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
        if (state.isLoading) {
            Box(Modifier.fillMaxSize().padding(padding), Alignment.Center) {
                CircularProgressIndicator(color = PNGRed)
            }
            return@Scaffold
        }

        Column(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            OutlinedTextField(
                value = state.fullName,
                onValueChange = viewModel::onFullNameChange,
                label = { Text("Full name *") },
                singleLine = true,
                keyboardOptions = KeyboardOptions(capitalization = KeyboardCapitalization.Words),
                modifier = Modifier.fillMaxWidth()
            )

            OutlinedTextField(
                value = state.phone,
                onValueChange = viewModel::onPhoneChange,
                label = { Text("Phone number") },
                singleLine = true,
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Phone, imeAction = ImeAction.Next),
                modifier = Modifier.fillMaxWidth()
            )

            LabeledDropdown(
                label = "Role *",
                options = state.roles,
                selected = state.selectedRole,
                optionLabel = { it.label },
                onSelect = viewModel::onRoleSelected
            )

            // Cascading geography — only shows the levels the chosen role needs.
            val depth = state.requiredDepth
            if (depth >= 1) {
                LabeledDropdown(
                    label = "District *",
                    options = state.districts,
                    selected = state.selectedDistrict,
                    optionLabel = { it.name },
                    onSelect = viewModel::onDistrictSelected
                )
            }
            if (depth >= 2) {
                LabeledDropdown(
                    label = "LLG *",
                    options = state.llgs,
                    selected = state.selectedLlg,
                    optionLabel = { it.name },
                    onSelect = viewModel::onLlgSelected,
                    enabled = state.selectedDistrict != null
                )
            }
            if (depth >= 3) {
                LabeledDropdown(
                    label = "Ward *",
                    options = state.wards,
                    selected = state.selectedWard,
                    optionLabel = { it.name },
                    onSelect = viewModel::onWardSelected,
                    enabled = state.selectedLlg != null
                )
            }
            if (depth >= 4) {
                LabeledDropdown(
                    label = "Village / area *",
                    options = state.villages,
                    selected = state.selectedVillage,
                    optionLabel = { it.name },
                    onSelect = viewModel::onVillageSelected,
                    enabled = state.selectedWard != null
                )
            }

            // Helper note about approval, in plain language.
            Surface(color = Color(0xFFEFF6FF), shape = RoundedCornerShape(10.dp)) {
                Row(Modifier.padding(12.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Info, contentDescription = null, tint = Color(0xFF1E40AF), modifier = Modifier.size(20.dp))
                    Spacer(Modifier.width(8.dp))
                    Text(
                        "The person you add will be sent to your supervisor for approval before they can start.",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color(0xFF1E40AF)
                    )
                }
            }

            if (state.errorMessage != null) {
                Text(state.errorMessage!!, color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodyMedium)
            }

            Button(
                onClick = viewModel::save,
                enabled = !state.isSaving,
                modifier = Modifier.fillMaxWidth().height(52.dp),
                colors = ButtonDefaults.buttonColors(containerColor = PNGRed)
            ) {
                if (state.isSaving) CircularProgressIndicator(Modifier.size(20.dp), color = Color.White, strokeWidth = 2.dp)
                else Text("Save Member", style = MaterialTheme.typography.titleMedium)
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}
