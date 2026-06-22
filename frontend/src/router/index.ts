import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signin',
      name: 'signin',
      component: () => import('@/views/SignIn.vue'),
      meta: { title: 'Вход' },
    },
    {
      path: '/clubs/create',
      name: 'create-club',
      component: () => import('@/views/CreateClub.vue'),
      meta: {
        requiresAuth: true,
        title: 'Создание клуба',
      },
    },
    {
      path: '/clubs/:id/edit',
      name: 'edit-club',
      component: () => import('@/views/EditClub.vue'),
      meta: {
        requiresAuth: true,
        title: 'Редактирование клуба',
      },
    },
    {
      path: '/clubs/:id',
      name: 'club-details',
      component: () => import('@/views/ClubDetails.vue'),
      meta: {
        requiresAuth: false,
        title: 'Детали клуба',
      },
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/UserProfile.vue'),
      meta: {
        requiresAuth: true,
        title: 'Профиль',
      },
    },
    {
      path: '/',
      name: 'clubs',
      component: () => import('@/views/ClubCards.vue'),
      meta: { title: 'Клубы' },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'signin' })
    return
  }

  next()
})

export default router
