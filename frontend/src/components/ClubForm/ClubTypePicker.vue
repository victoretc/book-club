<script setup lang="ts">
import type { ClubTypeEnum } from '@/api/Api'

defineOptions({ name: 'ClubTypePicker' })

const emit = defineEmits<{
  select: [type: ClubTypeEnum]
}>()

const choose = (type: ClubTypeEnum) => {
  emit('select', type)
}
</script>

<template>
  <div class="type-picker" data-testid="club-type-picker" role="group" aria-label="Тип клуба">
    <div class="type-picker__content">
      <h2 class="type-picker__title">Какой клуб хочешь создать?</h2>

      <div class="type-picker__options">
        <button
          type="button"
          class="type-option"
          data-testid="club-type-pill-book"
          @click="choose('book' as ClubTypeEnum)"
        >
          <span class="type-option__capsule type-option__capsule--blue" aria-hidden="true" />
          <span class="type-option__title">Клуб по книге</span>
        </button>

        <button
          type="button"
          class="type-option"
          data-testid="club-type-pill-author"
          @click="choose('author' as ClubTypeEnum)"
        >
          <span class="type-option__capsule type-option__capsule--red" aria-hidden="true" />
          <span class="type-option__title">Авторский клуб</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.type-picker {
  width: 100%;
  background: var(--color-surface);
  border: 1px solid var(--color-stroke-subtle);
  border-radius: var(--radius-2xl);
  box-shadow: var(--shadow-sm);
}

.type-picker__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 48px 40px 40px;
}

.type-picker__title {
  margin: 0;
  font-family: var(--font-heading);
  font-size: 34px;
  font-weight: 500;
  line-height: 1.1;
  color: var(--color-text);
}

.type-picker__options {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
  width: 100%;
  max-width: 640px;
  margin-top: 40px;
}

.type-option {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 28px 20px;
  border: 1px solid var(--color-stroke-subtle);
  border-radius: var(--radius-xl);
  background: var(--color-surface);
  font-family: var(--font-body);
  cursor: pointer;
  text-align: center;
  transition:
    transform var(--duration-normal) var(--ease-out),
    box-shadow var(--duration-normal) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}

.type-option:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-stroke-subtle);
}

.type-option:active {
  transform: translateY(0);
}

.type-option:focus-visible {
  outline: 2px solid var(--color-brand);
  outline-offset: 2px;
}

.type-option__capsule {
  width: 56px;
  height: 22px;
  border-radius: var(--radius-pill);
  border: 2px solid currentColor;
  position: relative;
  display: block;
}

.type-option__capsule::after {
  content: '';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: currentColor;
}

.type-option__capsule--blue {
  color: var(--color-brand);
}

.type-option__capsule--blue::after {
  left: 4px;
  background: var(--color-brand);
  box-shadow: 0 0 14px var(--color-brand-ring);
}

.type-option__capsule--red {
  color: #E05353;
}

.type-option__capsule--red::after {
  right: 4px;
  background: #E05353;
  box-shadow: 0 0 14px rgba(224, 83, 83, 0.4);
}

.type-option__title {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 500;
  line-height: 1.15;
  color: var(--color-text);
}

@media (max-width: 640px) {
  .type-picker__content {
    padding: 36px 20px 28px;
  }

  .type-picker__title {
    font-size: 26px;
  }

  .type-picker__options {
    grid-template-columns: 1fr;
    gap: 14px;
    max-width: 340px;
  }

  .type-option {
    padding: 22px 18px;
  }
}
</style>
