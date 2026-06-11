package com.campaignmasta.ui.screens.wards

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.campaignmasta.data.local.entity.WardProfileEntity
import com.campaignmasta.ui.theme.PNGRed
import com.campaignmasta.ui.theme.SupportStrong
import com.campaignmasta.ui.theme.SupportMedium
import com.campaignmasta.ui.theme.SupportWeak
import com.campaignmasta.ui.theme.SupportUnknown

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WardBriefsScreen(
    onBack: () -> Unit,
    viewModel: WardViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    if (uiState.selectedWard != null) {
        WardDetailScreen(
            ward = uiState.selectedWard!!,
            onBack = viewModel::closeWard
        )
        return
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Ward Briefs") },
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
        Column(modifier = Modifier.fillMaxSize().padding(padding)) {
            OutlinedTextField(
                value = uiState.searchQuery,
                onValueChange = viewModel::onSearchChange,
                placeholder = { Text("Search wards…") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                singleLine = true,
                modifier = Modifier.fillMaxWidth().padding(16.dp)
            )
            if (uiState.wards.isEmpty()) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(Icons.Default.Map, contentDescription = null, modifier = Modifier.size(64.dp), tint = Color.LightGray)
                        Spacer(modifier = Modifier.height(16.dp))
                        Text("No ward briefs yet. Sync to load.", style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
                    }
                }
            } else {
                LazyColumn {
                    items(uiState.wards, key = { it.localId }) { ward ->
                        WardBriefItem(ward = ward, onClick = { viewModel.selectWard(ward) })
                        HorizontalDivider()
                    }
                }
            }
        }
    }
}

@Composable
fun WardBriefItem(ward: WardProfileEntity, onClick: () -> Unit) {
    val strengthColor = when (ward.supportStrength) {
        "STRONG" -> SupportStrong
        "MEDIUM" -> SupportMedium
        "WEAK" -> SupportWeak
        else -> SupportUnknown
    }
    Row(
        modifier = Modifier.fillMaxWidth().clickable(onClick = onClick).padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Strength indicator
        Surface(
            modifier = Modifier.size(8.dp),
            shape = MaterialTheme.shapes.extraSmall,
            color = strengthColor
        ) {}
        Spacer(modifier = Modifier.width(12.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(ward.wardName, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
            Text(
                "${ward.llgName}${if (ward.councillorName.isNotBlank()) " • Cllr ${ward.councillorName}" else ""}",
                style = MaterialTheme.typography.bodySmall,
                color = Color.Gray
            )
            if (ward.estimatedVotingPopulation != null) {
                Text("~${ward.estimatedVotingPopulation} voters", style = MaterialTheme.typography.bodySmall, color = Color.Gray)
            }
        }
        Surface(
            color = strengthColor.copy(alpha = 0.12f),
            shape = MaterialTheme.shapes.small
        ) {
            Text(
                text = ward.supportStrength,
                style = MaterialTheme.typography.labelSmall,
                color = strengthColor,
                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
            )
        }
        Icon(Icons.Default.ChevronRight, contentDescription = null, tint = Color.LightGray)
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WardDetailScreen(ward: WardProfileEntity, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(ward.wardName) },
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
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            item { WardInfoCard(ward) }
            if (ward.mainCommunityIssues.isNotBlank()) {
                item { WardSection("Community Issues", ward.mainCommunityIssues, Icons.Default.Warning) }
            }
            if (ward.notesForCandidate.isNotBlank()) {
                item { WardSection("Notes for Candidate", ward.notesForCandidate, Icons.Default.Note) }
            }
            if (ward.keyClans.isNotBlank()) {
                item { WardSection("Key Clans", ward.keyClans, Icons.Default.People) }
            }
            if (ward.keyChurches.isNotBlank()) {
                item { WardSection("Key Churches", ward.keyChurches, Icons.Default.Church) }
            }
            if (ward.securityConcerns.isNotBlank()) {
                item { WardSection("Security Concerns", ward.securityConcerns, Icons.Default.Security) }
            }
        }
    }
}

@Composable
private fun WardInfoCard(ward: WardProfileEntity) {
    val strengthColor = when (ward.supportStrength) {
        "STRONG" -> SupportStrong
        "MEDIUM" -> SupportMedium
        "WEAK" -> SupportWeak
        else -> SupportUnknown
    }
    Card(colors = CardDefaults.cardColors(containerColor = strengthColor.copy(alpha = 0.08f))) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Row(horizontalArrangement = Arrangement.SpaceBetween, modifier = Modifier.fillMaxWidth()) {
                Text("Support Strength", style = MaterialTheme.typography.labelMedium, color = Color.Gray)
                Text(ward.supportStrength, style = MaterialTheme.typography.labelMedium, color = strengthColor, fontWeight = FontWeight.Bold)
            }
            if (ward.councillorName.isNotBlank()) {
                InfoRow("Councillor", ward.councillorName)
            }
            if (ward.populationEstimate != null) {
                InfoRow("Population (est.)", "${ward.populationEstimate}")
            }
            if (ward.estimatedVotingPopulation != null) {
                InfoRow("Voting Population (est.)", "${ward.estimatedVotingPopulation}")
            }
            InfoRow("LLG", ward.llgName)
        }
    }
}

@Composable
private fun WardSection(title: String, content: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Column {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Icon(icon, contentDescription = null, tint = PNGRed, modifier = Modifier.size(18.dp))
            Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
        }
        Spacer(modifier = Modifier.height(4.dp))
        Text(content, style = MaterialTheme.typography.bodyMedium)
        HorizontalDivider(modifier = Modifier.padding(top = 12.dp))
    }
}

@Composable
private fun InfoRow(label: String, value: String) {
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        Text("$label:", style = MaterialTheme.typography.bodySmall, color = Color.Gray, fontWeight = FontWeight.Medium)
        Text(value, style = MaterialTheme.typography.bodySmall)
    }
}
