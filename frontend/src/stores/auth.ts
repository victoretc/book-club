import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios, { type AxiosError, type AxiosRequestConfig } from 'axios'
import type { User, TokenResponse, AuthState } from '@/types/users'

const AUTH_STORAGE_KEY = 'book_club_auth'
const REFRESH_ENDPOINT = '/api/v1/auth/token/refresh/'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const pendingClubJoin = ref<number | null>(null)

  const updateAxiosAuthHeader = (token: string | null) => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete axios.defaults.headers.common['Authorization']
    }
  }

  const setPendingClubJoin = (clubId: number) => {
    pendingClubJoin.value = clubId
    saveState()
  }

  const clearPendingClubJoin = () => {
    pendingClubJoin.value = null
    saveState()
  }

  const saveState = () => {
    const state: Omit<AuthState, 'pendingClubJoin'> & { pendingClubJoin?: number } = {
      user: user.value,
      accessToken: accessToken.value,
      refreshToken: refreshToken.value,
      isAuthenticated: isAuthenticated.value,
    }

    if (pendingClubJoin.value !== null) {
      state.pendingClubJoin = pendingClubJoin.value
    }

    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(state))
  }

  const loadState = () => {
    const savedState = localStorage.getItem(AUTH_STORAGE_KEY)
    if (!savedState) return

    try {
      const {
        user: savedUser,
        accessToken: savedAccessToken,
        refreshToken: savedRefreshToken,
        isAuthenticated: savedIsAuthenticated,
        pendingClubJoin: savedPendingClubJoin,
      } = JSON.parse(savedState) as Partial<AuthState>

      user.value = savedUser || null
      accessToken.value = savedAccessToken || null
      refreshToken.value = savedRefreshToken || null
      isAuthenticated.value = savedIsAuthenticated || false
      pendingClubJoin.value = savedPendingClubJoin || null

      if (accessToken.value) {
        updateAxiosAuthHeader(accessToken.value)
      }
    } catch (error) {
      console.error('Failed to parse auth state from localStorage', error)
      localStorage.removeItem(AUTH_STORAGE_KEY)
    }
  }

  const requestCode = async (email: string) => {
    await axios.post('/api/v1/auth/code/', { email })
  }

  const verifyCode = async (email: string, code: string) => {
    const response = await axios.post<TokenResponse>('/api/v1/auth/code/verify/', {
      email,
      code,
    })

    accessToken.value = response.data.access
    refreshToken.value = response.data.refresh
    isAuthenticated.value = true

    updateAxiosAuthHeader(accessToken.value)
    await fetchUser()
    saveState()
  }

  const fetchUser = async () => {
    if (!accessToken.value) return

    try {
      const response = await axios.get<User>('/api/v1/users/me/')
      user.value = response.data
      saveState()
    } catch (error) {
      const axiosError = error as AxiosError
      if (axiosError.response?.status === 401) {
        if (await refreshTokens()) {
          await fetchUser()
        } else {
          logout()
        }
      } else {
        throw error
      }
    }
  }

  const updateUser = async (userData: Partial<User>) => {
    if (!accessToken.value) {
      throw new Error('No access token')
    }

    try {
      const response = await axios.patch<User>('/api/v1/users/me/', userData)
      user.value = response.data
      saveState()
      return response.data
    } catch (error) {
      console.error('Failed to update user:', error)
      throw error
    }
  }

  const refreshTokens = async (): Promise<boolean> => {
    if (!refreshToken.value) {
      logout()
      return false
    }

    try {
      const response = await axios.post<TokenResponse>(REFRESH_ENDPOINT, {
        refresh: refreshToken.value,
      })

      accessToken.value = response.data.access
      refreshToken.value = response.data.refresh || refreshToken.value
      isAuthenticated.value = true

      updateAxiosAuthHeader(accessToken.value)
      saveState()
      return true
    } catch (error) {
      console.error('Token refresh failed:', error)
      logout()
      return false
    }
  }

  const logout = () => {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    isAuthenticated.value = false
    pendingClubJoin.value = null

    updateAxiosAuthHeader(null)
    localStorage.removeItem(AUTH_STORAGE_KEY)
  }

  loadState()

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    pendingClubJoin,
    requestCode,
    verifyCode,
    logout,
    fetchUser,
    updateUser,
    refreshTokens,
    loadState,
    setPendingClubJoin,
    clearPendingClubJoin,
  }
})

axios.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean }
    const authStore = useAuthStore()

    if (
      originalRequest.url === REFRESH_ENDPOINT ||
      originalRequest._retry ||
      error.response?.status !== 401
    ) {
      return Promise.reject(error)
    }

    originalRequest._retry = true

    try {
      const refreshed = await authStore.refreshTokens()
      if (refreshed && authStore.accessToken) {
        originalRequest.headers = originalRequest.headers || {}
        originalRequest.headers['Authorization'] = `Bearer ${authStore.accessToken}`
        return axios(originalRequest)
      }
    } catch (refreshError) {
      console.error('Failed to refresh token:', refreshError)
    }

    authStore.logout()
    return Promise.reject(error)
  },
)
