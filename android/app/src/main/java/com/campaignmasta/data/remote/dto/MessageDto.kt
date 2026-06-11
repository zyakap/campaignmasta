package com.campaignmasta.data.remote.dto

import com.google.gson.annotations.SerializedName

data class MessageDto(
    val id: Int,
    val subject: String,
    val body: String,
    @SerializedName("message_type") val messageType: String = "STANDARD",
    val priority: String = "NORMAL",
    @SerializedName("sender_name") val senderName: String = "",
    @SerializedName("delivery_channel") val deliveryChannel: String = "IN_APP",
    val status: String = "SENT",
    @SerializedName("sent_at") val sentAt: String? = null,
    @SerializedName("is_read") val isRead: Boolean = false,
    @SerializedName("is_acknowledged") val isAcknowledged: Boolean = false,
    @SerializedName("read_receipt_required") val readReceiptRequired: Boolean = false,
    @SerializedName("acknowledgement_required") val acknowledgementRequired: Boolean = false,
    @SerializedName("updated_at") val updatedAt: String = ""
)
