<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useReviewsStore } from '@/stores/reviews'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'

const reviewsStore = useReviewsStore()
const router = useRouter()

const currentPage = ref(1)
const pageSize = ref(10)

const totalPages = computed(() => {
  return Math.ceil(reviewsStore.pagination.count / pageSize.value)
})

const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}

const getStars = (assessment: number) => {
  return '★'.repeat(assessment) + '☆'.repeat(5 - assessment)
}

const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    reviewsStore.fetchReviews(page, pageSize.value)
  }
}

const goToClub = (clubId: number) => {
  router.push(`/clubs/${clubId}`)
}

onMounted(() => {
  reviewsStore.fetchReviews(currentPage.value, pageSize.value)
})
</script>

<template>
  <div class="reviews-page">
    <h1>Все отзывы</h1>

    <div v-if="reviewsStore.isLoading" class="loading">Загрузка отзывов...</div>

    <div v-else-if="reviewsStore.error" class="error">
      {{ reviewsStore.error }}
    </div>

    <div v-else-if="reviewsStore.reviews.length === 0" class="no-reviews">
      <p>Пока нет отзывов</p>
    </div>

    <div v-else class="reviews-list">
      <div
        v-for="review in reviewsStore.reviews"
        :key="review.id"
        class="review-card"
        @click="goToClub(review.club)"
      >
        <div class="review-header">
          <div class="reviewer-info">
            <span class="reviewer-avatar">
              {{ review.username?.[0] || '?' }}
            </span>
            <div class="reviewer-details">
              <span class="reviewer-name">{{ review.username || 'Пользователь' }}</span>
              <span class="club-id">Клуб #{{ review.club }}</span>
            </div>
          </div>
          <div class="review-rating">
            <span class="stars">{{ getStars(review.assessment) }}</span>
            <span class="read-pages">{{ review.readPages }} стр.</span>
          </div>
        </div>

        <div class="review-content">
          <p>{{ review.review }}</p>
        </div>

        <div class="review-footer">
          <span class="review-date">
            {{ formatDate(review.created) }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="reviewsStore.pagination.count > pageSize" class="pagination">
      <BaseButton
        variant="outline"
        :disabled="!reviewsStore.pagination.previous"
        @click="goToPage(currentPage - 1)"
      >
        ← Назад
      </BaseButton>

      <span class="page-info"> Страница {{ currentPage }} из {{ totalPages }} </span>

      <BaseButton
        variant="outline"
        :disabled="!reviewsStore.pagination.next"
        @click="goToPage(currentPage + 1)"
      >
        Вперед →
      </BaseButton>
    </div>
  </div>
</template>

<style scoped>
.reviews-page {
  width: 100%;
  max-width: 704px;
  margin: 0 auto;
}

.reviews-page h1 {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 500;
  margin-bottom: 28px;
  text-align: center;
  color: var(--color-text);
}

.loading,
.error,
.no-reviews {
  text-align: center;
  padding: 48px;
  background: var(--color-surface);
  border-radius: 32px;
}

.error {
  color: var(--color-error);
  font-weight: 500;
}

.no-reviews {
  color: var(--color-text-secondary);
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.review-card {
  background: var(--color-surface);
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: box-shadow var(--duration-normal) var(--ease-out), transform var(--duration-normal) var(--ease-out);
}

.review-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 16px;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.reviewer-avatar {
  width: 48px;
  height: 48px;
  background: var(--color-brand);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 500;
  color: #FFFFFF;
  text-transform: uppercase;
}

.reviewer-details {
  display: flex;
  flex-direction: column;
}

.reviewer-name {
  font-weight: 500;
  font-size: 16px;
  color: var(--color-text);
}

.club-id {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.review-rating {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stars {
  color: var(--color-brand);
  font-size: 18px;
  letter-spacing: 2px;
}

.read-pages {
  background: var(--color-bg);
  border-radius: 30px;
  padding: 4px 12px;
  font-size: 14px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.review-content {
  margin-bottom: 16px;
  line-height: 1.6;
  white-space: pre-line;
  color: var(--color-text-secondary);
}

.review-footer {
  display: flex;
  justify-content: flex-end;
}

.review-date {
  color: var(--color-text-secondary);
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
}

.page-info {
  font-size: 16px;
  color: var(--color-text);
}

@media (max-width: 768px) {
  .review-card {
    padding: 20px;
  }

  .review-header {
    flex-direction: column;
  }

  .review-rating {
    width: 100%;
    justify-content: space-between;
  }

  .pagination {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .review-card {
    padding: 16px;
  }

  .reviewer-avatar {
    width: 40px;
    height: 40px;
    font-size: 16px;
  }
}
</style>
