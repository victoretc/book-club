<script setup lang="ts">
import { useRouter } from 'vue-router'

defineOptions({ name: 'LandingPage' })

const router = useRouter()

const steps = [
  {
    num: '01',
    title: 'Найдите книгу',
    text: 'Ищите по названию или категории. Не нашли — оставьте заявку: клуб создадут, вам пришлют уведомление.',
  },
  {
    num: '02',
    title: 'Вступите в клуб',
    text: 'Одна кнопка на странице книги. Чат клуба открывается в Telegram или Max — ничего ставить не нужно.',
  },
  {
    num: '03',
    title: 'Читайте и отмечайте',
    text: 'Оставьте рецензию: оценка и число прочитанных страниц. Книга появится в вашем списке прочитанного.',
  },
]

const openClubs = () => router.push('/clubs')
</script>

<template>
  <div class="landing">
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-copy">
          <p class="hero-kicker">
            <span class="hero-kicker-dot" />
            Книжные клубы по одной книге
          </p>
          <h1 class="hero-title">
            Не с кем почитать книгу?
            <span class="hero-title-accent">Мы соберём клуб</span>
          </h1>
          <p class="hero-subtitle">
            Вступайте в клуб книги, которую читаете. Обсуждайте её в Telegram или Max,
            ставьте оценки и ведите список прочитанного.
          </p>
          <div class="hero-actions">
            <button type="button" class="landing-cta" @click="openClubs">Смотреть клубы</button>
            <a href="#how" class="hero-secondary">
              Как это работает
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <path d="M8 3v10M4 9l4 4 4-4" />
              </svg>
            </a>
          </div>
        </div>

        <div class="hero-art" aria-hidden="true">
          <div class="hero-art-ring" />
          <div class="book book--back book--back-left">
            <span class="book-title">Портрет в тумане</span>
            <span class="book-author">К. Орлов</span>
          </div>
          <div class="book book--back book--back-right">
            <span class="book-title">Шифр бабочки</span>
            <span class="book-author">Л. Медведева</span>
          </div>
          <div class="book book--front">
            <span class="book-title">Тихий океан</span>
            <span class="book-author">А. Верхов</span>
            <span class="book-mark" />
          </div>
          <div class="hero-float hero-float--rating">
            <span class="hero-float-stars">★★★★★</span>
            <span class="hero-float-label">4.9 · читают сейчас</span>
          </div>
          <div class="hero-float hero-float--chat">
            <span class="hero-float-label">«Кто на 214-й странице?»</span>
          </div>
        </div>
      </div>
    </section>

    <section id="how" class="how">
      <div class="how-inner">
        <div class="how-head">
          <p class="how-kicker">Как это работает</p>
          <h2 class="how-title">Три шага до первого разговора</h2>
        </div>
        <ol class="steps">
          <li v-for="step in steps" :key="step.num" class="step">
            <span class="step-num">{{ step.num }}</span>
            <div class="step-body">
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-text">{{ step.text }}</p>
            </div>
          </li>
        </ol>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg);
}

.hero {
  position: relative;
  padding: 88px 24px 96px;
}

.hero::before {
  content: '';
  position: absolute;
  top: -140px;
  right: -120px;
  width: 560px;
  height: 560px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--color-brand-ring) 0%, transparent 68%);
  pointer-events: none;
}

.hero::after {
  content: '';
  position: absolute;
  bottom: -160px;
  left: -140px;
  width: 460px;
  height: 460px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(160, 236, 6, 0.18) 0%, transparent 70%);
  pointer-events: none;
}

.hero-inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  align-items: center;
  gap: 56px;
  max-width: 1200px;
  margin: 0 auto;
}

.hero-copy {
  animation: hero-in 0.6s var(--ease-out) both;
}

@keyframes hero-in {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-kicker {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.02em;
  color: var(--color-text-secondary);
}

.hero-kicker-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--color-accent);
  box-shadow: 0 0 0 4px rgba(160, 236, 6, 0.25);
}

.hero-title {
  margin-top: 28px;
  font-family: var(--font-heading);
  font-size: 64px;
  font-weight: 500;
  line-height: 1.04;
  letter-spacing: -0.015em;
  color: var(--color-text);
}

.hero-title-accent {
  display: block;
  color: var(--color-brand);
}

.hero-subtitle {
  margin-top: 24px;
  max-width: 460px;
  font-family: var(--font-body);
  font-size: 18px;
  line-height: 1.65;
  color: var(--color-text-secondary);
}

.hero-actions {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-top: 40px;
}

.landing-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 16px 32px;
  border: none;
  border-radius: var(--radius-pill);
  background: var(--color-brand);
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  line-height: 1.2;
  color: #ffffff;
  cursor: pointer;
  box-shadow: 0 12px 28px -8px rgba(59, 62, 255, 0.55);
  transition: filter var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out);
}

.landing-cta:hover {
  filter: brightness(1.08);
  transform: translateY(-2px);
  box-shadow: 0 16px 32px -8px rgba(59, 62, 255, 0.6);
}

.landing-cta:active {
  transform: scale(0.98);
}

.hero-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
  text-decoration: none;
  transition: color var(--duration-fast) var(--ease-out);
}

.hero-secondary svg {
  transition: transform var(--duration-fast) var(--ease-out);
}

.hero-secondary:hover {
  color: var(--color-brand);
}

.hero-secondary:hover svg {
  transform: translateY(2px);
}

.hero-art {
  position: relative;
  height: 460px;
  animation: hero-in 0.6s var(--ease-out) 0.12s both;
}

.hero-art-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  border: 1px dashed rgba(26, 28, 43, 0.12);
  transform: translate(-50%, -50%);
  animation: ring-spin 40s linear infinite;
}

@keyframes ring-spin {
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

.book {
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 26px 24px;
  border-radius: 4px 16px 16px 4px;
  font-family: var(--font-heading);
  box-shadow: var(--shadow-lg);
  transform-origin: center;
  transition: transform var(--duration-normal) var(--ease-out);
}

.book-title {
  font-size: 24px;
  font-weight: 500;
  line-height: 1.12;
}

.book-author {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 500;
  opacity: 0.85;
}

.book--back {
  width: 180px;
  height: 250px;
  top: 60px;
}

.book--back::after {
  content: '';
  position: absolute;
  top: 14px;
  bottom: 14px;
  left: 14px;
  width: 1px;
  background: rgba(26, 28, 43, 0.12);
}

.book--back-left {
  left: 20px;
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-stroke-subtle);
  transform: rotate(-10deg);
}

.book--back-right {
  right: 16px;
  background: linear-gradient(135deg, #a0ec06, #8fd90a);
  color: var(--color-text);
  transform: rotate(9deg);
}

.book--back-right::after {
  background: rgba(26, 28, 43, 0.14);
}

.book--front {
  top: 34px;
  left: 50%;
  width: 236px;
  height: 330px;
  background: linear-gradient(150deg, #4b4eff, #2a2cd4);
  color: #ffffff;
  transform: translateX(-50%) rotate(-2deg);
  z-index: 3;
}

.book--front::after {
  content: '';
  position: absolute;
  top: 22px;
  bottom: 22px;
  left: 22px;
  width: 1px;
  background: rgba(255, 255, 255, 0.28);
}

.book-mark {
  position: absolute;
  top: 24px;
  right: 24px;
  width: 26px;
  height: 34px;
  background: var(--color-accent);
  border-radius: 0 4px 4px 0;
}

.hero-float {
  position: absolute;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 14px 18px;
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  border: 1px solid var(--color-stroke-subtle);
  box-shadow: var(--shadow-md);
  font-family: var(--font-body);
  z-index: 4;
  animation: float-y 5s ease-in-out infinite;
}

.hero-float--rating {
  left: -16px;
  bottom: 24px;
}

.hero-float--chat {
  right: -8px;
  top: 0;
  animation-delay: 1.2s;
}

.hero-float-stars {
  font-size: 15px;
  letter-spacing: 0.1em;
  color: #ffb400;
}

.hero-float-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.hero-float--chat .hero-float-label {
  color: var(--color-text);
}

@keyframes float-y {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.how {
  padding: 88px 24px 100px;
  border-top: 1px solid var(--color-stroke-subtle);
  background: var(--color-surface);
}

.how-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.how-head {
  max-width: 560px;
}

.how-kicker {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--color-brand);
}

.how-title {
  margin-top: 16px;
  font-family: var(--font-heading);
  font-size: 42px;
  font-weight: 500;
  line-height: 1.12;
  color: var(--color-text);
}

.steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  margin: 56px 0 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--color-stroke-subtle);
  border-radius: var(--radius-2xl);
  overflow: hidden;
}

.step {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 40px 32px;
  background: var(--color-bg);
  transition: background var(--duration-normal) var(--ease-out);
}

.step + .step {
  border-left: 1px solid var(--color-stroke-subtle);
}

.step:hover {
  background: #ffffff;
}

.step-num {
  font-family: var(--font-heading);
  font-size: 20px;
  font-weight: 500;
  color: var(--color-brand);
}

.step-title {
  font-family: var(--font-body);
  font-size: 19px;
  font-weight: 600;
  color: var(--color-text);
}

.step-text {
  margin-top: 8px;
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.65;
  color: var(--color-text-secondary);
}

@media (max-width: 1000px) {
  .hero {
    padding: 64px 24px 72px;
  }

  .hero-inner {
    grid-template-columns: 1fr;
    gap: 64px;
  }

  .hero-copy {
    max-width: 640px;
  }

  .hero-art {
    height: 400px;
    max-width: 480px;
    width: 100%;
    margin: 0 auto;
  }

  .steps {
    grid-template-columns: 1fr;
  }

  .step + .step {
    border-left: none;
    border-top: 1px solid var(--color-stroke-subtle);
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 48px 16px 56px;
  }

  .hero-title {
    font-size: 44px;
  }

  .hero-subtitle {
    font-size: 17px;
  }

  .hero-art {
    height: 340px;
  }

  .book--back {
    width: 150px;
    height: 210px;
    top: 55px;
  }

  .book--front {
    width: 200px;
    height: 280px;
  }

  .how {
    padding: 64px 16px 72px;
  }

  .how-title {
    font-size: 32px;
  }

  .step {
    padding: 32px 24px;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 40px 16px 48px;
  }

  .hero-title {
    font-size: 34px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .hero-actions .landing-cta {
    width: 100%;
  }

  .hero-secondary {
    justify-content: center;
  }

  .hero-art {
    height: 300px;
  }

  .hero-art-ring {
    width: 300px;
    height: 300px;
  }

  .book--back {
    width: 130px;
    height: 185px;
    padding: 20px 18px;
    top: 50px;
  }

  .book--front {
    width: 170px;
    height: 240px;
  }

  .book-title {
    font-size: 19px;
  }

  .hero-float--chat {
    display: none;
  }

  .hero-float--rating {
    left: 0;
  }
}
</style>
