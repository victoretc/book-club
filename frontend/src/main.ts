import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'

const app = createApp(App)

app.use(createPinia())
app.use(router)

const authStore = useAuthStore()
authStore.loadState()
if (authStore.isAuthenticated && authStore.accessToken) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${authStore.accessToken}`
  authStore.fetchUser().catch(() => authStore.logout())
}

app.mount('#app')
