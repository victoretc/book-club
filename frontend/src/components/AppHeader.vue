<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
</script>

<template>
  <header class="header" data-testid="header">
    <div class="header-inner">
      <router-link to="/" class="brand" data-testid="logo-link">
        Читальная
      </router-link>

      <nav class="nav" data-testid="main-nav">
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

@media (max-width: 768px) {
  .header-inner {
    flex-direction: column;
    gap: 12px;
    padding: 16px;
  }

  .nav {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
    gap: 4px;
  }

  .nav-btn {
    padding: 6px 10px;
    font-size: 14px;
  }

  .nav-btn svg {
    width: 20px;
    height: 20px;
  }
}
</style>
