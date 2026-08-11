<script setup lang="ts">
import ClubForm from '@/components/ClubForm/ClubForm.vue'
import ClubFormInstruction from '@/components/ClubFormInstruction/ClubFormInstruction.vue'
</script>

<template>
  <div class="create-club" data-testid="create-club-page">
    <div class="create-club-form">
      <ClubForm />
    </div>
    <ClubFormInstruction />
  </div>
</template>

<style scoped>
.create-club {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 24px;
  align-items: start;
  width: 100%;
}

.create-club-form {
  min-width: 0;
}

@media (max-width: 900px) {
  .create-club {
    grid-template-columns: 1fr;
  }
}
</style>
