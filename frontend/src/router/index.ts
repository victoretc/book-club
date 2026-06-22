import { createRouter, createWebHistory } from 'vue-router'
import { beforeEachGuard } from './middleware'

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
      beforeEnter: [async (to) => {
        const { useAuthStore } = await import('@/stores/auth')
        const { api } = await import('@/api')
        const authStore = useAuthStore()
        if (!authStore.user) return

        try {
          const { data: club } = await api.api.clubsRetrieve(Number(to.params.id))
          if (Number(club.owner) !== Number(authStore.user.id)) {
            return { name: 'clubs' }
          }
        } catch {
          return { name: 'clubs' }
        }
      }],
    },
    {
      path: '/clubs/:id',
      name: 'club-details',
      component: () => import('@/views/ClubDetails.vue'),
      meta: {
        requiresAuth: true,
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

router.beforeEach(beforeEachGuard)

export default router
