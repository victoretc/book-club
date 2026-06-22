<script setup lang="ts">
import { useRoute } from 'vue-router'
import ClubForm from '@/components/ClubForm.vue'

const route = useRoute()
</script>

<template>
  <div class="edit-club">
    <ClubForm :club-id="Number(route.params.id)" />
  </div>
</template>
