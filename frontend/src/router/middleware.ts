import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import heroDesktop from '@/assets/images/nasa-image.jpg'
import heroMobile from '@/assets/images/nasa-image-without-human.png'

let heroPreloaded = false

function preloadHero() {
  if (heroPreloaded) return
  heroPreloaded = true
  const src = window.innerWidth >= 1025 ? heroDesktop : heroMobile
  const link = document.createElement('link')
  link.rel = 'preload'
  link.as = 'image'
  link.href = src
  document.head.appendChild(link)
}

export function beforeEachGuard(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext,
) {
  const authStore = useAuthStore()

  if (to.meta.fullBleed) {
    preloadHero()
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'signin' })
    return
  }

  next()
}
