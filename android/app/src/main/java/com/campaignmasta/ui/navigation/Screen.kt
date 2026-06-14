package com.campaignmasta.ui.navigation

sealed class Screen(val route: String) {
    object Login : Screen("login")
    object Dashboard : Screen("dashboard")
    object Supporters : Screen("supporters")
    object AddSupporter : Screen("add_supporter")
    object Calls : Screen("calls")
    object Messages : Screen("messages")
    object WardBriefs : Screen("ward_briefs")
    object Polling : Screen("polling")
    object Team : Screen("team")
    object AddMember : Screen("add_member")
}
