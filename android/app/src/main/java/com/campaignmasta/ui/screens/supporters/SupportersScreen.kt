package com.campaignmasta.ui.screens.supporters

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
import com.campaignmasta.data.local.entity.SupporterEntity
import com.campaignmasta.ui.theme.PNGRed
import com.campaignmasta.ui.theme.SupportStrong
import com.campaignmasta.ui.theme.SupportMedium
import com.campaignmasta.ui.theme.SupportWeak
import com.campaignmasta.ui.theme.SupportUnknown

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SupportersScreen(
    onBack: () -> Unit,
    onAddSupporter: () -> Unit,
    viewModel: SupporterViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Supporters (${uiState.supporters.size})") },
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
                onClick = onAddSupporter,
                containerColor = PNGRed,
                contentColor = Color.White
            ) {
                Icon(Icons.Default.PersonAdd, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Add Supporter")
            }
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Search bar
            OutlinedTextField(
                value = uiState.searchQuery,
                onValueChange = viewModel::onSearchChange,
                placeholder = { Text("Search name, ward, clan…") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                singleLine = true,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp)
            )

            if (uiState.supporters.isEmpty()) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Icon(
                            Icons.Default.People,
                            contentDescription = null,
                            modifier = Modifier.size(64.dp),
                            tint = Color.LightGray
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = if (uiState.searchQuery.isNotBlank()) "No supporters match your search"
                                else "No supporters yet. Tap + to add one.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color.Gray
                        )
                    }
                }
            } else {
                LazyColumn(contentPadding = PaddingValues(bottom = 80.dp)) {
                    items(uiState.supporters, key = { it.localId }) { supporter ->
                        SupporterListItem(supporter = supporter)
                        HorizontalDivider()
                    }
                }
            }
        }
    }
}

@Composable
fun SupporterListItem(supporter: SupporterEntity) {
    val statusColor = when (supporter.supportStatus) {
        "STRONG" -> SupportStrong
        "LEANING" -> SupportMedium
        "NOT_SUPPORTIVE" -> SupportWeak
        else -> SupportUnknown
    }

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Avatar circle
        Surface(
            modifier = Modifier.size(44.dp),
            shape = MaterialTheme.shapes.medium,
            color = statusColor.copy(alpha = 0.15f)
        ) {
            Box(contentAlignment = Alignment.Center) {
                Text(
                    text = supporter.fullName.first().uppercase(),
                    style = MaterialTheme.typography.titleMedium,
                    color = statusColor,
                    fontWeight = FontWeight.Bold
                )
            }
        }

        Spacer(modifier = Modifier.width(12.dp))

        Column(modifier = Modifier.weight(1f)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Text(
                    text = supporter.fullName,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Medium
                )
                if (supporter.syncStatus == "PENDING") {
                    Icon(
                        Icons.Default.CloudUpload,
                        contentDescription = "Pending sync",
                        modifier = Modifier.size(14.dp),
                        tint = Color.Gray
                    )
                }
            }
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                if (supporter.ward.isNotBlank()) {
                    Text(
                        text = supporter.ward,
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.Gray
                    )
                }
                if (supporter.clan.isNotBlank()) {
                    Text(
                        text = "• ${supporter.clan}",
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.Gray
                    )
                }
            }
            if (supporter.phone.isNotBlank()) {
                Text(
                    text = supporter.phone,
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Gray
                )
            }
        }

        // Support status badge
        Surface(
            color = statusColor.copy(alpha = 0.12f),
            shape = MaterialTheme.shapes.small
        ) {
            Text(
                text = supporter.supportStatus.replace("_", " ").lowercase()
                    .replaceFirstChar { it.uppercase() },
                style = MaterialTheme.typography.labelSmall,
                color = statusColor,
                modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
            )
        }
    }
}
