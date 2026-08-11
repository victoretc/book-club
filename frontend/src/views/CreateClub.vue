<script setup lang="ts">
import { onMounted, ref } from 'vue'
import ClubForm from '@/components/ClubForm/ClubForm.vue'
import ClubFormInstruction from '@/components/ClubFormInstruction/ClubFormInstruction.vue'
import { useClubsStore } from '@/stores/clubs'

const clubsStore = useClubsStore()
const showInstruction = ref(false)

onMounted(async () => {
  try {
    const count = await clubsStore.ownedClubsCount()
    showInstruction.value = count === 0
  } catch {
    showInstruction.value = false
  }
})
</script>

<template>
  <div class="create-club" data-testid="create-club-page">
    <ClubForm />
    <ClubFormInstruction :open="showInstruction" @close="showInstruction = false" />
  </div>
</template>

<style scoped>
.create-club {
  width: 100%;
  max-width: 640px;
  margin: 0 auto;
}
</style>
