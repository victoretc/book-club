<script setup lang="ts">
import AppHeader from '@/components/AppHeader/AppHeader.vue'
import ToastNotification from '@/components/ToastNotification/ToastNotification.vue'
</script>

<template>
  <div class="app-layout">
    <AppHeader />
    <main>
      <router-view />
    </main>
    <ToastNotification />
  </div>
</template>

<style>
@import '@/assets/main.css';

.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 24px 60px;
}

@media (max-width: 768px) {
  main {
    padding: 24px 16px 40px;
  }
}
</style>
