<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useClubsStore } from '@/stores/clubs'
import { useCategoriesStore } from '@/stores/categories'
import { pluralize, reviewLabel } from '@/utils/plural'
import ClubReviews from '@/components/ClubReviews/ClubReviews.vue'
import BaseButton from '@/components/BaseButton/BaseButton.vue'
import BreadcrumbsNav from '@/components/Breadcrumbs/BreadcrumbsNav.vue'
import type { Crumb } from '@/components/Breadcrumbs/BreadcrumbsNav.vue'
import type { Club } from '@/api/Api'

const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()
const clubsStore = useClubsStore()
const categoriesStore = useCategoriesStore()

const club = ref<Club | null>(null)
const isLoading = ref(false)
const error = ref('')

const breadcrumbTrail = computed<Crumb[]>(() => {
  const trail: Crumb[] = [{ label: 'Клубы', to: '/clubs' }]
  if (club.value) {
    if (club.value.category != null) {
      const path = categoriesStore.pathById(club.value.category)
      path.forEach((c) => {
        trail.push({ label: c.name, to: `/categories/${c.slug}` })
      })
    }
    trail.push({ label: club.value.bookTitle })
  }
  return trail
})

const isMember = computed(() => {
  return club.value ? clubsStore.isCurrentUserMember(club.value) : false
})

const isOwner = computed(() => {
  return club.value ? clubsStore.isCurrentUserOwner(club.value) : false
})

function openTelegram() {
  if (club.value?.telegramChatLink) {
    window.open(club.value.telegramChatLink, '_blank', 'noopener,noreferrer')
  }
}

function openMaxChat() {
  if (club.value?.maxChatLink) {
    window.open(club.value.maxChatLink, '_blank', 'noopener,noreferrer')
  }
}

async function fetchClub() {
  isLoading.value = true
  error.value = ''
  try {
    club.value = await clubsStore.fetchClub(Number(route.params.id))
  } catch {
    error.value = 'Не удалось загрузить информацию о клубе'
  } finally {
    isLoading.value = false
  }
}

async function handleJoin() {
  try {
    await clubsStore.joinClub(Number(route.params.id))
    await fetchClub()
  } catch {
    error.value = 'Не удалось присоединиться к клубу'
  }
}

const isLeaving = ref(false)

async function handleLeave() {
  isLeaving.value = true
  try {
    await clubsStore.leaveClub(Number(route.params.id))
    router.push('/clubs')
  } catch {
    error.value = 'Не удалось покинуть клуб'
    isLeaving.value = false
  }
}

onMounted(async () => {
  await categoriesStore.fetchCategories()
  await fetchClub()
})
</script>

<template>
  <div class="detail-page" data-testid="club-details-page">
    <BreadcrumbsNav v-if="club" :trail="breadcrumbTrail" />

    <div class="detail-card-wrap">
    <div v-if="isLoading" class="skeleton" data-testid="club-details-skeleton">
      <div class="skeleton-card">
        <div class="skeleton-line skeleton-line--title" />
        <div class="skeleton-line skeleton-line--short" />
        <div class="skeleton-line skeleton-line--long" />
        <div class="skeleton-line skeleton-line--long" />
        <div class="skeleton-line skeleton-line--medium" />
      </div>
    </div>

    <div v-else-if="error" class="error-state" data-testid="club-details-error">
      <p class="error-text" data-testid="club-details-error-text">{{ error }}</p>
      <BaseButton variant="outline" testId="club-details-retry-button" @click="fetchClub">Попробовать снова</BaseButton>
    </div>

    <div v-else-if="club" class="detail-card" data-testid="club-details-card">
      <div class="card-head">
        <h1 class="card-title" data-testid="club-details-book-title">{{ club.bookTitle }}</h1>
        <span class="year-badge" data-testid="club-details-publication-year">{{ club.publicationYear }}</span>
      </div>

      <p class="card-author" data-testid="club-details-book-author">{{ club.bookAuthors }}</p>

      <div class="card-divider" />

      <p class="card-desc" data-testid="club-details-description">{{ club.description }}</p>

      <div class="card-stats" data-testid="club-details-stats">
        <span class="stat">
          <span class="stat-num" data-testid="club-details-members-count">{{ club.members.length }}</span>
          {{ pluralize(club.members.length, ['участник', 'участника', 'участников']) }}
        </span>
        <span class="stat-sep">•</span>
        <span class="stat">
          <span class="stat-num" data-testid="club-details-reviews-count">{{ club.reviews?.length || 0 }}</span>
          {{ reviewLabel(club.reviews?.length || 0) }}
        </span>
      </div>

      <div class="card-divider" />

      <div class="card-actions" data-testid="club-details-actions">
        <BaseButton
          v-if="club.telegramChatLink && (isMember || isOwner)"
          variant="brand-outline"
          testId="club-details-telegram-button"
          @click="openTelegram"
        >
          Telegram чат
        </BaseButton>

        <BaseButton
          v-if="club.maxChatLink && (isMember || isOwner)"
          variant="outline"
          testId="club-details-max-chat-button"
          @click="openMaxChat"
        >
          Max чат
        </BaseButton>

        <template v-if="authStore.isAuthenticated">
          <BaseButton
            v-if="!isMember && !isOwner"
            variant="primary"
            testId="club-details-join-button"
            @click="handleJoin"
          >
            Присоединиться
          </BaseButton>

          <BaseButton
            v-if="isMember && !isOwner"
            variant="danger"
            :loading="isLeaving"
            :disabled="isLeaving"
            testId="club-details-leave-button"
            @click="handleLeave"
          >
            Покинуть клуб
          </BaseButton>

          <!-- <BaseButton
            v-if="isOwner"
            variant="outline"
            testId="club-details-edit-button"
            @click="router.push(`/clubs/${club.id}/edit`)"
          >
            Редактировать
          </BaseButton> -->
        </template>
      </div>

      <div class="card-divider" />

      <ClubReviews data-testid="club-details-reviews" :club-id="club.id" :club-members="club.members" :club-owner="club.owner" />
    </div>
    </div>
  </div>
</template>

<style scoped>
.detail-page {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-card-wrap {
  width: 100%;
  max-width: 704px;
  margin: 0 auto;
}

/* === Loader === */

.skeleton {
  display: flex;
  justify-content: center;
}

.skeleton-card {
  width: 100%;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skeleton-line {
  height: 16px;
  border-radius: 8px;
  background: var(--color-stroke-subtle);
  animation: pulse 1.5s ease-in-out infinite;
}

.skeleton-line--title {
  height: 36px;
  width: 60%;
}

.skeleton-line--short {
  width: 40%;
}

.skeleton-line--long {
  width: 100%;
}

.skeleton-line--medium {
  width: 55%;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

/* === Error === */

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 48px 24px;
  text-align: center;
}

.error-text {
  color: var(--color-error);
  font-weight: 500;
}

/* === Card === */

.detail-card {
  background: var(--color-surface);
  border-radius: 32px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  transition: box-shadow var(--duration-normal) var(--ease-out), transform var(--duration-normal) var(--ease-out);
}

.card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.card-title {
  font-family: var(--font-heading);
  font-size: 30px;
  font-weight: 500;
  line-height: 1.1;
  color: var(--color-text);
  margin: 0;
}

.year-badge {
  padding: 4px 10px;
  background: var(--color-bg);
  border: 1px solid var(--color-stroke-subtle);
  border-radius: 30px;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 500;
  line-height: 1.21;
  color: var(--color-text-secondary);
  flex-shrink: 0;
  margin-top: 4px;
}

.card-author {
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 400;
  line-height: 1.21;
  color: var(--color-text-secondary);
  margin: 0;
}

.card-divider {
  height: 1px;
  background: var(--color-stroke-subtle);
}

.card-desc {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 400;
  line-height: 1.6;
  color: var(--color-text-secondary);
  white-space: pre-line;
  margin: 0;
}

.card-stats {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-body);
  font-size: 15px;
  color: var(--color-text-secondary);
}

.stat-num {
  font-weight: 600;
  color: var(--color-text);
}

.stat-sep {
  color: var(--color-text-muted);
}

.card-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

@media (max-width: 768px) {
  .detail-card {
    padding: 24px;
    gap: 16px;
  }

  .card-title {
    font-size: 24px;
  }

  .card-head {
    flex-direction: column;
    gap: 8px;
  }

  .card-actions {
    flex-direction: column;
  }

  .card-desc {
    font-size: 14px;
  }

  .skeleton-card {
    padding: 24px;
  }
}
</style>
