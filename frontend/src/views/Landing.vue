<script setup lang="ts">
import { useRouter } from 'vue-router'

defineOptions({ name: 'LandingPage' })

const router = useRouter()

const openClubs = () => router.push('/clubs')
</script>

<template>
  <div class="landing">
    <section class="hero">
      <h1 class="hero-title">
        Не с кем почитать книгу?
        <span class="hero-title-accent">Решим.</span>
      </h1>
      <p class="hero-subtitle">
        Если на сайте не найдете клуб по книге, которую читаете, — вы всегда сможете создать клуб,
        а мы поможем найти собеседников.
      </p>
      <span class="hero-rule" aria-hidden="true" />
      <button type="button" class="landing-cta" @click="openClubs">Смотреть клубы</button>
    </section>
  </div>
</template>

<style scoped>
.landing {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 680px;
  padding: 48px 0;
}

.hero-title {
  font-family: var(--font-heading);
  font-size: 64px;
  font-weight: 500;
  line-height: 1.08;
  letter-spacing: -0.02em;
  color: var(--color-text);
  margin: 0;
}

.hero-title-accent {
  color: var(--color-brand);
}

.hero-subtitle {
  margin: 24px 0 0;
  max-width: 520px;
  font-family: var(--font-body);
  font-size: 19px;
  line-height: 1.6;
  color: var(--color-text-secondary);
}

.hero-rule {
  width: 48px;
  height: 3px;
  margin: 40px 0 36px;
  border-radius: 2px;
  background: var(--color-accent);
}

.landing-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 16px 36px;
  border: none;
  border-radius: var(--radius-pill);
  background: var(--color-brand);
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  line-height: 1.2;
  color: #ffffff;
  cursor: pointer;
  box-shadow: 0 10px 24px -10px rgba(59, 62, 255, 0.45);
  transition: background var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out);
}

.landing-cta:hover {
  background: #2f31d6;
  transform: translateY(-1px);
  box-shadow: 0 14px 28px -10px rgba(59, 62, 255, 0.5);
}

.landing-cta:active {
  transform: scale(0.98);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 48px;
  }

  .hero-subtitle {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .hero-rule {
    margin: 32px 0 28px;
  }

  .landing-cta {
    width: 100%;
    max-width: 320px;
  }
}
</style>
