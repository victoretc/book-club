<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useClubsStore } from '@/stores/clubs'
import BaseButton from '@/components/BaseButton/BaseButton.vue'

const router = useRouter()
const authStore = useAuthStore()
const clubsStore = useClubsStore()

const searchQuery = ref('')
const activeFilter = ref<'all' | 'member'>('all')
const searchInput = ref<HTMLInputElement | null>(null)
const mounted = ref(false)
const showFilterDropdown = ref(false)
const filterDropdownRef = ref<HTMLDivElement | null>(null)

const filters = ['all', 'member'] as const

const filterLabels: Record<string, string> = {
  all: 'Все клубы',
  member: 'Участвую',
}

let debounceTimer: ReturnType<typeof setTimeout> | null = null

watch(
  () => clubsStore.activeFilter,
  (val) => {
    if (val) activeFilter.value = val
  },
  { immediate: true },
)

onMounted(() => {
  mounted.value = true
  document.addEventListener('click', handleOutsideClick)
})

const doSearch = (query: string) => {
  if (query.trim()) {
    clubsStore.searchClubs(query.trim())
  } else {
    clubsStore.fetchClubs()
  }
}

watch(searchQuery, (val) => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => doSearch(val), 200)
})

const handleSearch = () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  doSearch(searchQuery.value)
}

const handleSearchKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter') {
    handleSearch()
  }
}

const applyFilter = (filter: 'all' | 'member') => {
  if (!authStore.isAuthenticated && filter === 'member') {
    router.push('/signin')
    return
  }
  activeFilter.value = filter
  clubsStore.filterByMembership(filter)
  showFilterDropdown.value = false
}

const toggleFilterDropdown = () => {
  showFilterDropdown.value = !showFilterDropdown.value
}

const handleOutsideClick = (e: MouseEvent) => {
  if (filterDropdownRef.value && !filterDropdownRef.value.contains(e.target as Node)) {
    showFilterDropdown.value = false
  }
}

const filterLabel = (f: 'all' | 'member') => filterLabels[f]
</script>

<template>
  <div class="filters-section">
    <div class="search-bar">
      <input
        ref="searchInput"
        v-model="searchQuery"
        type="text"
        placeholder="Найти книжный клуб"
        class="search-input"
        @keydown="handleSearchKeydown"
      />
      <BaseButton variant="primary" class="search-btn" @click="handleSearch">
        <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8" />
          <path d="M21 21l-4.35-4.35" />
        </svg>
        <span class="search-btn-text">Найти</span>
      </BaseButton>
    </div>

    <div ref="filterDropdownRef" class="filter-tabs">
      <div class="filter-current" @click="toggleFilterDropdown">
        <span class="filter-current-label">{{ filterLabel(activeFilter) }}</span>
        <svg class="filter-chevron" :class="{ open: showFilterDropdown }" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="6 9 12 15 18 9" />
        </svg>
      </div>
      <div v-if="showFilterDropdown" class="filter-options">
        <button
          v-for="f in filters"
          :key="f"
          @click="applyFilter(f)"
          :class="{ active: activeFilter === f }"
          class="filter-tab filter-tab--membership"
        >
          {{ filterLabel(f) }}
        </button>
      </div>
      <div class="filter-options-desktop">
        <button
          v-for="f in filters"
          :key="f"
          @click="applyFilter(f)"
          :class="{ active: activeFilter === f, 'active-pop': activeFilter === f && mounted }"
          class="filter-tab filter-tab--membership"
        >
          {{ filterLabel(f) }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.filters-section {
  width: 100%;
  display: grid;
  grid-template-columns: minmax(0, 704px) 300px;
  justify-content: center;
  align-items: stretch;
  gap: 16px;
}

.search-bar {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 704px;
  background: var(--color-surface);
  border-radius: 30px;
  padding: 8px 10px 8px 24px;
  gap: 8px;
}

.search-input {
  flex: 1;
  background: none;
  border: none;
  font-family: var(--font-body);
  font-size: 20px;
  font-weight: 400;
  line-height: 1.21;
  color: var(--color-text);
  outline: none;
  min-width: 0;
}

.search-input::placeholder {
  color: var(--color-text-secondary);
}

.search-btn {
  height: 48px;
  padding: 0 24px;
  border-radius: 30px;
  font-size: 20px;
  flex-shrink: 0;
}

.search-icon {
  display: none;
}

.filter-tabs {
  position: relative;
  display: flex;
  gap: 10px;
  padding: 8px 10px;
  background: var(--color-surface);
  border-radius: 30px;
  width: 100%;
}

.filter-current {
  display: none;
}

.filter-options {
  display: none;
}

.filter-options-desktop {
  display: flex;
  gap: 10px;
  width: 100%;
}

.filter-tab {
  flex: 1;
  padding: 10px 20px;
  background: transparent;
  border: none;
  border-radius: 30px;
  font-family: var(--font-body);
  font-size: 20px;
  font-weight: 500;
  line-height: 1.21;
  color: var(--color-text);
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.25s ease, color 0.25s ease;
}

.filter-tab.active {
  background: var(--color-brand);
  color: #FFFFFF;
}

.filter-tab:not(.active):hover {
  background: var(--color-brand-soft);
}

@keyframes active-pop {
  0% { transform: scale(1); }
  40% { transform: scale(1.06); }
  100% { transform: scale(1); }
}

.filter-tab.active-pop {
  animation: active-pop 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@media (max-width: 900px) {
  .filters-section {
    grid-template-columns: 1fr;
    gap: 8px;
  }

  .search-bar {
    width: 100%;
  }

  .filter-tabs {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .search-bar {
    padding: 6px 6px 6px 16px;
    gap: 6px;
  }

  .search-input {
    font-size: 16px;
  }

  .search-btn {
    height: 40px;
    padding: 0 14px;
  }

  .search-btn-text {
    display: none;
  }

  .search-icon {
    display: block;
  }

  .filter-tabs {
    width: 100%;
    padding: 0;
    background: none;
    border-radius: 0;
    gap: 0;
  }

  .filter-current {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    padding: 10px 16px;
    background: var(--color-surface);
    border-radius: 30px;
    cursor: pointer;
    gap: 8px;
  }

  .filter-current-label {
    font-family: var(--font-body);
    font-size: 15px;
    font-weight: 500;
    color: var(--color-text);
  }

  .filter-chevron {
    flex-shrink: 0;
    color: var(--color-text-secondary);
    transition: transform 0.2s;
  }

  .filter-chevron.open {
    transform: rotate(180deg);
  }

  .filter-options {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: calc(100% + 4px);
    left: 0;
    right: 0;
    background: var(--color-surface);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    z-index: 50;
  }

  .filter-options-desktop {
    display: none;
  }

  .filter-tab--membership {
    width: 100%;
    padding: 12px 16px;
    border-radius: 0;
    font-size: 15px;
    text-align: left;
    background: transparent;
    color: var(--color-text);
    border: none;
    border-bottom: 1px solid var(--color-stroke-subtle);
    transition: background 0.15s, color 0.15s;
  }

  .filter-tab--membership:last-child {
    border-bottom: none;
  }

  .filter-tab--membership.active {
    background: var(--color-brand-soft);
    color: var(--color-brand);
  }

  .filter-tab--membership:not(.active):hover {
    background: var(--color-brand-soft);
  }

  .filter-tab--membership.active-pop {
    animation: none;
  }
}

@media (max-width: 480px) {
  .filters-section {
    gap: 8px;
  }

  .search-bar {
    padding: 4px 4px 4px 12px;
    gap: 4px;
  }

  .search-input {
    font-size: 16px;
  }

  .search-btn {
    height: 34px;
    padding: 0 10px;
  }

  .search-icon {
    width: 18px;
    height: 18px;
  }

  .filter-current {
    padding: 8px 14px;
  }

  .filter-current-label {
    font-size: 14px;
  }

  .filter-tab {
    padding: 10px 14px;
    font-size: 14px;
  }
}
</style>
