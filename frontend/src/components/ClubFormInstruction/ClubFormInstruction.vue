<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref } from 'vue'
import BaseButton from '@/components/BaseButton/BaseButton.vue'

const props = defineProps<{ open: boolean }>()
const emit = defineEmits<{ close: [] }>()

const dialogRef = ref<HTMLElement | null>(null)
const closeButtonRef = ref<HTMLButtonElement | null>(null)
let previouslyFocused: HTMLElement | null = null

function close() {
  emit('close')
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    close()
  }
}

onMounted(() => {
  if (props.open) {
    previouslyFocused = document.activeElement as HTMLElement | null
    closeButtonRef.value?.focus()
  }
})

onBeforeUnmount(() => {
  previouslyFocused?.focus?.()
})
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="open"
        class="modal-overlay"
        role="presentation"
        @click.self="close"
        @keydown.esc="onKeydown"
      >
        <div
          ref="dialogRef"
          class="modal"
          role="dialog"
          aria-modal="true"
          aria-labelledby="club-form-instruction-title"
          data-testid="club-form-instruction"
        >
          <button
            ref="closeButtonRef"
            type="button"
            class="modal-close"
            aria-label="Закрыть"
            data-testid="club-form-instruction-close-button"
            @click="close"
          >
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
              <path d="M1 1 L13 13 M13 1 L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
          </button>

          <div class="modal-art" aria-hidden="true">
            <svg class="modal-art-svg" viewBox="0 0 300 140" fill="none">
              <defs>
                <linearGradient id="clubInstructionAccent" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0" stop-color="var(--color-accent)" />
                  <stop offset="1" stop-color="#7ED600" />
                </linearGradient>
                <linearGradient id="clubInstructionBrand" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0" stop-color="#5B5EFF" />
                  <stop offset="1" stop-color="#282BF0" />
                </linearGradient>
                <filter id="clubInstructionShadow" x="-30%" y="-30%" width="160%" height="160%">
                  <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="rgba(26, 28, 43, 0.16)" />
                </filter>
              </defs>

              <ellipse cx="150" cy="70" rx="118" ry="50" fill="var(--color-accent)" opacity="0.12" />

              <circle cx="24" cy="30" r="6" fill="var(--color-brand-soft)" />
              <circle cx="40" cy="46" r="4" fill="var(--color-brand)" />
              <circle cx="12" cy="52" r="3.5" fill="var(--color-accent)" />

              <g filter="url(#clubInstructionShadow)">
                <rect x="62" y="16" width="150" height="52" rx="26" fill="url(#clubInstructionAccent)" />
                <path d="M90 68 L84 90 L106 68 Z" fill="url(#clubInstructionAccent)" />
              </g>
              <rect x="88" y="34" width="92" height="8" rx="4" fill="rgba(26, 28, 43, 0.22)" />
              <rect x="88" y="50" width="58" height="8" rx="4" fill="rgba(26, 28, 43, 0.22)" />

              <g filter="url(#clubInstructionShadow)">
                <rect x="218" y="60" width="52" height="36" rx="18" fill="var(--color-surface)" stroke="url(#clubInstructionBrand)" stroke-width="3" />
                <path d="M232 96 L225 116 L246 96 Z" fill="var(--color-surface)" stroke="url(#clubInstructionBrand)" stroke-width="3" />
              </g>
              <circle cx="244" cy="78" r="4.5" fill="url(#clubInstructionBrand)" />

              <g filter="url(#clubInstructionShadow)">
                <rect x="170" y="20" width="28" height="28" rx="14" fill="url(#clubInstructionBrand)" />
                <path d="M178 48 L172 60 L186 48 Z" fill="url(#clubInstructionBrand)" />
              </g>
              <circle cx="184" cy="34" r="3.5" fill="#FFFFFF" />

              <path
                d="M254 20 L257 31 L268 34 L257 37 L254 48 L251 37 L240 34 L251 31 Z"
                fill="var(--color-accent)"
              />
            </svg>
          </div>

          <h2 id="club-form-instruction-title" class="modal-title">Как создать клуб</h2>

          <p class="modal-text">
            Приветствую! На странице клубов ты можешь найти все доступные на данный момент клубы.
            Если ты хочешь найти участников для книги, которой сейчас нет на просторах Читальной,
            ты можешь отправить запрос на создание клуба.
          </p>

          <p class="modal-text">
            Введи <strong>Название книги</strong>, <strong>Авторов(а) книги</strong>, <strong>Описание книги</strong>
            в форму, а затем кликни Создать клуб. Администратор увидит твою заявку и создаст чаты в Max, Telegram,
            клуб появится на главной странице, тебе придет уведомление на почту о том, что клуб был создан.
          </p>

          <BaseButton
            class="modal-action"
            variant="primary"
            full-width
            testId="club-form-instruction-continue-button"
            @click="close"
          >
            Понятно, перейти к созданию
          </BaseButton>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(26, 28, 43, 0.45);
  backdrop-filter: blur(4px);
}

.modal {
  position: relative;
  width: 100%;
  max-width: 520px;
  max-height: calc(100vh - 48px);
  overflow-y: auto;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 32px 36px 36px;
  box-shadow: var(--shadow-lg);
}

.modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 50%;
  background: var(--color-bg);
  color: var(--color-text-muted);
  cursor: pointer;
  transition: color var(--duration-fast) var(--ease-out), background var(--duration-fast) var(--ease-out);
}

.modal-close:hover {
  background: var(--color-brand-soft);
  color: var(--color-brand);
}

.modal-art {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: -32px -36px 20px;
  height: 150px;
  background:
    radial-gradient(120% 160% at 50% 0%, rgba(160, 236, 6, 0.16) 0%, rgba(160, 236, 6, 0) 55%),
    radial-gradient(90% 140% at 88% 100%, rgba(59, 62, 255, 0.08) 0%, rgba(59, 62, 255, 0) 60%);
}

.modal-art-svg {
  width: 280px;
  height: auto;
}

.modal-title {
  font-family: var(--font-heading);
  font-size: 26px;
  font-weight: 500;
  line-height: 1.15;
  color: var(--color-text);
  margin-bottom: 16px;
}

.modal-text {
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.65;
  color: var(--color-text-secondary);
  margin: 0 0 14px;
}

.modal-text:last-of-type {
  margin-bottom: 24px;
}

.modal-text strong {
  color: var(--color-text);
  font-weight: 600;
}

.modal-action {
  margin-top: 4px;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity var(--duration-normal) var(--ease-out);
}

.modal-enter-active .modal,
.modal-leave-active .modal {
  transition: transform var(--duration-normal) var(--ease-out);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal {
  transform: translateY(16px) scale(0.98);
}

.modal-leave-to .modal {
  transform: translateY(8px) scale(0.98);
}

@media (max-width: 600px) {
  .modal {
    padding: 24px 24px 28px;
    border-radius: 24px;
  }

  .modal-art {
    height: 116px;
    margin: -24px -24px 16px;
  }

  .modal-art-svg {
    width: 224px;
  }

  .modal-title {
    font-size: 22px;
  }

  .modal-text {
    font-size: 14px;
  }
}
</style>
