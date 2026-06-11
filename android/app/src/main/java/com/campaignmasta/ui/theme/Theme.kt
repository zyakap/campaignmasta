package com.campaignmasta.ui.theme

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColorScheme = lightColorScheme(
    primary = PNGRed,
    onPrimary = Color.White,
    primaryContainer = PNGRedDark,
    onPrimaryContainer = Color.White,
    secondary = PNGGold,
    onSecondary = PNGBlack,
    secondaryContainer = PNGGoldDark,
    onSecondaryContainer = PNGBlack,
    background = Background,
    onBackground = PNGBlack,
    surface = Surface,
    onSurface = PNGBlack,
    error = SupportWeak,
    onError = Color.White
)

@Composable
fun CampaignMastaTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColorScheme,
        typography = Typography,
        content = content
    )
}
