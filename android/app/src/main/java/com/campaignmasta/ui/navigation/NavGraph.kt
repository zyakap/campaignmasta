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
import com.campaignmasta.ui.screens.team.AddMemberScreen
import com.campaignmasta.ui.screens.team.TeamScreen
import com.campaignmasta.ui.screens.wards.WardBriefsScreen
import dagger.hilt.EntryPoint
import dagger.hilt.InstallIn
import dagger.hilt.android.EntryPointAccessors
import dagger.hilt.components.SingletonComponent

@EntryPoint
@InstallIn(SingletonComponent::class)
interface NavGraphEntryPoint {
    fun userPreferences(): UserPreferences
}

@Composable
fun CampaignMastaNavGraph() {
    val navController = rememberNavController()
    val context = LocalContext.current

    // Determine start destination based on the saved auth token so a returning,
    // already-authenticated user lands straight on the dashboard.
    var startDestination by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        val userPreferences = EntryPointAccessors
            .fromApplication(context.applicationContext, NavGraphEntryPoint::class.java)
            .userPreferences()
        startDestination = if (userPreferences.isLoggedIn()) {
            Screen.Dashboard.route
        } else {
            Screen.Login.route
        }

        // Start periodic background sync.
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

        composable(Screen.Team.route) {
            TeamScreen(
                onBack = { navController.popBackStack() },
                onAddMember = { navController.navigate(Screen.AddMember.route) }
            )
        }

        composable(Screen.AddMember.route) {
            AddMemberScreen(
                onBack = { navController.popBackStack() },
                onSaved = { navController.popBackStack() }
            )
        }
    }
}
