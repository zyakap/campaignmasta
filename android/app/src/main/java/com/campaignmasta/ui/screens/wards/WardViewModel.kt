package com.campaignmasta.ui.screens.wards

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.campaignmasta.data.local.dao.WardProfileDao
import com.campaignmasta.data.local.entity.WardProfileEntity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import javax.inject.Inject

data class WardBriefsUiState(
    val wards: List<WardProfileEntity> = emptyList(),
    val selectedWard: WardProfileEntity? = null,
    val searchQuery: String = ""
)

@HiltViewModel
class WardViewModel @Inject constructor(
    private val wardProfileDao: WardProfileDao
) : ViewModel() {

    private val _search = MutableStateFlow("")
    private val _selected = MutableStateFlow<WardProfileEntity?>(null)

    val uiState: StateFlow<WardBriefsUiState> = combine(
        wardProfileDao.getAllFlow(),
        _search,
        _selected
    ) { wards, search, selected ->
        val filtered = if (search.isBlank()) wards
        else wards.filter {
            it.wardName.contains(search, true) || it.llgName.contains(search, true)
        }
        WardBriefsUiState(wards = filtered, selectedWard = selected, searchQuery = search)
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = WardBriefsUiState()
    )

    fun onSearchChange(q: String) { _search.value = q }
    fun selectWard(ward: WardProfileEntity) { _selected.value = ward }
    fun closeWard() { _selected.value = null }
}
