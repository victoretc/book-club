<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import heroDesktop from '@/assets/images/nasa-image.jpg'
import heroMobile from '@/assets/images/nasa-image-without-human.png'

defineOptions({ name: 'LandingPage' })

const router = useRouter()

const headerHeight = ref('0px')
const isImageLoaded = ref(false)

function updateHeaderHeight() {
  const h = document.querySelector('[data-testid="header"]')?.getBoundingClientRect().height ?? 0
  headerHeight.value = `${h}px`
}

function heroSrc() {
  return window.innerWidth >= 1025 ? heroDesktop : heroMobile
}

onMounted(() => {
  updateHeaderHeight()
  window.addEventListener('resize', updateHeaderHeight)
  const img = new Image()
  img.onload = () => {
    isImageLoaded.value = true
  }
  img.src = heroSrc()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateHeaderHeight)
})

const openClubs = () => router.push('/clubs')
</script>

<template>
  <div
    class="landing"
    :style="{ '--hero-desktop': `url('${heroDesktop}')`, '--hero-mobile': `url('${heroMobile}')` }"
  >
    <div class="landing-bg" aria-hidden="true" data-testid="landing-background">
      <div class="landing-bg-img" :class="{ 'is-loaded': isImageLoaded }" />
      <div class="landing-bg-overlay" />
    </div>
    <section class="hero">
      <h1 class="hero-title">
        Не с кем почитать книгу?
        <span class="hero-title-accent">Решим.</span>
      </h1>
      <p class="hero-subtitle">
        Если на сайте не найдете клуб по книге, которую читаете, — вы всегда сможете создать клуб,
        а мы поможем найти собеседников.
      </p>
      <!-- <span class="hero-rule" aria-hidden="true" /> -->
      <button type="button" class="landing-cta" @click="openClubs">Смотреть клубы</button>
    </section>
  </div>
</template>

<style scoped>
.landing {
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  height: calc(100vh - v-bind(headerHeight));
  height: calc(100dvh - v-bind(headerHeight));
  padding: 10vh 48px 0 0;
}

@media (max-width: 768px) {
  .landing {
    padding: 10vh 24px 0;
  }
}

.landing-bg {
  position: fixed;
  inset: 0;
  z-index: -1;
  background: #0d1024;
}

.landing-bg-img {
  position: absolute;
  inset: 0;
  background: var(--hero-desktop) right center / 120% auto no-repeat;
  opacity: 0;
  transition: opacity var(--duration-normal) ease;
}

@media (orientation: portrait) {
  .landing-bg-img {
    background-size: cover;
  }
}

@media (max-width: 1024px) {
  .landing-bg-img {
    background: var(--hero-mobile) center / cover no-repeat;
  }
}

.landing-bg-img.is-loaded {
  opacity: 1;
}

.landing-bg-overlay {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(8, 10, 24, 0.42) 0%, rgba(8, 10, 24, 0.05) 42%, rgba(8, 10, 24, 0.32) 100%);
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  max-width: 680px;
  padding: 48px 0;
}

.hero-title {
  font-family: var(--font-heading);
  font-size: 64px;
  font-weight: 500;
  line-height: 1.08;
  letter-spacing: -0.02em;
  color: #ffffff;
  margin: 0;
}

.hero-title-accent {
  color: #b3b6ff;
}

.hero-subtitle {
  margin: 24px 0 0;
  max-width: 520px;
  font-family: var(--font-body);
  font-size: 19px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.82);
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
  margin: 40px 0 36px;
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
