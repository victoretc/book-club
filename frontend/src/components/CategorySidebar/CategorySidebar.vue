<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Category } from '@/api/Api'

defineProps<{
  title: string
  categories: Category[]
  activeId?: number | null
}>()

const router = useRouter()

const openCategory = (slug: string) => {
  router.push(`/categories/${slug}`)
}

const goToAllCategories = () => {
  router.push('/clubs')
}
</script>

<template>
  <aside class="sidebar">
    <h2 class="sidebar-title">{{ title }}</h2>

    <div v-if="categories.length" class="cat-list">
      <button
        v-for="c in categories"
        :key="c.id"
        type="button"
        class="cat-item"
        :class="{ active: activeId === c.id }"
        @click="openCategory(c.slug)"
      >
        <span class="cat-name">{{ c.name }}</span>
        <svg class="cat-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 18l6-6-6-6" />
        </svg>
      </button>
    </div>

    <div v-else class="sidebar-empty">
      {{ activeId != null ? 'Подкатегорий пока нет' : 'Категории появятся позже' }}
    </div>

    <button v-if="activeId != null" type="button" class="sidebar-back" @click="goToAllCategories">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 12H5M11 18l-6-6 6-6" />
      </svg>
      Все категории
    </button>
  </aside>
</template>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: var(--color-surface);
  border-radius: 32px;
  padding: 24px;
  position: sticky;
  top: 96px;
}

.sidebar-title {
  font-family: var(--font-heading);
  font-size: 22px;
  font-weight: 500;
  line-height: 1.2;
  color: var(--color-text);
  padding: 0 4px;
}

.cat-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.cat-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
  padding: 12px 16px;
  border: none;
  border-radius: 16px;
  background: transparent;
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 500;
  line-height: 1.21;
  color: var(--color-text);
  cursor: pointer;
  text-align: left;
  transition: background 0.2s ease, color 0.2s ease;
}

.cat-item:hover {
  background: var(--color-brand-soft);
  color: var(--color-brand);
}

.cat-item.active {
  background: var(--color-brand);
  color: #FFFFFF;
}

.cat-arrow {
  flex-shrink: 0;
  color: var(--color-text-muted);
  transition: color 0.2s ease, transform 0.2s ease;
}

.cat-item:hover .cat-arrow {
  color: var(--color-brand);
  transform: translateX(2px);
}

.cat-item.active .cat-arrow {
  color: rgba(255, 255, 255, 0.85);
}

.sidebar-empty {
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.5;
  color: var(--color-text-secondary);
  padding: 8px 4px;
}

.sidebar-back {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px 16px;
  border: none;
  border-radius: 16px;
  background: var(--color-brand-soft);
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 500;
  color: var(--color-brand);
  cursor: pointer;
  transition: background 0.2s ease;
}

.sidebar-back:hover {
  background: var(--color-brand-ring);
}

@media (max-width: 768px) {
  .sidebar {
    position: static;
    border-radius: 24px;
    padding: 20px;
  }
}
</style>
