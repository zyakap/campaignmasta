package com.campaignmasta.ui.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

private val LightColorScheme = lightColorScheme(
    primary = PNGRed,
    onPrimary = Color.White,
    primaryContainer = CampaignMist,
    onPrimaryContainer = CampaignGreenDark,
    secondary = CampaignMaroon,
    onSecondary = Color.White,
    secondaryContainer = Color(0xFFF8E8E8),
    onSecondaryContainer = CampaignMaroon,
    tertiary = PNGGold,
    onTertiary = PNGBlack,
    background = Background,
    onBackground = PNGBlack,
    surface = Surface,
    onSurface = PNGBlack,
    surfaceVariant = CampaignMist,
    onSurfaceVariant = TextMuted,
    outline = CampaignLine,
    error = SupportWeak,
    onError = Color.White
)

private val AppShapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp),
    small = RoundedCornerShape(12.dp),
    medium = RoundedCornerShape(18.dp),
    large = RoundedCornerShape(24.dp),
    extraLarge = RoundedCornerShape(32.dp)
)

@Composable
fun CampaignMastaTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColorScheme,
        typography = Typography,
        shapes = AppShapes,
        content = content
    )
}
