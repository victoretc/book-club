<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

const route = useRoute()
const menuOpen = ref(false)

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value
}

const closeMenu = () => {
  menuOpen.value = false
}

watch(
  () => route.fullPath,
  () => closeMenu(),
)

function onDocumentClick(event: MouseEvent) {
  const target = event.target
  if (!(target instanceof Element) || !target.closest('.header')) {
    closeMenu()
  }
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', onDocumentClick)
  document.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocumentClick)
  document.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <header class="header" data-testid="header">
    <div class="header-inner">
      <nav class="header-left" data-testid="main-nav">
        <router-link to="/clubs" class="nav-link" data-testid="clubs-link">Клубы</router-link>
        <router-link v-if="isAuthenticated" to="/clubs/create" class="nav-link" data-testid="create-club-link">
          Создать клуб
        </router-link>
      </nav>

      <router-link to="/clubs" class="header-brand" data-testid="logo-link">
        <span class="header-brand-name">Читальная</span>
      </router-link>

      <nav class="header-right">
        <router-link v-if="isAuthenticated" to="/profile" class="nav-link" data-testid="profile-link">
          Профиль
        </router-link>
        <router-link v-if="!isAuthenticated" to="/signin" class="nav-link nav-link--cta">
          Войти
        </router-link>

        <button
          class="burger"
          type="button"
          data-testid="burger-button"
          :aria-label="menuOpen ? 'Закрыть меню' : 'Открыть меню'"
          aria-controls="mobile-nav"
          :aria-expanded="menuOpen"
          @click="toggleMenu"
        >
          <span class="burger-bar" />
          <span class="burger-bar" />
        </button>
      </nav>
    </div>

    <Transition name="mobile-menu">
      <div v-if="menuOpen" class="mobile-menu">
        <router-link to="/clubs" class="mobile-menu-link">Клубы</router-link>
        <router-link v-if="isAuthenticated" to="/clubs/create" class="mobile-menu-link">
          Создать клуб
        </router-link>
        <router-link v-if="isAuthenticated" to="/profile" class="mobile-menu-link">Профиль</router-link>
        <router-link v-if="!isAuthenticated" to="/signin" class="mobile-menu-link">Войти</router-link>
      </div>
    </Transition>
  </header>
</template>

<style scoped>
.header {
  position: relative;
  z-index: 100;
  padding: 16px 24px 0;
}

.header-inner {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 1120px;
  margin: 0 auto;
  padding: 14px 12px;
  border-radius: 100px;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow:
    0 1px 2px rgba(0, 0, 0, 0.04),
    0 4px 16px rgba(0, 0, 0, 0.04);
  transition:
    box-shadow 0.3s var(--ease-out),
    background 0.3s var(--ease-out);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
}

.header-brand {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  text-decoration: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 24px;
  flex-shrink: 0;
  z-index: 1;
}

.header-brand-name {
  font-family: var(--font-display);
  font-size: 22px;
  font-weight: 400;
  line-height: 1;
  color: var(--color-text);
  transition: opacity 0.2s ease;
}

.header-brand:hover .header-brand-name {
  opacity: 0.7;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 2px;
  flex: 1;
  justify-content: flex-end;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: 100px;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  line-height: 1;
  color: var(--color-text-secondary);
  text-decoration: none;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  background: transparent;
  transition:
    color 0.2s ease,
    background 0.2s ease;
}

.nav-link:hover {
  color: var(--color-text);
  background: rgba(0, 0, 0, 0.04);
}

.nav-link.router-link-active {
  color: var(--color-text);
  background: rgba(0, 0, 0, 0.06);
}

.nav-link--cta {
  color: var(--color-brand);
  font-weight: 600;
}

.nav-link--cta:hover {
  color: #2e30cc;
  background: var(--color-brand-soft);
}

.burger {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 36px;
  height: 36px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-left: 4px;
}

.burger:hover {
  background: rgba(0, 0, 0, 0.04);
}

.burger-bar {
  display: block;
  width: 18px;
  height: 1.5px;
  border-radius: 2px;
  background: var(--color-text);
  transition:
    transform 0.3s var(--ease-out),
    opacity 0.3s var(--ease-out);
  transform-origin: center;
}

.burger[aria-expanded='true'] .burger-bar:first-child {
  transform: translateY(3.25px) rotate(45deg);
}

.burger[aria-expanded='true'] .burger-bar:last-child {
  transform: translateY(-3.25px) rotate(-45deg);
}

.mobile-menu {
  display: none;
  flex-direction: column;
  gap: 2px;
  max-width: 1120px;
  margin: 8px auto 0;
  padding: 8px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.mobile-menu-link {
  display: block;
  padding: 12px 16px;
  border-radius: 12px;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: color 0.2s ease, background 0.2s ease;
}

.mobile-menu-link:hover {
  color: var(--color-text);
  background: rgba(0, 0, 0, 0.04);
}

.mobile-menu-link.router-link-active {
  color: var(--color-text);
  background: rgba(0, 0, 0, 0.06);
}

.mobile-menu-enter-active {
  transition: opacity 0.2s ease, transform 0.2s var(--ease-out);
}

.mobile-menu-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.mobile-menu-enter-from {
  opacity: 0;
  transform: translateY(-8px) scale(0.96);
}

.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-4px) scale(0.98);
}

@media (max-width: 640px) {
  .header {
    padding: 10px 12px;
  }

  .header-inner {
    padding: 10px 10px 10px 16px;
  }

  .header-left {
    display: none;
  }

  .header-right .nav-link {
    display: none;
  }

  .burger {
    display: flex;
  }

  .header-brand {
    position: static;
    transform: none;
    padding: 0;
  }

  .mobile-menu {
    display: flex;
  }
}
</style>
