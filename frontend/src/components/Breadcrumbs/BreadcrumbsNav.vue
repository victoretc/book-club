<script setup lang="ts">
export interface Crumb {
  label: string
  to?: string
}

defineProps<{
  trail: Crumb[]
  trailingSlash?: boolean
}>()
</script>

<template>
  <nav class="breadcrumbs-nav" aria-label="Хлебные крошки">
    <div class="breadcrumbs-nav__trail">
      <template v-for="(crumb, i) in trail" :key="`${i}-${crumb.label}`">
        <router-link v-if="crumb.to" :to="crumb.to" class="crumb crumb--link">
          {{ crumb.label }}
        </router-link>
        <span v-else class="crumb" :class="{ 'crumb--current': i === trail.length - 1 }">
          {{ crumb.label }}
        </span>
        <span v-if="i < trail.length - 1 || trailingSlash" class="crumb-sep">/</span>
      </template>
    </div>

    <slot name="actions" />
  </nav>
</template>

<style scoped>
.breadcrumbs-nav {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px 16px;
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.3;
}

.breadcrumbs-nav__trail {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.crumb {
  color: var(--color-text-secondary);
  text-decoration: none;
  padding: 4px 8px;
  border-radius: 8px;
  transition: color 0.2s ease, background 0.2s ease;
}

.crumb--link:hover {
  color: var(--color-text);
  background: var(--color-bg);
}

.crumb--current {
  color: var(--color-text-secondary);
  font-weight: 500;
}

.crumb-sep {
  color: var(--color-text-muted);
}
</style>
