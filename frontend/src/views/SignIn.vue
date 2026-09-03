<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import heroImg from '@/assets/images/eugene-golovesov-zUuJz_idfqM-unsplash.jpg'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const step = ref<'email' | 'code'>('email')
const form = reactive({
  email: '',
  code: '',
})
const error = ref('')
const isLoading = ref(false)

async function requestCodeHandler() {
  isLoading.value = true
  error.value = ''
  try {
    await authStore.requestCode(form.email)
    step.value = 'code'
  } catch (e) {
    const err = e as { detail?: string }
    error.value = err.detail || 'Ошибка при отправке кода'
  } finally {
    isLoading.value = false
  }
}

async function verifyCodeHandler() {
  isLoading.value = true
  error.value = ''
  try {
    await authStore.verifyCode(form.email, form.code)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : ''
    if (redirect) {
      router.push(redirect)
      return
    }
    const joinClubId = route.query.join
    if (joinClubId) {
      router.push({ name: 'club-details', params: { id: Number(joinClubId) } })
    } else {
      router.push('/clubs')
    }
  } catch (e) {
    const err = e as { detail?: string }
    error.value = err.detail || 'Неверный код подтверждения'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="auth-page" data-testid="login-page">
    <button class="auth-close" @click="router.push('/clubs')" aria-label="Закрыть">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M5 5L15 15M15 5L5 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </button>

    <div class="auth-card" :style="{ backgroundImage: `url(${heroImg})` }" data-testid="login-container">
      <div class="auth-card-overlay" />

      <div class="auth-body">
        <h1 class="auth-title">Вход</h1>

        <form v-if="step === 'email'" @submit.prevent="requestCodeHandler" class="auth-form" data-testid="login-form-element">
          <div class="field">
            <label for="email">Электропочта</label>
            <input
              v-model="form.email"
              type="email"
              id="email"
              required
              placeholder="example@yandex.ru"
              class="input"
              data-testid="email-input"
            />
          </div>
          <button type="submit" class="auth-submit" :disabled="isLoading" data-testid="submit-button">
            {{ isLoading ? 'Отправка…' : 'Получить код' }}
          </button>
          <p v-if="error" class="error-msg">{{ error }}</p>
        </form>

        <form v-else @submit.prevent="verifyCodeHandler" class="auth-form">
          <div class="field">
            <label for="code">Код из письма</label>
            <input
              v-model="form.code"
              type="text"
              id="code"
              required
              inputmode="numeric"
              maxlength="4"
              placeholder="0000"
              class="input"
              data-testid="code-input"
              autocomplete="one-time-code"
            />
          </div>
          <button type="submit" class="auth-submit" :disabled="isLoading || form.code.length !== 4" data-testid="verify-button">
            {{ isLoading ? 'Проверка…' : 'Подтвердить' }}
          </button>
          <p v-if="error" class="error-msg">{{ error }}</p>
          <p class="auth-recovery">Если код не пришёл — проверьте «Спам»</p>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  position: fixed;
  inset: 0;
  z-index: 200;
  display: flex;
  padding: 24px;
}

.auth-close {
  position: absolute;
  top: 36px;
  right: 36px;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.12);
  color: rgba(255, 255, 255, 0.8);
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.auth-close:hover {
  background: rgba(255, 255, 255, 0.24);
  color: #FFFFFF;
}

.auth-card {
  position: relative;
  width: 100%;
  border-radius: var(--radius-lg);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.auth-card-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
}

.auth-card > *:not(.auth-card-overlay) {
  position: relative;
  z-index: 1;
}

.auth-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 28px 28px;
  gap: 20px;
}

.auth-title {
  font-family: var(--font-heading);
  font-size: 34px;
  font-weight: 500;
  line-height: 1.1;
  text-align: center;
  color: #FFFFFF;
  margin: 0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 440px;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
}

.field label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.8);
}

.input {
  width: 100%;
  height: 52px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-md);
  padding: 0 18px;
  font-family: var(--font-body);
  font-size: 17px;
  color: #FFFFFF;
  transition: border-color var(--duration-fast) var(--ease-out), background var(--duration-fast) var(--ease-out);
}

.input::placeholder {
  color: rgba(255, 255, 255, 0.45);
}

.input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.18);
}

.auth-submit {
  height: 52px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.12);
  cursor: pointer;
  font-family: var(--font-body);
  font-size: 17px;
  font-weight: 600;
  color: #FFFFFF;
  transition: background 0.2s ease, border-color 0.2s ease;
}

.auth-submit:hover {
  background: rgba(255, 255, 255, 0.22);
  border-color: rgba(255, 255, 255, 0.5);
}

.auth-submit:active {
  background: rgba(255, 255, 255, 0.28);
}

.auth-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.auth-recovery {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.5;
  text-align: center;
  margin: 0;
}

.error-msg {
  color: #FFB3B3;
  text-align: center;
  font-size: 15px;
  font-weight: 500;
  margin: 0;
}

@media (max-width: 480px) {
  .auth-page {
    padding: 16px;
  }

  .auth-close {
    top: 28px;
    right: 28px;
  }

  .auth-title {
    font-size: 26px;
  }

  .auth-body {
    padding: 0 20px 20px;
  }

  .input {
    height: 46px;
    padding: 0 14px;
    font-size: 16px;
  }

  .auth-submit {
    height: 46px;
    font-size: 16px;
  }
}
</style>
