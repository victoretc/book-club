<script setup lang="ts">
import { useToast, hideToast } from '@/stores/toast'

const toast = useToast()
</script>

<template>
  <Teleport to="body">
    <div v-if="toast.visible" class="toast" :class="toast.type" @click="hideToast">
      <svg v-if="toast.type === 'error'" class="toast-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
        <circle cx="10" cy="10" r="9" stroke="currentColor" stroke-width="1.5" />
        <line x1="7" y1="7" x2="13" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
        <line x1="13" y1="7" x2="7" y2="13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
      </svg>
      <span class="toast-text">{{ toast.message }}</span>
    </div>
  </Teleport>
</template>

<style scoped>
.toast {
  position: fixed;
  top: calc(64px + 16px);
  right: 24px;
  z-index: 1000;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 20px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  max-width: 380px;
  cursor: pointer;
  animation: toast-in 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.toast.error {
  background: #fef2f2;
  color: #991b1b;
}

.toast.success {
  background: #f0fdf4;
  color: #166534;
}

.toast-icon {
  flex-shrink: 0;
  margin-top: 1px;
}

.toast-text {
  flex: 1;
}

@keyframes toast-in {
  from {
    opacity: 0;
    transform: translateX(24px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

@media (max-width: 480px) {
  .toast {
    right: 16px;
    left: 16px;
    max-width: none;
  }
}
</style>
