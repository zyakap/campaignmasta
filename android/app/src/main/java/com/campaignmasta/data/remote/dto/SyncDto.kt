package com.campaignmasta.data.remote.dto

import com.google.gson.annotations.SerializedName

data class SyncPushItem(
    @SerializedName("entity_type") val entityType: String,
    val operation: String,
    @SerializedName("local_id") val localId: String,
    @SerializedName("server_id") val serverId: Int?,
    val payload: Map<String, Any?>
)

data class SyncPushRequest(
    val items: List<SyncPushItem>
)

data class SyncPushResultItem(
    @SerializedName("local_id") val localId: String,
    @SerializedName("server_id") val serverId: Int?,
    val status: String
)

data class SyncPushResponse(
    val results: List<SyncPushResultItem>
)

data class PaginatedResponse<T>(
    val count: Int,
    val next: String?,
    val previous: String?,
    val results: List<T>
)

data class ListResponse<T>(
    val count: Int,
    val results: List<T>
)
