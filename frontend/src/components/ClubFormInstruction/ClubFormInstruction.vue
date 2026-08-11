<script setup lang="ts">
</script>

<template>
  <aside class="instruction" data-testid="club-form-instruction">
    <div class="instruction-figures" aria-hidden="true">
      <svg class="figure figure--circle" width="120" height="120" viewBox="0 0 120 120" fill="none">
        <circle cx="60" cy="60" r="58" stroke="var(--color-accent)" stroke-width="4" />
        <circle cx="60" cy="60" r="40" fill="var(--color-accent)" />
      </svg>
      <svg class="figure figure--spark" width="64" height="64" viewBox="0 0 64 64" fill="none">
        <path d="M32 2 L38 26 L62 32 L38 38 L32 62 L26 38 L2 32 L26 26 Z" fill="var(--color-accent)" />
      </svg>
      <svg class="figure figure--blob" width="96" height="64" viewBox="0 0 96 64" fill="none">
        <path
          d="M48 4 C62 4 70 14 78 20 C86 26 96 22 94 32 C92 42 80 44 70 50 C60 56 54 60 44 60 C34 60 24 56 16 50 C8 44 0 40 2 30 C4 20 12 18 22 14 C30 10 36 4 48 4 Z"
          fill="var(--color-accent)"
          fill-opacity="0.25"
        />
      </svg>
    </div>

    <h2 class="instruction-title">Как создать клуб</h2>

    <p class="instruction-text">
      Приветствую! На странице клубов ты можешь найти все доступные на данный момент клубы.
      Если ты хочешь найти участников для книги, которой сейчас нет на просторах Читальной — ты
      можешь попросить админов создать клуб.
    </p>

    <p class="instruction-text">
      Введи <strong>Название книги</strong> *, <strong>Автор(ы) книги</strong> *, <strong>Описание книги</strong> *
      в форму, и администратор создаст чаты в Max, Telegram, клуб появится на главной странице,
      и тебе придет уведомление на почту о том, что клуб был создан.
    </p>
  </aside>
</template>

<style scoped>
.instruction {
  position: relative;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 40px 36px;
  overflow: hidden;
}

.instruction-figures {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.figure {
  position: absolute;
}

.figure--circle {
  top: -28px;
  right: -28px;
}

.figure--spark {
  top: 88px;
  left: 24px;
  opacity: 0.9;
}

.figure--blob {
  bottom: 24px;
  right: 28px;
}

.instruction-title {
  font-family: var(--font-heading);
  font-size: 26px;
  font-weight: 500;
  line-height: 1.1;
  color: var(--color-text);
  margin-bottom: 20px;
}

.instruction-text {
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.65;
  color: var(--color-text-secondary);
  margin: 0 0 16px;
  max-width: 380px;
}

.instruction-text:last-child {
  margin-bottom: 0;
}

.instruction-text strong {
  color: var(--color-text);
  font-weight: 600;
}

@media (max-width: 600px) {
  .instruction {
    padding: 28px 24px;
  }

  .figure--blob {
    display: none;
  }
}
</style>
