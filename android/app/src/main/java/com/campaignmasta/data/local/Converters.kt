package com.campaignmasta.data.local

import androidx.room.TypeConverter

class Converters {

    @TypeConverter
    fun fromIntNullable(value: Int?): String? = value?.toString()

    @TypeConverter
    fun toIntNullable(value: String?): Int? = value?.toIntOrNull()
}
