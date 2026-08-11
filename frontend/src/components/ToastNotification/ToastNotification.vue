<script setup lang="ts">
import { useToast, hideToast } from '@/stores/toast'

const toast = useToast()
</script>

<template>
  <Teleport to="body">
    <div v-if="toast.visible" class="toast" :class="`toast--${toast.type}`" role="status" @click="hideToast">
      <svg v-if="toast.type === 'error'" class="toast-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10" />
        <line x1="9" y1="9" x2="15" y2="15" />
        <line x1="15" y1="9" x2="9" y2="15" />
      </svg>
      <svg v-else class="toast-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10" />
        <polyline points="8 12 11 15 16 9" />
      </svg>
      <span class="toast-text">{{ toast.message }}</span>
      <button class="toast-close" aria-label="Закрыть уведомление" @click.stop="hideToast">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="5" y1="5" x2="19" y2="19" />
          <line x1="19" y1="5" x2="5" y2="19" />
        </svg>
      </button>
    </div>
  </Teleport>
</template>

<style scoped>
.toast {
  position: fixed;
  top: 16px;
  right: 24px;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 12px;
  max-width: 380px;
  padding: 14px 16px;
  border: 1px solid var(--color-stroke-subtle);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  color: var(--color-text);
  box-shadow: var(--shadow-md);
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  cursor: pointer;
  animation: toast-in 0.3s var(--ease-out);
}

.toast--error {
  border-left: 3px solid var(--color-error);
}

.toast--error .toast-icon {
  color: var(--color-error);
}

.toast--success {
  border-left: 3px solid var(--color-success);
}

.toast--success .toast-icon {
  color: var(--color-success);
}

.toast-icon {
  flex-shrink: 0;
}

.toast-text {
  flex: 1;
  color: var(--color-text);
}

.toast-close {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  margin: -2px -4px -2px 0;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: color 0.2s ease, background 0.2s ease;
}

.toast-close:hover {
  color: var(--color-text);
  background: var(--color-brand-soft);
}

@keyframes toast-in {
  from {
    opacity: 0;
    transform: translateX(16px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
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
