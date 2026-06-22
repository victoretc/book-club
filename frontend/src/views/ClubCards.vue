<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useClubsStore } from '@/stores/clubs'
import { useAuthStore } from '@/stores/auth'
import ClubFilters from '@/components/ClubFilters.vue'
import PaginationControls from '@/components/PaginationControls.vue'
import { memberReadingText } from '@/utils/plural'
import type { Club } from '@/types/clubs'
import type { User } from '@/types/users'

const clubsStore = useClubsStore()
if (clubsStore.clubs.length === 0) {
  clubsStore.isLoading = true
}
const authStore = useAuthStore()
const router = useRouter()

const renderKey = ref(0)

watch(() => clubsStore.clubs, () => {
  renderKey.value++
}, { deep: true })

onMounted(async () => {
  await clubsStore.fetchClubs()

  if (authStore.isAuthenticated && authStore.pendingClubJoin) {
    const clubId = authStore.pendingClubJoin
    try {
      await clubsStore.joinClub(clubId)
      router.push(`/clubs/${clubId}`)
    } catch {
      console.error('Ошибка при присоединении')
    } finally {
      authStore.clearPendingClubJoin()
    }
  }
})

const isMember = (club: Club) => {
  return authStore.user ? club.members.some(m => m.id === authStore.user!.id) : false
}

const joinClub = async (clubId: number) => {
  if (!authStore.isAuthenticated) {
    authStore.setPendingClubJoin(clubId)
    router.push('/signin')
    return
  }

  try {
    await clubsStore.joinClub(clubId)
    router.push(`/clubs/${clubId}`)
  } catch {
    console.error('Ошибка при присоединении')
  }
}

const openClubPage = (clubId: number) => {
  router.push(`/clubs/${clubId}`)
}

const avatarColors = ['#F1FFD6', '#A0EC06', '#42CF71', '#FFE4B5', '#DDA0DD', '#87CEEB']

const getInitials = (m: User): string => {
  if (m.firstName && m.lastName) return (m.firstName[0] + m.lastName[0]).toUpperCase()
  if (m.firstName) return m.firstName[0].toUpperCase()
  if (m.lastName) return m.lastName[0].toUpperCase()
  if (m.email) return m.email[0].toUpperCase()
  if (m.username) return m.username[0].toUpperCase()
  return '?'
}

const memberInitials = (club: Club) => {
  return club.members.slice(0, 3).map((m, i) => ({
    initials: getInitials(m),
    color: avatarColors[i % avatarColors.length],
  }))
}
</script>

<template>
  <div class="clubs-page">
    <ClubFilters />

    <div v-if="clubsStore.error" class="error">{{ clubsStore.error }}</div>

    <Transition name="fade-slide" mode="out-in">
      <div v-if="clubsStore.isLoading" key="loading" class="clubs-list clubs-loading">
        <div v-for="n in 3" :key="n" class="skeleton-card">
          <div class="skeleton-heading">
            <div class="skeleton-line skeleton-title" />
            <div class="skeleton-line skeleton-badge" />
          </div>
          <div class="skeleton-line skeleton-author" />
          <div class="skeleton-line skeleton-desc" />
          <div class="skeleton-line skeleton-desc skeleton-desc--short" />
          <div class="skeleton-footer">
            <div class="skeleton-line skeleton-members" />
            <div class="skeleton-line skeleton-arrow" />
          </div>
        </div>
      </div>
      <div v-else-if="clubsStore.clubs.length === 0" key="empty" class="no-results">
        <img src="@/assets/images/not-found.png" alt="Ничего не найдено" class="not-found-img" />
      </div>
      <div v-else :key="'list-' + renderKey" class="clubs-list">
        <div
          v-for="club in clubsStore.clubs"
          :key="club.id"
          class="club-card"
          @click="openClubPage(club.id)"
        >
          <div class="card-header">
            <h3 class="card-title">{{ club.bookTitle }}</h3>
            <span class="year-badge">{{ club.publicationYear }}</span>
          </div>

          <div class="card-author">{{ club.bookAuthors }}</div>

          <p class="card-desc">{{ club.description }}</p>

          <div class="card-footer">
            <div class="card-members">
              <div class="member-avatars">
                <span
                  v-for="(item, i) in memberInitials(club)"
                  :key="i"
                  class="member-avatar"
                  :style="{ backgroundColor: item.color }"
                >
                  {{ item.initials }}
                </span>
                <span v-if="isMember(club)" class="you-badge">вы</span>
              </div>
              <span class="member-count">{{ memberReadingText(club.members.length, isMember(club)) }}</span>
            </div>

            <span class="card-arrow" aria-hidden="true">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14M13 5l7 7-7 7"/>
              </svg>
            </span>
          </div>
        </div>
      </div>
    </Transition>

    <PaginationControls v-if="clubsStore.clubs.length > 0 && !clubsStore.isLoading" class="pagination-wrap" />
  </div>
</template>

<style scoped>
.clubs-page {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.clubs-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
}

.pagination-wrap {
  margin-top: auto;
}

.club-card {
  width: 704px;
  max-width: 100%;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 28px;
  cursor: pointer;
  transition: box-shadow var(--duration-normal) var(--ease-out), transform var(--duration-normal) var(--ease-out);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.club-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.card-title {
  font-family: var(--font-heading);
  font-size: 30px;
  font-weight: 500;
  line-height: 1.1;
  color: var(--color-text);
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
}

.card-author {
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 400;
  line-height: 1.21;
  color: var(--color-text-secondary);
}

.card-desc {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 400;
  line-height: 1.6;
  color: var(--color-text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--color-stroke-subtle);
}

.card-members {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.member-avatars {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.member-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 700;
  color: #1A1A1A;
  border: 2px solid var(--color-surface);
  margin-left: -8px;
  flex-shrink: 0;
}

.member-avatar:first-child {
  margin-left: 0;
}

.you-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-brand);
  border: 2px solid var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-body);
  font-size: 11px;
  font-weight: 700;
  color: #FFFFFF;
  margin-left: -8px;
  flex-shrink: 0;
}

.member-count {
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 400;
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-arrow {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
}

.error {
  color: var(--color-error);
  font-weight: 500;
  padding: 32px;
  text-align: center;
}

.no-results {
  display: flex;
  justify-content: center;
  width: 704px;
  max-width: 100%;
}

.clubs-loading {
  gap: 16px;
}

.skeleton-card {
  width: 704px;
  max-width: 100%;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.skeleton-line {
  height: 16px;
  border-radius: 8px;
  background: var(--color-stroke-subtle);
  position: relative;
  overflow: hidden;
}

.skeleton-line::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  animation: skeleton-shimmer 1.6s ease-in-out infinite;
}

.skeleton-title {
  flex: 1;
  height: 32px;
}

.skeleton-badge {
  width: 60px;
  height: 28px;
  flex-shrink: 0;
}

.skeleton-author {
  width: 40%;
  height: 18px;
}

.skeleton-desc {
  width: 100%;
}

.skeleton-desc--short {
  width: 65%;
}

.skeleton-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid var(--color-stroke-subtle);
}

.skeleton-members {
  width: 120px;
  height: 32px;
}

.skeleton-arrow {
  width: 18px;
  height: 18px;
}

@keyframes skeleton-shimmer {
  0% { translate: -100%; }
  100% { translate: 100%; }
}

.not-found-img {
  height: auto;
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

@media (max-width: 768px) {
  .club-card {
    width: 100%;
    padding: 20px;
    gap: 10px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .card-title {
    font-size: 24px;
  }

  .card-author {
    font-size: 14px;
  }

  .card-desc {
    font-size: 14px;
  }

  .card-footer {
    gap: 12px;
  }

  .member-count {
    font-size: 13px;
  }

  .not-found-img {
    max-width: 100%;
    height: auto;
  }

  .no-results {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .card-footer {
    flex-direction: column;
    align-items: stretch;
  }

  .card-members {
    justify-content: center;
  }

}
</style>
