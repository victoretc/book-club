import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { createPinia, setActivePinia } from 'pinia'
import { useClubsStore } from '@/stores/clubs'
import PaginationControls from './PaginationControls.vue'

const meta = {
  title: 'Components/PaginationControls',
  component: PaginationControls,
  tags: ['autodocs'],
  parameters: {
    layout: 'padded',
  },
} satisfies Meta<typeof PaginationControls>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  decorators: [
    (story) => {
      const pinia = createPinia()
      setActivePinia(pinia)
      const store = useClubsStore()
      store.$patch({
        pagination: { count: 100, currentPage: 1, pageSize: 10, next: '...', previous: null },
      })
      return {
        components: { story },
        template: '<story />',
      }
    },
  ],
}

export const LastPage: Story = {
  decorators: [
    (story) => {
      const pinia = createPinia()
      setActivePinia(pinia)
      const store = useClubsStore()
      store.$patch({
        pagination: { count: 100, currentPage: 10, pageSize: 10, next: null, previous: '...' },
      })
      return {
        components: { story },
        template: '<story />',
      }
    },
  ],
}
