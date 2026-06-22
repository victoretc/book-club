export interface User {
  id: number
  username: string
  firstName?: string
  lastName?: string
  email?: string
  remoteAddr?: string
}

export interface TokenResponse {
  access: string
  refresh: string
}

export interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  pendingClubJoin: number | null
}
