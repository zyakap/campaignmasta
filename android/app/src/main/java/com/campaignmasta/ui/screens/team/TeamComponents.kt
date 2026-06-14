package com.campaignmasta.ui.screens.team

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.campaignmasta.data.remote.dto.GeoItemDto
import com.campaignmasta.ui.theme.PNGRed

/**
 * A large, touch-friendly dropdown. Disabled until [enabled] so cascading
 * pickers reveal one level at a time — clearer for first-time users.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun <T> LabeledDropdown(
    label: String,
    options: List<T>,
    selected: T?,
    optionLabel: (T) -> String,
    onSelect: (T) -> Unit,
    enabled: Boolean = true,
    modifier: Modifier = Modifier
) {
    var expanded by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(
        expanded = expanded && enabled,
        onExpandedChange = { if (enabled) expanded = it },
        modifier = modifier
    ) {
        OutlinedTextField(
            value = selected?.let(optionLabel) ?: "",
            onValueChange = {},
            readOnly = true,
            enabled = enabled,
            label = { Text(label) },
            placeholder = { Text(if (enabled) "Tap to choose" else "Choose the level above first") },
            trailingIcon = { Icon(Icons.Default.ArrowDropDown, contentDescription = null) },
            singleLine = true,
            modifier = Modifier.menuAnchor().fillMaxWidth()
        )
        ExposedDropdownMenu(expanded = expanded && enabled, onDismissRequest = { expanded = false }) {
            if (options.isEmpty()) {
                DropdownMenuItem(text = { Text("No options available") }, onClick = { expanded = false })
            }
            options.forEach { option ->
                DropdownMenuItem(
                    text = { Text(optionLabel(option), style = MaterialTheme.typography.bodyLarge) },
                    onClick = { onSelect(option); expanded = false }
                )
            }
        }
    }
}

@Composable
fun AddVillageDialog(
    wards: List<GeoItemDto>,
    saving: Boolean,
    onDismiss: () -> Unit,
    onSave: (wardId: Int, name: String) -> Unit
) {
    var name by remember { mutableStateOf("") }
    var ward by remember { mutableStateOf<GeoItemDto?>(null) }

    AlertDialog(
        onDismissRequest = { if (!saving) onDismiss() },
        title = { Text("Add Village / Area") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text(
                    "New villages are sent to the LLG coordinator for approval before they can be used.",
                    style = MaterialTheme.typography.bodySmall
                )
                LabeledDropdown(
                    label = "Ward",
                    options = wards,
                    selected = ward,
                    optionLabel = { it.name },
                    onSelect = { ward = it }
                )
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it },
                    label = { Text("Village / area name") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
            }
        },
        confirmButton = {
            Button(
                onClick = { ward?.let { onSave(it.id, name) } },
                enabled = !saving && ward != null && name.isNotBlank(),
                colors = ButtonDefaults.buttonColors(containerColor = PNGRed)
            ) {
                if (saving) CircularProgressIndicator(Modifier.size(18.dp), color = androidx.compose.ui.graphics.Color.White, strokeWidth = 2.dp)
                else Text("Submit")
            }
        },
        dismissButton = { TextButton(onClick = onDismiss, enabled = !saving) { Text("Cancel") } }
    )
}
