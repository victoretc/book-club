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
      <router-link to="/" class="brand" data-testid="logo-link">
        Читальная
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
        <span class="burger-bar" />
      </button>

      <nav id="mobile-nav" class="nav" data-testid="main-nav" :class="{ 'nav--open': menuOpen }">
        <template v-if="isAuthenticated">
          <router-link to="/clubs/create" class="nav-btn" data-testid="create-club-link">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <line x1="19" y1="8" x2="19" y2="14" />
              <line x1="22" y1="11" x2="16" y2="11" />
            </svg>
            Создать клуб
          </router-link>
        </template>

        <router-link to="/" class="nav-btn" data-testid="clubs-link">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 00-3-3.87" />
            <path d="M16 3.13a4 4 0 010 7.75" />
          </svg>
          Клубы
        </router-link>

        <router-link v-if="isAuthenticated" to="/profile" class="nav-btn" data-testid="profile-link">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          Профиль
        </router-link>

        <template v-if="!isAuthenticated">
          <router-link to="/signin" class="nav-btn">
            Войти
          </router-link>
        </template>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: relative;
  z-index: 100;
  padding: 16px 0;
  border-bottom: 1px solid var(--color-stroke-subtle);
  background: var(--color-bg);
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.brand {
  font-family: var(--font-display);
  font-size: 25px;
  font-weight: 400;
  line-height: 1.138;
  color: var(--color-brand);
  text-decoration: none;
  flex-shrink: 0;
}

.nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.burger {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  width: 40px;
  height: 40px;
  padding: 0;
  border: none;
  border-radius: var(--radius-sm);
  background: transparent;
  cursor: pointer;
  transition: background 0.2s ease;
}

.burger:hover {
  background: var(--color-brand-soft);
}

.burger-bar {
  display: block;
  width: 20px;
  height: 2px;
  border-radius: 2px;
  background: var(--color-text);
  transition:
    transform 0.25s var(--ease-out),
    opacity 0.25s var(--ease-out);
}

.burger[aria-expanded='true'] .burger-bar:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
}

.burger[aria-expanded='true'] .burger-bar:nth-child(2) {
  opacity: 0;
}

.burger[aria-expanded='true'] .burger-bar:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
}

.nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 500;
  line-height: 1.2;
  color: var(--color-text);
  text-decoration: none;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  background: transparent;
  transition:
    color 0.2s ease,
    background 0.2s ease;
}

.nav-btn svg {
  width: 22px;
  height: 22px;
}

.nav-btn:hover {
  color: var(--color-brand);
  background: var(--color-brand-soft);
}

.nav-btn:active {
  color: var(--color-brand);
}

.nav-btn.router-link-active {
  color: var(--color-brand);
}

@media (hover: none) {
  .nav-btn:hover {
    color: inherit;
    background: transparent;
  }
}

@media (max-width: 768px) {
  .header {
    padding: 12px 0;
  }

  .header-inner {
    padding: 0 16px;
  }

  .brand {
    font-size: 22px;
  }

  .burger {
    display: inline-flex;
  }

  .nav {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    flex-direction: column;
    align-items: stretch;
    gap: 2px;
    padding: 0 16px 16px;
    background: var(--color-bg);
    border-bottom: 1px solid var(--color-stroke-subtle);
    overflow: hidden;
    max-height: 0;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-8px);
    transition:
      max-height 0.3s var(--ease-out),
      opacity 0.25s var(--ease-out),
      transform 0.3s var(--ease-out),
      visibility 0.3s;
  }

  .nav--open {
    max-height: 320px;
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
  }

  .nav-btn {
    justify-content: flex-start;
    padding: 10px 12px;
    font-size: 16px;
  }

  .nav-btn svg {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 10px 0;
  }

  .header-inner {
    padding: 0 12px;
  }

  .brand {
    font-size: 20px;
  }

  .nav {
    padding: 0 12px 12px;
  }
}
</style>
