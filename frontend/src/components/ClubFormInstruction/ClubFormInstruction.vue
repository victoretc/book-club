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
                <linearGradient
                  id="modal-cover-grad"
                  x1="86"
                  y1="64"
                  x2="214"
                  y2="124"
                  gradientUnits="userSpaceOnUse"
                >
                  <stop offset="0" stop-color="#5A5DFF" />
                  <stop offset="1" stop-color="#3336FF" />
                </linearGradient>
              </defs>

              <circle cx="62" cy="-30" r="78" fill="var(--color-brand-soft)" />
              <circle cx="252" cy="86" r="19" fill="none" stroke="var(--color-brand-soft)" stroke-width="6" />

              <ellipse cx="150" cy="128" rx="74" ry="7" fill="rgba(26, 28, 43, 0.06)" />

              <path d="M150 64 C 128 66, 104 70, 82 76 L 82 112 C 106 118, 126 120, 150 126 Z" fill="url(#modal-cover-grad)" />
              <path d="M150 64 C 172 66, 196 70, 218 76 L 218 112 C 194 118, 174 120, 150 126 Z" fill="url(#modal-cover-grad)" />

              <path d="M150 58 C 134 60, 112 63, 88 68 L 88 106 C 112 111, 134 112, 150 117 Z" fill="#FFFFFF" />
              <path d="M150 58 C 166 60, 188 63, 212 68 L 212 106 C 188 111, 166 112, 150 117 Z" fill="#FFFFFF" />

              <path d="M150 58 L150 117" stroke="rgba(26, 28, 43, 0.1)" stroke-width="1.5" />

              <path d="M101 81 L133 78" stroke="var(--color-brand)" stroke-opacity="0.15" stroke-width="5" stroke-linecap="round" />
              <path d="M101 93 L126 90" stroke="var(--color-brand)" stroke-opacity="0.15" stroke-width="5" stroke-linecap="round" />
              <path d="M101 105 L115 103" stroke="var(--color-brand)" stroke-opacity="0.15" stroke-width="5" stroke-linecap="round" />
              <path d="M167 78 L199 81" stroke="var(--color-brand)" stroke-opacity="0.15" stroke-width="5" stroke-linecap="round" />
              <path d="M174 90 L199 93" stroke="var(--color-brand)" stroke-opacity="0.15" stroke-width="5" stroke-linecap="round" />
              <path d="M185 103 L199 105" stroke="var(--color-brand)" stroke-opacity="0.15" stroke-width="5" stroke-linecap="round" />

              <path d="M146 32 h8 v20 l-4 5 -4 -5 z" fill="var(--color-accent)" />

              <path d="M238 38 v12 M232 44 h12" stroke="var(--color-accent)" stroke-width="3" stroke-linecap="round" />
              <circle cx="94" cy="38" r="2.5" fill="var(--color-brand)" opacity="0.4" />
              <circle cx="42" cy="116" r="3" fill="var(--color-accent)" opacity="0.5" />
            </svg>
          </div>

          <h2 id="club-form-instruction-title" class="modal-title">Как создать клуб</h2>

          <p class="modal-text">
            На странице клубов — все доступные клубы. Хочешь найти участников для книги,
            которой ещё нет в Читальной? Отправь запрос на создание клуба.
          </p>

          <p class="modal-text">
            Заполни форму: <strong>Название книги</strong>, <strong>Автор(ы) книги</strong>,
            <strong>Год выпуска</strong> и <strong>Описание книги</strong>. Выбери <strong>Категорию</strong>,
            при необходимости — <strong>Подкатегорию</strong>. Нажми «Создать клуб».
          </p>

          <p class="modal-text">
            Администратор увидит заявку и создаст чаты в Max и Telegram. Когда всё будет готово,
            клуб появится на главной странице, а тебе на почту придёт письмо.
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
  font-size: 17px;
  line-height: 1.6;
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
    font-size: 16px;
  }
}
</style>
