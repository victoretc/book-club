<script setup lang="ts">
import { onMounted, computed, ref, watch, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useClubsStore } from '@/stores/clubs'
import { useCategoriesStore } from '@/stores/categories'
import type { Club, Member } from '@/api/Api'
import ClubFilters from '@/components/ClubFilters/ClubFilters.vue'
import CategorySidebar from '@/components/CategorySidebar/CategorySidebar.vue'
import PaginationControls from '@/components/PaginationControls/PaginationControls.vue'
import BreadcrumbsNav from '@/components/Breadcrumbs/BreadcrumbsNav.vue'
import type { Crumb } from '@/components/Breadcrumbs/BreadcrumbsNav.vue'
import { useClubsView } from '@/composables/useClubsView'
import { memberReadingText } from '@/utils/plural'

const clubsStore = useClubsStore()
if (clubsStore.clubs.length === 0) {
  clubsStore.isLoading = true
}
const categoriesStore = useCategoriesStore()
const router = useRouter()
const route = useRoute()
const { viewMode } = useClubsView()

const currentSlug = computed(() => String(route.params.slug ?? ''))
const currentCategory = computed(() => categoriesStore.categoryBySlug(currentSlug.value))
const sidebarCategories = computed(() => {
  if (currentCategory.value) {
    return categoriesStore.childrenOf(currentCategory.value.id)
  }
  return categoriesStore.topLevelCategories
})
const sidebarTitle = computed(() => (currentCategory.value ? 'Подкатегории' : 'Категории'))
const breadcrumbTrail = computed<Crumb[]>(() => {
  const trail: Crumb[] = [{ label: 'Клубы', to: '/clubs' }]
  if (currentCategory.value) {
    const path = categoriesStore.pathById(currentCategory.value.id)
    path.forEach((c, i) => {
      trail.push({
        label: c.name,
        to: i < path.length - 1 ? `/categories/${c.slug}` : undefined,
      })
    })
  }
  return trail
})

onMounted(async () => {
  await categoriesStore.fetchCategories()
  await loadClubsByRoute()
})

watch(currentSlug, async () => {
  await categoriesStore.fetchCategories()
  await loadClubsByRoute()
})

const showScrollTop = ref(false)

function onScroll() {
  showScrollTop.value = window.scrollY > window.innerHeight * 0.6
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  onScroll()
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', onScroll)
})

const loadClubsByRoute = async () => {
  if (currentCategory.value) {
    await clubsStore.filterByCategory(currentCategory.value.id)
  } else {
    if (clubsStore.activeFilter && clubsStore.activeFilter !== 'all') {
      clubsStore.activeCategory = null
      await clubsStore.filterByMembership(clubsStore.activeFilter)
    } else {
      await clubsStore.fetchClubs()
    }
  }
}

const goBackToCategories = () => {
  router.push('/clubs')
}

const openCategory = (slug: string) => {
  router.push(`/categories/${slug}`)
}

const isMember = (club: Club) => clubsStore.isCurrentUserMember(club)

const openClubPage = (clubId: number) => {
  router.push(`/clubs/${clubId}`)
}

const avatarColors = ['#F1FFD6', '#A0EC06', '#42CF71', '#FFE4B5', '#DDA0DD', '#87CEEB']

const getInitials = (m: Member): string => {
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
    <BreadcrumbsNav :trail="breadcrumbTrail" :trailing-slash="!currentCategory">
      <template #actions>
        <button v-if="currentCategory" type="button" class="crumb-back" @click="goBackToCategories">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5M11 18l-6-6 6-6" />
          </svg>
          Назад к категориям
        </button>
      </template>
    </BreadcrumbsNav>

    <ClubFilters />

    <nav class="category-chips" aria-label="Категории">
      <button
        v-if="currentCategory"
        type="button"
        class="chip chip--all"
        :class="{ 'chip--active': !currentCategory }"
        @click="goBackToCategories"
      >
        Все категории
      </button>
      <button
        v-for="c in sidebarCategories"
        :key="c.id"
        type="button"
        class="chip"
        :class="{ 'chip--active': currentCategory?.id === c.id }"
        @click="openCategory(c.slug)"
      >
        {{ c.name }}
      </button>
    </nav>

    <div class="content-grid">
      <div class="clubs-column">
        <Transition name="fade-slide" mode="out-in">
          <div v-if="clubsStore.isLoading" key="loading" class="clubs-list clubs-loading" :class="`clubs-list--${viewMode}`">
            <div v-for="n in 3" :key="n" class="skeleton-card" :class="`skeleton-card--${viewMode}`">
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
          <div v-else class="clubs-list" :class="`clubs-list--${viewMode}`">
            <div
              v-for="club in clubsStore.clubs"
              :key="club.id"
              class="club-card"
              :class="`club-card--${viewMode}`"
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

        <PaginationControls
          v-if="clubsStore.clubs.length >= 5 && !clubsStore.isLoading"
          class="pagination-wrap"
          :current-page="clubsStore.pagination.currentPage"
          :total-pages="clubsStore.totalPages"
          :page-size="clubsStore.pagination.pageSize"
          @page-change="clubsStore.goToPage"
          @page-size-change="clubsStore.changePageSize"
        />
      </div>

      <CategorySidebar
        class="category-sidebar"
        :title="sidebarTitle"
        :categories="sidebarCategories"
        :active-id="currentCategory?.id"
      />
    </div>

    <Transition name="scroll-top">
      <button
        v-if="showScrollTop"
        type="button"
        class="scroll-top"
        aria-label="Наверх"
        data-testid="scroll-top-button"
        @click="scrollToTop"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 19V5M5 12l7-7 7 7" />
        </svg>
      </button>
    </Transition>
  </div>
</template>

<style scoped>
.clubs-page {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
}

.crumb-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border: none;
  border-radius: 8px;
  background: transparent;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 400;
  line-height: 1.3;
  color: var(--color-text-secondary);
  cursor: pointer;
  white-space: nowrap;
}

.crumb-back svg {
  flex-shrink: 0;
}

.category-chips {
  display: none;
}

.category-sidebar {
  display: block;
}

.chip {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  background: var(--color-surface);
  border: 1px solid var(--color-stroke-subtle);
  border-radius: 9999px;
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 500;
  line-height: 1.21;
  color: var(--color-text);
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.chip:not(.chip--active):hover {
  background: var(--color-brand-soft);
  color: var(--color-brand);
  border-color: var(--color-brand-ring);
}

.chip--active {
  background: var(--color-brand);
  border-color: var(--color-brand);
  color: #FFFFFF;
}

.chip--all {
  border-style: dashed;
  border-color: var(--color-brand-ring);
  color: var(--color-brand);
  background: var(--color-brand-soft);
}

.chip--all.chip--active {
  border-style: solid;
}

.content-grid {
  width: 100%;
  display: grid;
  grid-template-columns: minmax(0, 704px) 300px;
  justify-content: center;
  gap: 24px 16px;
  align-items: start;
}

.clubs-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  min-width: 0;
}

.clubs-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  width: 100%;
}

@media (min-width: 768px) {
  .clubs-list--grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    align-items: start;
  }

  .clubs-list--grid .club-card,
  .clubs-list--grid .skeleton-card {
    max-width: none;
  }
}

.pagination-wrap {
  width: 100%;
}

.club-card {
  width: 100%;
  max-width: 704px;
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

@media (min-width: 768px) {
  .club-card--grid {
    aspect-ratio: 4 / 3;
    height: 100%;
    border-radius: 24px;
    padding: 20px;
    gap: 8px;
    overflow: hidden;
  }

  .club-card--grid .card-title {
    font-size: 22px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .club-card--grid .card-author {
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .club-card--grid .card-desc {
    font-size: 14px;
    line-height: 1.55;
    -webkit-line-clamp: 2;
  }

  .club-card--grid .card-footer {
    margin-top: auto;
    padding-top: 12px;
    gap: 8px;
  }

  .club-card--grid .year-badge {
    font-size: 12px;
    padding: 3px 8px;
  }

  .club-card--grid .member-avatar,
  .club-card--grid .you-badge {
    width: 28px;
    height: 28px;
    font-size: 10px;
  }

  .club-card--grid .member-count {
    font-size: 13px;
  }
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
  word-break: break-word;
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

.no-results {
  display: flex;
  justify-content: center;
  width: 100%;
}

.clubs-loading {
  gap: 16px;
}

.skeleton-card {
  width: 100%;
  max-width: 704px;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (min-width: 768px) {
  .skeleton-card--grid {
    aspect-ratio: 4 / 3;
    height: 100%;
    border-radius: 24px;
    padding: 20px;
    gap: 8px;
    overflow: hidden;
  }
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
  max-width: 100%;
  height: auto;
  width: 360px;
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

@media (max-width: 900px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .clubs-column {
    order: 1;
  }
}

@media (max-width: 768px) {
  .clubs-page {
    gap: 16px;
  }

  .category-chips {
    display: flex;
    align-items: center;
    gap: 8px;
    width: 100%;
    overflow-x: auto;
    scrollbar-width: none;
    padding: 2px 2px 6px;
    -webkit-overflow-scrolling: touch;
  }

  .category-chips::-webkit-scrollbar {
    display: none;
  }

  .category-sidebar {
    display: none;
  }

  .club-card {
    width: 100%;
    padding: 20px;
    gap: 10px;
  }

  .card-header {
    gap: 10px;
  }

  .card-title {
    font-size: 24px;
    flex: 1;
  }

  .card-author {
    font-size: 14px;
  }

  .card-desc {
    font-size: 14px;
  }

  .card-footer {
    gap: 12px;
    padding-top: 12px;
  }

  .member-count {
    font-size: 13px;
  }

  .not-found-img {
    max-width: 100%;
    width: 240px;
    height: auto;
  }

  .no-results {
    width: 100%;
  }
}

@media (hover: none) {
  .club-card:hover {
    box-shadow: none;
    transform: none;
  }
}

@media (max-width: 480px) {
  .clubs-page {
    gap: 12px;
  }

  .clubs-list {
    gap: 12px;
  }

  .clubs-column {
    gap: 16px;
  }

  .club-card {
    padding: 16px;
    gap: 8px;
  }

  .card-header {
    gap: 8px;
  }

  .card-title {
    font-size: 20px;
    flex: 1;
  }

  .year-badge {
    font-size: 12px;
    padding: 3px 8px;
  }

  .card-author {
    font-size: 13px;
  }

  .card-desc {
    font-size: 13px;
    line-height: 1.5;
    -webkit-line-clamp: 2;
  }

  .card-footer {
    gap: 8px;
    padding-top: 10px;
  }

  .card-members {
    gap: 8px;
  }

  .member-avatar,
  .you-badge {
    width: 28px;
    height: 28px;
    font-size: 10px;
    border-width: 1.5px;
    margin-left: -6px;
  }

  .member-count {
    font-size: 12px;
  }

  .card-arrow svg {
    width: 16px;
    height: 16px;
  }

  .skeleton-card {
    padding: 16px;
    gap: 8px;
  }

  .skeleton-heading {
    gap: 8px;
  }

  .skeleton-title {
    height: 24px;
  }

  .skeleton-badge {
    width: 48px;
    height: 22px;
  }

  .skeleton-author {
    height: 15px;
  }

  .skeleton-desc {
    height: 14px;
  }

  .skeleton-footer {
    padding-top: 10px;
  }

  .skeleton-members {
    width: 100px;
    height: 28px;
  }
}

.scroll-top {
  position: fixed;
  right: 24px;
  bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border: none;
  border-radius: 50%;
  background: var(--color-brand);
  color: #FFFFFF;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(59, 62, 255, 0.35);
  z-index: 40;
  transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}

.scroll-top:hover {
  background: var(--color-brand);
  filter: brightness(1.08);
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(59, 62, 255, 0.4);
}

.scroll-top:active {
  transform: translateY(0);
}

.scroll-top-enter-active,
.scroll-top-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.scroll-top-enter-from,
.scroll-top-leave-to {
  opacity: 0;
  transform: translateY(12px);
}

@media (max-width: 480px) {
  .scroll-top {
    right: 16px;
    bottom: 16px;
    width: 48px;
    height: 48px;
  }
}
</style>
