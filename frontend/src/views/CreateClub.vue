<script setup lang="ts">
import { onMounted, ref, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import ClubForm from '@/components/ClubForm/ClubForm.vue'
import ClubFormInstruction from '@/components/ClubFormInstruction/ClubFormInstruction.vue'
import BreadcrumbsNav from '@/components/Breadcrumbs/BreadcrumbsNav.vue'
import { useClubsStore } from '@/stores/clubs'
import heroImg from '@/assets/images/eugene-golovesov-zUuJz_idfqM-unsplash.jpg'

const router = useRouter()
const clubsStore = useClubsStore()
const showInstruction = ref(false)
const isMobile = ref(false)

const breadcrumbs = [
  { label: 'Клубы', to: '/clubs' },
  { label: 'Создать клуб' },
]

function checkMobile() {
  isMobile.value = window.innerWidth <= 768
}

onMounted(async () => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
  try {
    const count = await clubsStore.ownedClubsCount()
    showInstruction.value = count === 0 && isMobile.value
  } catch {
    showInstruction.value = false
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<template>
  <div class="create-page" data-testid="create-club-page">
    <BreadcrumbsNav :trail="breadcrumbs" />

    <div class="create-split">
      <div class="create-left">
        <div class="create-left-img" :style="{ backgroundImage: `url(${heroImg})` }">
          <div class="create-left-overlay" />
          <div class="create-left-content">
            <h2 class="create-left-title">Как создать клуб</h2>
            <p class="create-left-desc">
              На странице клубов — все доступные клубы. Хочешь найти участников для книги,
              которой ещё нет в Читальной? Отправь запрос на создание клуба.
            </p>
            <p class="create-left-desc">
              Заполни форму: <strong>Название книги</strong>, <strong>Автор(ы) книги</strong>,
              <strong>Год выпуска</strong> и <strong>Описание книги</strong>. Выбери <strong>Категорию</strong>,
              при необходимости — <strong>Подкатегорию</strong>. Нажми «Создать клуб».
            </p>
            <p class="create-left-desc">
              Администратор увидит заявку и создаст чаты в Max и Telegram. Когда всё будет готово,
              клуб появится на главной странице, а тебе на почту придёт письмо.
            </p>
          </div>
        </div>
      </div>

      <div class="create-right">
        <div class="create-right-inner">
          <ClubForm />
        </div>
      </div>
    </div>

    <ClubFormInstruction :open="showInstruction" @close="showInstruction = false" />
  </div>
</template>

<style scoped>
.create-page {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.create-split {
  display: flex;
  width: 100%;
  gap: 32px;
  align-items: flex-start;
}

.create-left {
  flex: 1;
  min-width: 0;
}

.create-left-img {
  position: relative;
  width: 100%;
  min-height: 480px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 32px;
  overflow: hidden;
  display: flex;
  align-items: flex-end;
}

.create-left-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.05) 0%, rgba(0, 0, 0, 0.65) 100%);
}

.create-left-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 32px;
  color: #fff;
}

.create-left-title {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 500;
  line-height: 1.15;
  color: #fff;
  margin: 0;
}

.create-left-desc {
  font-family: var(--font-body);
  font-size: 14px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
}

.create-left-desc strong {
  color: #fff;
  font-weight: 600;
}

.create-right {
  flex: 1;
  min-width: 0;
}

.create-right-inner {
  width: 100%;
  max-width: 520px;
}

:deep(.form-card) {
  background: transparent;
  border-radius: 0;
  padding: 0;
  box-shadow: none;
  border: none;
}

:deep(.form-title) {
  text-align: left;
  font-size: 24px;
  margin-bottom: 28px;
}

:deep(.type-picker) {
  background: transparent;
  border: none;
  box-shadow: none;
}

:deep(.type-picker__content) {
  align-items: flex-start;
  text-align: left;
  padding: 0;
}

:deep(.type-picker__title) {
  font-size: 24px;
}

@media (max-width: 768px) {
  .create-left {
    display: none;
  }

  .create-split {
    flex-direction: column;
  }

  .create-right {
    width: 100%;
  }
}
</style>
