package com.campaignmasta.ui.screens.supporters

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.campaignmasta.data.local.entity.SupporterEntity
import com.campaignmasta.ui.theme.SupportMedium
import com.campaignmasta.ui.theme.SupportStrong
import com.campaignmasta.ui.theme.SupportUnknown
import com.campaignmasta.ui.theme.SupportWeak

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SupporterDetailScreen(
    localId: String,
    onBack: () -> Unit,
    viewModel: SupporterDetailViewModel = hiltViewModel()
) {
    val supporter by viewModel.observe(localId).collectAsStateWithLifecycle(initialValue = null)
    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("Supporter details") },
                navigationIcon = {
                    IconButton(onClick = onBack) { Icon(Icons.Default.ArrowBack, contentDescription = "Back") }
                }
            )
        }
    ) { padding ->
        if (supporter == null) {
            Box(Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("Supporter not found")
            }
        } else {
            SupporterDetailContent(
                supporter = supporter!!,
                modifier = Modifier.padding(padding)
            )
        }
    }
}

@Composable
private fun SupporterDetailContent(supporter: SupporterEntity, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val statusColor = supporter.statusColor()
    Column(
        modifier = modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp)
    ) {
        ElevatedCard(shape = RoundedCornerShape(28.dp)) {
            Column(
                modifier = Modifier.padding(22.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                Surface(
                    color = statusColor.copy(alpha = 0.14f),
                    shape = RoundedCornerShape(18.dp)
                ) {
                    Icon(
                        Icons.Default.Person,
                        contentDescription = null,
                        tint = statusColor,
                        modifier = Modifier.padding(14.dp).size(34.dp)
                    )
                }
                Text(
                    text = supporter.fullName,
                    style = MaterialTheme.typography.headlineSmall,
                    fontWeight = FontWeight.ExtraBold
                )
                Text(
                    text = listOf(supporter.ward, supporter.village, supporter.clan)
                        .filter { it.isNotBlank() }
                        .joinToString(" • ")
                        .ifBlank { "No location details recorded" },
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                StatusPill(supporter.supportStatus, statusColor)
            }
        }

        if (supporter.phone.isNotBlank()) {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp), modifier = Modifier.fillMaxWidth()) {
                ActionButton("Call", Icons.Default.Call, Modifier.weight(1f)) {
                    context.startActivity(Intent(Intent.ACTION_DIAL, Uri.parse("tel:${supporter.phone}")))
                }
                ActionButton("WhatsApp", Icons.Default.Chat, Modifier.weight(1f)) {
                    val clean = supporter.phone.filter { it.isDigit() }
                    context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://wa.me/$clean")))
                }
            }
        }

        DetailSection(
            title = "Campaign profile",
            rows = listOf(
                "Phone" to supporter.phone.ifBlank { "Not recorded" },
                "Gender" to supporter.gender.ifBlank { "Unknown" },
                "Enrollment" to supporter.enrollmentStatus.toDisplayText(),
                "Influence" to supporter.supportStatus.toDisplayText(),
                "SMS consent" to if (supporter.consentToMessages) "Yes" else "No",
                "Follow-up" to if (supporter.followUpRequired) supporter.followUpDate ?: "Required" else "Not required"
            )
        )
        DetailSection(
            title = "Notes",
            rows = listOf("Notes" to supporter.notes.ifBlank { "No notes recorded" })
        )
    }
}

@Composable
private fun ActionButton(label: String, icon: androidx.compose.ui.graphics.vector.ImageVector, modifier: Modifier, onClick: () -> Unit) {
    FilledTonalButton(
        onClick = onClick,
        modifier = modifier.height(52.dp),
        shape = RoundedCornerShape(16.dp)
    ) {
        Icon(icon, contentDescription = null)
        Spacer(Modifier.width(8.dp))
        Text(label, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun StatusPill(status: String, color: Color) {
    Surface(color = color.copy(alpha = 0.14f), shape = RoundedCornerShape(999.dp)) {
        Text(
            text = status.toDisplayText(),
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 7.dp),
            color = color,
            style = MaterialTheme.typography.labelSmall,
            fontWeight = FontWeight.Bold
        )
    }
}

@Composable
private fun DetailSection(title: String, rows: List<Pair<String, String>>) {
    ElevatedCard(shape = RoundedCornerShape(22.dp)) {
        Column(modifier = Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            rows.forEach { (label, value) ->
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Text(label, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Text(value, fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(start = 16.dp))
                }
            }
        }
    }
}

private fun SupporterEntity.statusColor(): Color = when (supportStatus) {
    "STRONG" -> SupportStrong
    "LEANING" -> SupportMedium
    "NOT_SUPPORTIVE" -> SupportWeak
    else -> SupportUnknown
}

private fun String.toDisplayText(): String = replace("_", " ").lowercase().replaceFirstChar { it.uppercase() }
