<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useForm, Field, ErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/BaseButton.vue'

const props = defineProps({
  clubId: {
    type: Number,
    default: null,
  },
})

const emit = defineEmits(['submit'])
const router = useRouter()
const isLoading = ref(false)
const errorMsg = ref('')

const validationSchema = yup.object({
  bookTitle: yup.string().required('Название книги обязательно'),
  bookAuthors: yup.string().required('Автор(ы) книги обязательно'),
  publicationYear: yup.number().typeError('Введите число').required('Год выпуска обязательно'),
  description: yup.string().required('Описание книги обязательно'),
  telegramChatLink: yup
    .string()
    .required('Ссылка на Telegram чат обязательна')
    .matches(/^https:\/\/t\.me\//, 'Ссылка должна начинаться с https://t.me/'),
})

const { handleSubmit, setValues } = useForm({
  validationSchema,
})

onMounted(async () => {
  if (props.clubId) {
    isLoading.value = true
    try {
      const response = await axios.get(`/api/v1/clubs/${props.clubId}/`)
      const authStore = useAuthStore()
      if (authStore.user && Number(response.data.owner?.id) !== Number(authStore.user.id)) {
        router.push({ name: 'clubs' })
        return
      }
      setValues({
        bookTitle: response.data.bookTitle,
        bookAuthors: response.data.bookAuthors,
        publicationYear: response.data.publicationYear,
        description: response.data.description,
        telegramChatLink: response.data.telegramChatLink,
      })
    } catch {
      router.push({ name: 'clubs' })
    } finally {
      isLoading.value = false
    }
  }
})

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  errorMsg.value = ''
  try {
    if (props.clubId) {
      await axios.put(`/api/v1/clubs/${props.clubId}/`, values)
    } else {
      await axios.post('/api/v1/clubs/', values)
    }
    emit('submit')
    router.push({ name: 'clubs' })
  } catch (err) {
    if (axios.isAxiosError(err) && err.response?.data) {
      errorMsg.value = 'Ошибка при сохранении. Проверьте введенные данные.'
    }
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <form @submit="onSubmit" class="form-card">
    <h1 class="form-title">{{ clubId ? 'Редактирование клуба' : 'Создать клуб' }}</h1>

    <div class="field">
      <label for="bookTitle">Название книги *</label>
      <Field
        id="bookTitle"
        name="bookTitle"
        type="text"
        placeholder="Компьютерные сети"
        :disabled="isLoading"
        class="input"
      />
      <ErrorMessage name="bookTitle" class="field-error" />
    </div>

    <div class="field">
      <label for="bookAuthors">Автор(ы) книги *</label>
      <Field
        id="bookAuthors"
        name="bookAuthors"
        type="text"
        placeholder="Дэвид Уэзеролл и Эндрю Таненбаум"
        :disabled="isLoading"
        class="input"
      />
      <ErrorMessage name="bookAuthors" class="field-error" />
    </div>

    <div class="field">
      <label for="publicationYear">Год выпуска *</label>
      <Field
        id="publicationYear"
        type="number"
        name="publicationYear"
        placeholder="2012"
        :disabled="isLoading"
        class="input"
      />
      <ErrorMessage name="publicationYear" class="field-error" />
    </div>

    <div class="field">
      <label for="description">Описание книги *</label>
      <Field
        id="description"
        name="description"
        as="textarea"
        rows="5"
        placeholder="Описание книги"
        :disabled="isLoading"
        class="textarea"
      />
      <ErrorMessage name="description" class="field-error" />
    </div>

    <div class="field">
      <label for="telegramChatLink">Ссылка на Telegram чат *</label>
      <Field
        id="telegramChatLink"
        name="telegramChatLink"
        placeholder="https://t.me/..."
        :disabled="isLoading"
        class="input"
      />
      <ErrorMessage name="telegramChatLink" class="field-error" />
    </div>

    <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>

    <div class="form-actions">
      <BaseButton type="submit" variant="primary" full-width :loading="isLoading" :disabled="isLoading">
        {{ clubId ? 'Сохранить изменения' : 'Создать клуб' }}
      </BaseButton>
      <BaseButton variant="outline" full-width @click="router.push('/')" :disabled="isLoading">
        Отмена
      </BaseButton>
    </div>
  </form>
</template>

<style scoped>
.form-card {
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 36px 32px 32px;
}

.form-title {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 500;
  line-height: 1.1;
  margin-bottom: 36px;
  text-align: center;
  color: var(--color-text);
}

.field {
  margin-bottom: 20px;
}

.field label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--color-text-secondary);
}

.input,
.textarea {
  width: 100%;
  background: var(--color-surface);
  border: 1px solid var(--color-stroke-subtle);
  border-radius: 12px;
  padding: 12px 16px;
  font-family: var(--font-body);
  font-size: 16px;
  color: var(--color-text);
  transition: border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out);
}

.input {
  height: 48px;
}

.textarea {
  min-height: 120px;
  resize: vertical;
}

.input::placeholder,
.textarea::placeholder {
  color: var(--color-text-secondary);
}

.input:focus,
.textarea:focus {
  outline: none;
  border-color: var(--color-brand);
  box-shadow: 0 0 0 3px var(--color-brand-ring);
}

.input:disabled,
.textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.field-error {
  color: var(--color-error);
  font-size: 14px;
  margin-top: 4px;
  display: block;
}

.error-msg {
  color: var(--color-error);
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 16px;
}

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

@media (max-width: 600px) {
  .form-card {
    padding: 24px;
    border-radius: 24px;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
