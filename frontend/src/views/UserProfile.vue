<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'

const authStore = useAuthStore()
const router = useRouter()

const userInitials = computed(() => {
  const u = authStore.user
  if (!u) return '?'
  if (u.firstName && u.lastName) return (u.firstName[0] + u.lastName[0]).toUpperCase()
  if (u.firstName) return u.firstName[0].toUpperCase()
  if (u.lastName) return u.lastName[0].toUpperCase()
  if (u.email) return u.email[0].toUpperCase()
  if (u.username) return u.username[0].toUpperCase()
  return '?'
})

const isEditing = ref(false)
const isLoading = ref(false)
const error = ref('')
const success = ref('')

const editForm = ref({
  username: '',
  firstName: '',
  lastName: '',
  email: '',
})

onMounted(() => {
  if (authStore.user) {
    editForm.value = {
      username: authStore.user.username || '',
      firstName: authStore.user.firstName || '',
      lastName: authStore.user.lastName || '',
      email: authStore.user.email || '',
    }
  }
})

const handleLogout = async () => {
  await authStore.logout()
  router.push('/signin')
}

const startEditing = () => {
  isEditing.value = true
  error.value = ''
  success.value = ''
}

const cancelEditing = () => {
  isEditing.value = false
  error.value = ''
  success.value = ''

  if (authStore.user) {
    editForm.value = {
      username: authStore.user.username || '',
      firstName: authStore.user.firstName || '',
      lastName: authStore.user.lastName || '',
      email: authStore.user.email || '',
    }
  }
}

const updateProfile = async () => {
  isLoading.value = true
  error.value = ''
  success.value = ''

  try {
    const updatedData: Record<string, string> = {}

    if (editForm.value.username !== authStore.user?.username) {
      updatedData.username = editForm.value.username
    }
    if (editForm.value.firstName !== authStore.user?.firstName) {
      updatedData.first_name = editForm.value.firstName
    }
    if (editForm.value.lastName !== authStore.user?.lastName) {
      updatedData.last_name = editForm.value.lastName
    }
    if (editForm.value.email !== authStore.user?.email) {
      updatedData.email = editForm.value.email
    }

    if (Object.keys(updatedData).length > 0) {
      await authStore.updateUser(updatedData)
      success.value = 'Профиль успешно обновлен'
    } else {
      success.value = 'Нет изменений для сохранения'
    }

    isEditing.value = false
  } catch (err: unknown) {
    const apiError = err as {
      response?: {
        data?: {
          username?: string[]
          email?: string[]
        }
      }
    }
    const errors = apiError.response?.data

    if (errors?.username) {
      error.value = `Логин: ${errors.username.join(', ')}`
    } else if (errors?.email) {
      error.value = `Email: ${errors.email.join(', ')}`
    } else {
      error.value = 'Ошибка при обновлении профиля'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="profile-page">
    <div v-if="authStore.user" class="profile-card">
      <div v-if="!isEditing" class="profile-view">
        <div class="profile-avatar">
          {{ userInitials }}
        </div>

        <div class="profile-fields">
          <div class="profile-field">
            <span class="field-label">Логин</span>
            <span class="field-value">{{ authStore.user.username }}</span>
          </div>
          <div v-if="authStore.user.firstName" class="profile-field">
            <span class="field-label">Имя</span>
            <span class="field-value">{{ authStore.user.firstName }}</span>
          </div>
          <div v-if="authStore.user.lastName" class="profile-field">
            <span class="field-label">Фамилия</span>
            <span class="field-value">{{ authStore.user.lastName }}</span>
          </div>
          <div v-if="authStore.user.email" class="profile-field">
            <span class="field-label">Email</span>
            <span class="field-value">{{ authStore.user.email }}</span>
          </div>
        </div>

        <div class="profile-actions">
          <BaseButton variant="primary" full-width @click="startEditing">Редактировать</BaseButton>
          <BaseButton variant="danger" full-width @click="handleLogout">Выйти</BaseButton>
        </div>
      </div>

      <div v-else class="profile-edit">
        <h2 class="edit-title">Редактирование профиля</h2>
        <form @submit.prevent="updateProfile" class="edit-form">
          <div class="field">
            <label for="username">Логин</label>
            <input v-model="editForm.username" type="text" id="username" required placeholder="Логин" class="input" />
          </div>
          <div class="field">
            <label for="firstName">Имя</label>
            <input v-model="editForm.firstName" type="text" id="firstName" placeholder="Имя" class="input" />
          </div>
          <div class="field">
            <label for="lastName">Фамилия</label>
            <input v-model="editForm.lastName" type="text" id="lastName" placeholder="Фамилия" class="input" />
          </div>
          <div class="field">
            <label for="email">Email</label>
            <input v-model="editForm.email" type="email" id="email" placeholder="Email" class="input" />
          </div>

          <div v-if="error" class="msg msg--error">{{ error }}</div>
          <div v-if="success" class="msg msg--success">{{ success }}</div>

          <div class="form-actions">
            <BaseButton type="submit" variant="primary" full-width :loading="isLoading" :disabled="isLoading">
              Сохранить
            </BaseButton>
            <BaseButton variant="outline" full-width @click="cancelEditing" :disabled="isLoading">
              Отмена
            </BaseButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
}

.profile-card {
  background: var(--color-surface);
  border-radius: 32px;
  padding: 36px 32px 32px;
}

.profile-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 36px;
}

.profile-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-size: 52px;
  font-weight: 400;
  text-transform: uppercase;
  line-height: 1;
  letter-spacing: 0.12em;
  text-indent: 0.12em;
  color: var(--color-brand);
}

.profile-fields {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.profile-field {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-stroke-subtle);
}

.profile-field:last-child {
  border-bottom: none;
}

.field-label {
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.field-value {
  font-size: 16px;
  font-weight: 500;
  text-align: right;
  word-break: break-word;
  color: var(--color-text);
}

.profile-actions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.profile-edit {
  width: 100%;
}

.edit-title {
  font-family: var(--font-heading);
  font-size: 24px;
  font-weight: 500;
  margin-bottom: 24px;
  text-align: center;
  color: var(--color-text);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.field {
  width: 100%;
}

.field label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--color-text-secondary);
}

.input {
  width: 100%;
  height: 48px;
  background: var(--color-surface);
  border: 1px solid var(--color-stroke-subtle);
  border-radius: 12px;
  padding: 0 16px;
  font-family: var(--font-body);
  font-size: 16px;
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

.msg {
  text-align: center;
  font-size: 14px;
  font-weight: 500;
}

.msg--error {
  color: var(--color-error);
}

.msg--success {
  color: var(--color-success);
}

.form-actions {
  display: flex;
  gap: 12px;
}

@media (max-width: 600px) {
  .profile-card {
    padding: 24px;
  }

  .profile-avatar {
    font-size: 40px;
    letter-spacing: 0.1em;
    text-indent: 0.1em;
  }

  .profile-field {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .field-value {
    text-align: left;
  }

  .form-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .form-actions {
    flex-direction: column;
  }
}
</style>
