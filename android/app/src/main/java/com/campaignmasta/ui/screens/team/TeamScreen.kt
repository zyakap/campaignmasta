package com.campaignmasta.ui.screens.team

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.campaignmasta.data.remote.dto.TeamMemberDto
import com.campaignmasta.data.remote.dto.VillageDto
import com.campaignmasta.ui.theme.PNGRed
import com.campaignmasta.ui.theme.SupportStrong
import com.campaignmasta.ui.theme.SupportMedium
import com.campaignmasta.ui.theme.SupportUnknown

private fun roleColor(role: String): Color = when (role) {
    "CANDIDATE", "CAMPAIGN_MANAGER" -> PNGRed
    "DISTRICT_COORDINATOR" -> Color(0xFF6A1B9A)
    "LLG_COORDINATOR" -> Color(0xFF1565C0)
    "WARD_COORDINATOR" -> SupportStrong
    "VILLAGE_COORDINATOR" -> Color(0xFF00897B)
    "VOLUNTEER" -> SupportMedium
    else -> SupportUnknown
}

private fun memberLocation(m: TeamMemberDto): String = when {
    !m.villageName.isNullOrBlank() -> m.villageName!!
    m.wardName.isNotBlank() -> m.wardName
    !m.llgName.isNullOrBlank() -> m.llgName!!
    !m.districtName.isNullOrBlank() -> m.districtName!!
    else -> "Whole campaign"
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TeamScreen(
    onBack: () -> Unit,
    onAddMember: () -> Unit,
    viewModel: TeamViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val snackbarHost = remember { SnackbarHostState() }

    LaunchedEffect(state.actionMessage) {
        state.actionMessage?.let {
            snackbarHost.showSnackbar(it)
            viewModel.clearActionMessage()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Campaign Team") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back", tint = Color.White)
                    }
                },
                actions = {
                    if (state.canAddVillage) {
                        IconButton(onClick = viewModel::openVillageDialog) {
                            Icon(Icons.Default.AddLocationAlt, contentDescription = "Add village", tint = Color.White)
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = PNGRed,
                    titleContentColor = Color.White,
                    actionIconContentColor = Color.White
                )
            )
        },
        snackbarHost = { SnackbarHost(snackbarHost) },
        floatingActionButton = {
            if (state.canAddMembers) {
                ExtendedFloatingActionButton(
                    onClick = onAddMember,
                    containerColor = PNGRed,
                    contentColor = Color.White
                ) {
                    Icon(Icons.Default.PersonAdd, contentDescription = null)
                    Spacer(Modifier.width(8.dp))
                    Text("Add Member")
                }
            }
        }
    ) { padding ->
        PullToRefreshBox(
            isRefreshing = state.isRefreshing,
            onRefresh = { viewModel.load(isRefresh = true) },
            modifier = Modifier.padding(padding).fillMaxSize()
        ) {
            when {
                state.isLoading -> Box(Modifier.fillMaxSize(), Alignment.Center) {
                    CircularProgressIndicator(color = PNGRed)
                }
                state.errorMessage != null && state.team.isEmpty() ->
                    ErrorState(state.errorMessage!!) { viewModel.load() }
                else -> LazyColumn(
                    contentPadding = PaddingValues(bottom = 96.dp, top = 8.dp)
                ) {
                    state.performance?.let { perf ->
                        item {
                            PerformanceCard(
                                registered = perf.supportersRegistered,
                                teamTotal = perf.teamTotal,
                                volunteers = perf.volunteersCreated
                            )
                        }
                    }
                    if (state.leaderboard.isNotEmpty()) {
                        item { SectionHeader("Registration Leaderboard") }
                        itemsIndexed(state.leaderboard) { index, row ->
                            LeaderboardRow(rank = index + 1, name = row.fullName, role = row.roleDisplay, count = row.count)
                        }
                    }

                    if (state.pendingMembers.isNotEmpty() || state.pendingVillages.isNotEmpty()) {
                        item { SectionHeader("Awaiting Your Approval") }
                        items(state.pendingMembers, key = { "m${it.id}" }) { m ->
                            PendingMemberCard(
                                member = m,
                                busy = state.busyMemberId == m.id,
                                onApprove = { viewModel.approveMember(m.id, reject = false) },
                                onReject = { viewModel.approveMember(m.id, reject = true) }
                            )
                        }
                        items(state.pendingVillages, key = { "v${it.id}" }) { v ->
                            PendingVillageCard(
                                village = v,
                                busy = state.busyVillageId == v.id,
                                onApprove = { viewModel.approveVillage(v.id, reject = false) },
                                onReject = { viewModel.approveVillage(v.id, reject = true) }
                            )
                        }
                    }

                    item { SectionHeader("Team Members (${state.team.size})") }
                    if (state.team.isEmpty()) {
                        item { EmptyHint("No team members in your area yet.") }
                    } else {
                        items(state.team, key = { it.id }) { m -> MemberRow(m) }
                    }
                }
            }
        }
    }

    if (state.villageDialogOpen) {
        AddVillageDialog(
            wards = state.villageWards,
            saving = state.villageSavingName,
            onDismiss = viewModel::closeVillageDialog,
            onSave = { wardId, name -> viewModel.createVillage(wardId, name) }
        )
    }
}

@Composable
private fun PerformanceCard(registered: Int, teamTotal: Int, volunteers: Int) {
    Surface(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp),
        shape = RoundedCornerShape(16.dp),
        color = SupportStrong
    ) {
        Column(Modifier.padding(16.dp)) {
            Text("MY PERFORMANCE", style = MaterialTheme.typography.labelMedium, color = Color.White.copy(alpha = 0.8f), fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(12.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                StatCell("Registered", registered, Modifier.weight(1f))
                StatCell("Team total", teamTotal, Modifier.weight(1f))
                if (volunteers > 0) StatCell("Volunteers", volunteers, Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun StatCell(label: String, value: Int, modifier: Modifier = Modifier) {
    Surface(modifier = modifier, color = Color.White.copy(alpha = 0.15f), shape = RoundedCornerShape(10.dp)) {
        Column(Modifier.padding(vertical = 12.dp, horizontal = 8.dp)) {
            Text("$value", style = MaterialTheme.typography.headlineSmall, color = Color.White, fontWeight = FontWeight.Bold)
            Text(label, style = MaterialTheme.typography.bodySmall, color = Color.White.copy(alpha = 0.85f))
        }
    }
}

@Composable
private fun LeaderboardRow(rank: Int, name: String, role: String, count: Int) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text("$rank", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = Color.Gray, modifier = Modifier.width(28.dp))
        Column(Modifier.weight(1f)) {
            Text(name, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
            if (role.isNotBlank()) Text(role, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
        }
        Text("$count", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = SupportStrong)
    }
    HorizontalDivider(color = Color(0xFFEEEEEE))
}

@Composable
private fun SectionHeader(text: String) {
    Text(
        text = text.uppercase(),
        style = MaterialTheme.typography.labelMedium,
        fontWeight = FontWeight.Bold,
        color = Color.Gray,
        modifier = Modifier.padding(start = 16.dp, end = 16.dp, top = 16.dp, bottom = 6.dp)
    )
}

@Composable
private fun MemberRow(m: TeamMemberDto) {
    val color = roleColor(m.role)
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Surface(modifier = Modifier.size(44.dp), shape = RoundedCornerShape(10.dp), color = color.copy(alpha = 0.15f)) {
            Box(contentAlignment = Alignment.Center) {
                Text(m.fullName.firstOrNull()?.uppercase() ?: "?", color = color, fontWeight = FontWeight.Bold)
            }
        }
        Spacer(Modifier.width(12.dp))
        Column(Modifier.weight(1f)) {
            Text(m.fullName, style = MaterialTheme.typography.bodyLarge, fontWeight = FontWeight.Medium)
            Text(memberLocation(m), style = MaterialTheme.typography.bodySmall, color = Color.Gray)
            if (m.phone.isNotBlank()) {
                Text(m.phone, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
            }
        }
        RoleChip(m.roleDisplay.ifBlank { m.role }, color)
    }
    HorizontalDivider(color = Color(0xFFEEEEEE))
}

@Composable
private fun RoleChip(label: String, color: Color) {
    Surface(color = color.copy(alpha = 0.12f), shape = RoundedCornerShape(6.dp)) {
        Text(
            label,
            style = MaterialTheme.typography.labelSmall,
            color = color,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
        )
    }
}

@Composable
private fun PendingMemberCard(
    member: TeamMemberDto,
    busy: Boolean,
    onApprove: () -> Unit,
    onReject: () -> Unit
) {
    ApprovalCard(
        title = member.fullName,
        subtitle = "${member.roleDisplay.ifBlank { member.role }} · ${memberLocation(member)}",
        footnote = member.createdByMemberName?.let { "Added by $it" },
        color = roleColor(member.role),
        busy = busy,
        onApprove = onApprove,
        onReject = onReject
    )
}

@Composable
private fun PendingVillageCard(
    village: VillageDto,
    busy: Boolean,
    onApprove: () -> Unit,
    onReject: () -> Unit
) {
    ApprovalCard(
        title = village.name,
        subtitle = "New village · ${village.wardName}" + (village.llgName?.let { " · $it" } ?: ""),
        footnote = village.createdBy?.let { "Requested by $it" },
        color = Color(0xFF00897B),
        busy = busy,
        onApprove = onApprove,
        onReject = onReject
    )
}

@Composable
private fun ApprovalCard(
    title: String,
    subtitle: String,
    footnote: String?,
    color: Color,
    busy: Boolean,
    onApprove: () -> Unit,
    onReject: () -> Unit
) {
    Surface(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 6.dp),
        shape = RoundedCornerShape(14.dp),
        color = Color(0xFFFFFBEB),
        border = androidx.compose.foundation.BorderStroke(1.dp, Color(0xFFFDE68A))
    ) {
        Column(Modifier.padding(14.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text(subtitle, style = MaterialTheme.typography.bodyMedium, color = Color(0xFF92400E))
            if (footnote != null) {
                Text(footnote, style = MaterialTheme.typography.bodySmall, color = Color.Gray)
            }
            Spacer(Modifier.height(12.dp))
            if (busy) {
                CircularProgressIndicator(Modifier.size(24.dp), color = color, strokeWidth = 2.dp)
            } else {
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    Button(
                        onClick = onApprove,
                        modifier = Modifier.weight(1f).height(48.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = SupportStrong)
                    ) {
                        Icon(Icons.Default.Check, contentDescription = null)
                        Spacer(Modifier.width(6.dp))
                        Text("Approve")
                    }
                    OutlinedButton(
                        onClick = onReject,
                        modifier = Modifier.weight(1f).height(48.dp)
                    ) {
                        Icon(Icons.Default.Close, contentDescription = null)
                        Spacer(Modifier.width(6.dp))
                        Text("Reject")
                    }
                }
            }
        }
    }
}

@Composable
private fun ErrorState(message: String, onRetry: () -> Unit) {
    Box(Modifier.fillMaxSize(), Alignment.Center) {
        Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(24.dp)) {
            Icon(Icons.Default.CloudOff, contentDescription = null, modifier = Modifier.size(56.dp), tint = Color.LightGray)
            Spacer(Modifier.height(12.dp))
            Text(message, style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
            Spacer(Modifier.height(16.dp))
            Button(onClick = onRetry, colors = ButtonDefaults.buttonColors(containerColor = PNGRed)) {
                Text("Try Again")
            }
        }
    }
}

@Composable
private fun EmptyHint(text: String) {
    Box(Modifier.fillMaxWidth().padding(32.dp), Alignment.Center) {
        Text(text, style = MaterialTheme.typography.bodyMedium, color = Color.Gray)
    }
}
