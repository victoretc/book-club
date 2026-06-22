<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'

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
    const joinClubId = route.query.join
    if (joinClubId) {
      router.push({ name: 'club-details', params: { id: Number(joinClubId) } })
    } else {
      router.push('/')
    }
  } catch (e) {
    const err = e as { detail?: string }
    error.value = err.detail || 'Неверный код подтверждения'
  } finally {
    isLoading.value = false
  }
}

function backToEmail() {
  step.value = 'email'
  error.value = ''
}
</script>

<template>
  <div class="auth-page" data-testid="login-page">
    <div class="auth-card" data-testid="login-container">
      <h1 class="auth-title">Вход</h1>

      <form v-if="step === 'email'" @submit.prevent="requestCodeHandler" class="auth-form" data-testid="login-form-element">
        <p class="auth-hint">Введите адрес электронной почты — пришлём туда код для входа</p>
        <div class="field">
          <label for="email">Электропочта *</label>
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
        <BaseButton type="submit" variant="primary" full-width :loading="isLoading" :disabled="isLoading" data-testid="submit-button">
          Получить код
        </BaseButton>
        <p v-if="error" class="error-msg">{{ error }}</p>
      </form>

      <form v-else @submit.prevent="verifyCodeHandler" class="auth-form">
        <div class="field">
          <label for="code">Код из письма *</label>
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
        <BaseButton type="submit" variant="primary" full-width :loading="isLoading" :disabled="isLoading || form.code.length !== 4" data-testid="verify-button">
          Подтвердить
        </BaseButton>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <p class="auth-recovery">Если код не пришёл — проверьте «Спам»</p>
        <div style="text-align: center; margin-top: 8px;">
          <BaseButton variant="ghost" @click="backToEmail">Назад</BaseButton>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
  padding-top: 40px;
}

.auth-card {
  width: 100%;
  max-width: 440px;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 44px 40px 40px;
}

.auth-title {
  font-family: var(--font-heading);
  font-size: 34px;
  font-weight: 500;
  line-height: 1.1;
  margin-bottom: 40px;
  text-align: center;
  color: var(--color-text);
}

.auth-form {
  display: flex;
  flex-direction: column;
}

.auth-hint {
  font-size: 15px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin-bottom: 24px;
}

.auth-recovery {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.5;
  text-align: center;
  margin-top: 24px;
}

.error-msg {
  color: var(--color-error);
  text-align: center;
  margin-top: 20px;
  font-size: 15px;
  font-weight: 500;
}

.field {
  margin-bottom: 24px;
}

.field label {
  display: block;
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 10px;
  color: var(--color-text-secondary);
}

.input {
  width: 100%;
  height: 52px;
  background: var(--color-surface);
  border: 1px solid var(--color-stroke-subtle);
  border-radius: 14px;
  padding: 0 18px;
  font-family: var(--font-body);
  font-size: 17px;
  color: var(--color-text);
  transition: border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out);
}

.input::placeholder {
  color: var(--color-text-secondary);
}

.input:focus {
  outline: none;
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px var(--color-brand-ring);
}

@media (max-width: 480px) {
  .auth-card {
    padding: 24px;
    border-radius: 24px;
  }
}
</style>
