package com.campaignmasta.ui.navigation

import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.work.WorkManager
import com.campaignmasta.data.preferences.UserPreferences
import com.campaignmasta.sync.SyncWorker
import com.campaignmasta.ui.screens.auth.LoginScreen
import com.campaignmasta.ui.screens.calls.CallsScreen
import com.campaignmasta.ui.screens.dashboard.DashboardScreen
import com.campaignmasta.ui.screens.messages.MessagesScreen
import com.campaignmasta.ui.screens.polling.PollingScreen
import com.campaignmasta.ui.screens.supporters.AddSupporterScreen
import com.campaignmasta.ui.screens.supporters.SupportersScreen
import com.campaignmasta.ui.screens.wards.WardBriefsScreen
import dagger.hilt.android.EntryPointAccessors
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

@Composable
fun CampaignMastaNavGraph() {
    val navController = rememberNavController()
    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    // Determine start destination based on saved auth token
    var startDestination by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        // We can't inject UserPreferences directly here without Hilt entry point,
        // so we check via the hilt entry point pattern. For simplicity we default
        // to Login and let the LoginViewModel redirect on valid token.
        startDestination = Screen.Login.route

        // Start periodic sync worker
        SyncWorker.enqueuePeriodicSync(WorkManager.getInstance(context))
    }

    if (startDestination == null) return

    NavHost(
        navController = navController,
        startDestination = startDestination!!
    ) {
        composable(Screen.Login.route) {
            LoginScreen(
                onLoginSuccess = {
                    navController.navigate(Screen.Dashboard.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.Dashboard.route) {
            DashboardScreen(
                onNavigate = { route -> navController.navigate(route) },
                onLogout = {
                    navController.navigate(Screen.Login.route) {
                        popUpTo(0) { inclusive = true }
                    }
                }
            )
        }

        composable(Screen.Supporters.route) {
            SupportersScreen(
                onBack = { navController.popBackStack() },
                onAddSupporter = { navController.navigate(Screen.AddSupporter.route) }
            )
        }

        composable(Screen.AddSupporter.route) {
            AddSupporterScreen(
                onBack = { navController.popBackStack() },
                onSaved = { navController.popBackStack() }
            )
        }

        composable(Screen.Calls.route) {
            CallsScreen(onBack = { navController.popBackStack() })
        }

        composable(Screen.Messages.route) {
            MessagesScreen(onBack = { navController.popBackStack() })
        }

        composable(Screen.WardBriefs.route) {
            WardBriefsScreen(onBack = { navController.popBackStack() })
        }

        composable(Screen.Polling.route) {
            PollingScreen(onBack = { navController.popBackStack() })
        }
    }
}
