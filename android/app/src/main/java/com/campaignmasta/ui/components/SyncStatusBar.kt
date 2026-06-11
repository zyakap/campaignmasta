package com.campaignmasta.ui.components

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CloudDone
import androidx.compose.material.icons.filled.CloudUpload
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.campaignmasta.ui.theme.SyncDone
import com.campaignmasta.ui.theme.SyncPending

@Composable
fun SyncStatusBar(pendingCount: Int, modifier: Modifier = Modifier) {
    AnimatedVisibility(visible = pendingCount > 0, modifier = modifier) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .background(SyncPending)
                .padding(horizontal = 16.dp, vertical = 4.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = Icons.Default.CloudUpload,
                contentDescription = null,
                tint = Color.White,
                modifier = Modifier.size(14.dp)
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = "$pendingCount change${if (pendingCount > 1) "s" else ""} pending sync",
                style = MaterialTheme.typography.labelSmall,
                color = Color.White
            )
        }
    }
}
