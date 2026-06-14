package com.campaignmasta.ui.screens.supporters

import androidx.lifecycle.ViewModel
import com.campaignmasta.data.local.entity.SupporterEntity
import com.campaignmasta.data.repository.SupporterRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

@HiltViewModel
class SupporterDetailViewModel @Inject constructor(
    private val supporterRepository: SupporterRepository
) : ViewModel() {
    fun observe(localId: String): Flow<SupporterEntity?> = supporterRepository.observeSupporter(localId)
}
