import { defineStore } from 'pinia'
import { api } from '@/api'
import { useAuthStore } from '@/stores/auth'
import type { Club, ClubsListParams, PatchedClub } from '@/api/data-contracts'

interface ClubsState {
  clubs: Club[]
  isLoading: boolean
  error: string | null
  activeFilter: 'member' | 'owner' | 'all' | null
  activeSearch: string | null
  pagination: {
    count: number
    next: string | null
    previous: string | null
    currentPage: number
    pageSize: number
  }
}

export const useClubsStore = defineStore('clubs', {
  state: (): ClubsState => ({
    clubs: [],
    isLoading: false,
    error: null,
    activeFilter: null,
    activeSearch: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
      currentPage: 1,
      pageSize: 10,
    },
  }),

  actions: {
    async _fetchClubsWithParams(params: ClubsListParams, errorMessage: string) {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.api.clubsList(params)
        this.clubs = response.data.results
        this.pagination = {
          count: response.data.count,
          next: response.data.next ?? null,
          previous: response.data.previous ?? null,
          currentPage: params.page ?? 1,
          pageSize: params.page_size ?? 10,
        }
      } catch (error) {
        this.error = errorMessage
        console.error('Error fetching clubs:', error)
      } finally {
        this.isLoading = false
      }
    },

    _fetchWithCurrentParams(page: number, pageSize: number) {
      if (this.activeSearch) {
        return this.searchClubs(this.activeSearch, page, pageSize)
      }
      if (this.activeFilter && this.activeFilter !== 'all') {
        return this.filterByMembership(this.activeFilter, page, pageSize)
      }
      return this.fetchClubs(page, pageSize)
    },

    async fetchClubs(page: number = 1, pageSize: number = 10) {
      this.activeFilter = 'all'
      this.activeSearch = null
      await this._fetchClubsWithParams(
        { page, page_size: pageSize },
        'Не удалось загрузить список клубов',
      )
    },

    async searchClubs(query: string, page: number = 1, pageSize: number = 10) {
      this.activeSearch = query
      this.activeFilter = null
      await this._fetchClubsWithParams(
        { search: query, page, page_size: pageSize },
        'Ошибка при поиске клубов',
      )
    },

    async filterByMembership(
      type: 'member' | 'owner' | 'all',
      page: number = 1,
      pageSize: number = 10,
    ) {
      this.activeFilter = type
      this.activeSearch = null
      const params: ClubsListParams = { page, page_size: pageSize }
      if (type !== 'all') params.membership = type
      await this._fetchClubsWithParams(params, 'Ошибка при фильтрации клубов')
    },

    async nextPage() {
      if (this.pagination.next) {
        await this._fetchWithCurrentParams(this.pagination.currentPage + 1, this.pagination.pageSize)
      }
    },

    async prevPage() {
      if (this.pagination.previous) {
        await this._fetchWithCurrentParams(this.pagination.currentPage - 1, this.pagination.pageSize)
      }
    },

    async goToPage(page: number) {
      if (page >= 1 && page <= this.totalPages) {
        await this._fetchWithCurrentParams(page, this.pagination.pageSize)
      }
    },

    async changePageSize(size: number) {
      await this._fetchWithCurrentParams(1, size)
    },

    async joinClub(clubId: number) {
      try {
        await api.api.clubsMembersMeCreate(clubId)
      } catch (error) {
        console.error('Error joining club:', error)
        throw error
      }
    },

    async leaveClub(clubId: number) {
      try {
        await api.api.clubsMembersMeDestroy(clubId)
      } catch (error) {
        console.error('Error leaving club:', error)
        throw error
      }
    },

    isCurrentUserMember(club: Club): boolean {
      const authStore = useAuthStore()
      return authStore.user ? club.members.some(m => m.id === Number(authStore.user!.id)) : false
    },

    isCurrentUserOwner(club: Club): boolean {
      const authStore = useAuthStore()
      return authStore.user ? Number(club.owner) === Number(authStore.user.id) : false
    },

    async createClub(data: Partial<Club>) {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.api.clubsCreate(data as Club)
        return response.data
      } catch (error) {
        this.error = 'Ошибка при создании клуба'
        console.error('Error creating club:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async updateClub(clubId: number, data: Partial<Club>) {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.api.clubsUpdate(clubId, data as Club)
        return response.data
      } catch (error) {
        this.error = 'Ошибка при обновлении клуба'
        console.error('Error updating club:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },

    async fetchClub(clubId: number) {
      this.isLoading = true
      this.error = null
      try {
        const response = await api.api.clubsRetrieve(clubId)
        return response.data
      } catch (error) {
        this.error = 'Не удалось загрузить информацию о клубе'
        console.error('Error fetching club:', error)
        throw error
      } finally {
        this.isLoading = false
      }
    },
  },

  getters: {
    totalPages(state): number {
      return Math.ceil(state.pagination.count / state.pagination.pageSize)
    },
    hasNextPage(state): boolean {
      return state.pagination.next !== null
    },
    hasPrevPage(state): boolean {
      return state.pagination.previous !== null
    },
    clubsCount(state): number {
      return state.clubs.length
    },
  },
})
