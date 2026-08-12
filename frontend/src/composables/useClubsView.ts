import { ref, watch } from 'vue'

export type ClubsViewMode = 'grid' | 'list'

const STORAGE_KEY = 'clubs-view-mode'

function readInitialMode(): ClubsViewMode {
  try {
    return localStorage.getItem(STORAGE_KEY) === 'grid' ? 'grid' : 'list'
  } catch {
    return 'list'
  }
}

const viewMode = ref<ClubsViewMode>(readInitialMode())

watch(viewMode, (mode) => {
  try {
    localStorage.setItem(STORAGE_KEY, mode)
  } catch {
    // ignore storage errors
  }
})

export function useClubsView() {
  return { viewMode }
}
