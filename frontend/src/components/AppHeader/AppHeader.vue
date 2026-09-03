<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import heroImg from '@/assets/images/eugene-golovesov-zUuJz_idfqM-unsplash.jpg'

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
    <div class="capsule">
      <nav class="capsule-left" data-testid="main-nav">
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

        <router-link v-if="isAuthenticated" to="/clubs/create" class="nav-pill" data-testid="create-club-link">
          Создать клуб
        </router-link>

        <router-link to="/clubs" class="nav-pill" data-testid="clubs-link">
          Клубы
        </router-link>
      </nav>

      <router-link to="/clubs" class="capsule-brand" data-testid="logo-link">
        <span class="capsule-brand-name">Читальная</span>
        <span class="capsule-brand-tagline">Не с кем читать? Решим!</span>
      </router-link>

      <nav class="capsule-right">
        <router-link v-if="isAuthenticated" to="/profile" class="nav-pill" data-testid="profile-link">
          Профиль
        </router-link>

        <router-link v-if="!isAuthenticated" to="/signin" class="nav-pill">
          Войти
        </router-link>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  justify-content: center;
  padding: 14px 24px;
}

.capsule {
  position: relative;
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px 28px;
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 1400px;
}

.capsule-left {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
}

.capsule-brand {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  flex-shrink: 0;
  padding: 0 20px;
}

.capsule-brand-name {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 400;
  line-height: 1.1;
  color: var(--color-text);
}

.capsule-brand-tagline {
  font-family: var(--font-heading);
  font-size: 11px;
  font-weight: 500;
  line-height: 1.2;
  color: var(--color-text-secondary);
  letter-spacing: 0.02em;
}

.capsule-right {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
  justify-content: flex-end;
}

.nav-pill {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  border-radius: 100px;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.2;
  color: var(--color-text-secondary);
  text-decoration: none;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  background: var(--color-bg);
  transition:
    color 0.2s ease,
    background 0.2s ease;
}

.nav-pill:hover {
  color: var(--color-text);
  background: var(--color-stroke-subtle);
}

.nav-pill:active {
  color: var(--color-text);
}

.nav-pill.router-link-active {
  color: var(--color-text);
  background: var(--color-stroke-subtle);
}

.burger {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
  width: 36px;
  height: 36px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: var(--color-bg);
  cursor: pointer;
  transition: background 0.2s ease;
}

.burger:hover {
  background: var(--color-stroke-subtle);
}

.burger-bar {
  display: block;
  width: 18px;
  height: 2px;
  border-radius: 2px;
  background: var(--color-text);
  transition:
    transform 0.25s var(--ease-out),
    opacity 0.25s var(--ease-out);
}

.burger[aria-expanded='true'] .burger-bar:nth-child(1) {
  transform: translateY(6px) rotate(45deg);
}

.burger[aria-expanded='true'] .burger-bar:nth-child(2) {
  opacity: 0;
}

.burger[aria-expanded='true'] .burger-bar:nth-child(3) {
  transform: translateY(-6px) rotate(-45deg);
}

@media (hover: none) {
  .nav-pill:hover {
    color: inherit;
    background: rgba(255, 255, 255, 0.12);
  }
}

@media (max-width: 600px) {
  .header {
    padding: 10px 12px;
  }

  .capsule {
    padding: 10px 14px;
    gap: 8px;
  }

  .capsule-brand {
    font-size: 20px;
    padding: 0 12px;
  }

  .burger {
    display: inline-flex;
  }

  .capsule-left .nav-pill,
  .capsule-right .nav-pill {
    display: none;
  }

  .burger[aria-expanded='true'] ~ .capsule-brand {
    display: none;
  }

  .capsule-left {
    flex: 0;
  }

  .capsule-right {
    flex: 0;
  }
}
</style>
