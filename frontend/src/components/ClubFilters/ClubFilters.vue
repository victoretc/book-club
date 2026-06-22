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
const activeFilter = ref<'all' | 'member' | 'owner'>('all')
const searchInput = ref<HTMLInputElement | null>(null)
const mounted = ref(false)

const filters = ['all', 'owner', 'member'] as const

let debounceTimer: ReturnType<typeof setTimeout> | null = null

onMounted(() => { mounted.value = true })

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

const applyFilter = (filter: 'all' | 'member' | 'owner') => {
  if (!authStore.isAuthenticated && filter !== 'all') {
    router.push('/signin')
    return
  }
  activeFilter.value = filter
  if (filter === 'all') {
    clubsStore.fetchClubs()
  } else {
    clubsStore.filterByMembership(filter)
  }
}
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
      <BaseButton variant="primary" class="search-btn" @click="handleSearch">Найти</BaseButton>
    </div>

    <div class="filter-tabs">
      <button
        v-for="f in filters"
        :key="f"
        @click="applyFilter(f)"
        :class="{ active: activeFilter === f, 'active-pop': activeFilter === f && mounted }"
        class="filter-tab"
      >
        {{ f === 'all' ? 'Все клубы' : f === 'owner' ? 'Мои клубы' : 'Участвую' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.filters-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.search-bar {
  display: flex;
  align-items: center;
  width: 704px;
  max-width: 100%;
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

.filter-tabs {
  display: flex;
  gap: 10px;
  padding: 8px 10px;
  background: var(--color-surface);
  border-radius: 30px;
}

.filter-tab {
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

@media (max-width: 768px) {
  .filters-section {
    gap: 12px;
  }

  .search-bar {
    width: 100%;
    padding: 6px 6px 6px 16px;
    gap: 6px;
  }

  .search-input {
    font-size: 16px;
  }

  .search-btn {
    height: 40px;
    padding: 0 16px;
    font-size: 16px;
  }

  .filter-tabs {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
    width: 100%;
    gap: 6px;
    padding: 6px 8px;
  }

  .filter-tab {
    font-size: 16px;
    padding: 8px 16px;
  }
}

@media (max-width: 480px) {
  .search-bar {
    padding: 4px 4px 4px 12px;
    border-radius: 24px;
  }

  .search-btn {
    height: 36px;
    padding: 0 12px;
    font-size: 14px;
  }

  .filter-tab {
    padding: 6px 10px;
    font-size: 14px;
  }
}
</style>
