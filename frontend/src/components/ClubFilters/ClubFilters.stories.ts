import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { createPinia, setActivePinia } from 'pinia'
import { provide } from 'vue'
import { routerKey, routeLocationKey } from 'vue-router'
import ClubFilters from './ClubFilters.vue'

const meta = {
  title: 'Components/ClubFilters',
  component: ClubFilters,
  tags: ['autodocs'],
  parameters: {
    layout: 'padded',
  },
} satisfies Meta<typeof ClubFilters>

export default meta
type Story = StoryObj<typeof meta>

const mockRouter = { push: () => {} }
const mockRoute = { path: '/', query: {}, params: {}, hash: '', fullPath: '/', matched: [] }

export const Default: Story = {
  decorators: [
    (story) => {
      const pinia = createPinia()
      setActivePinia(pinia)
      return {
        components: { story },
        template: '<story />',
        setup() {
          provide(routerKey, mockRouter)
          provide(routeLocationKey, mockRoute)
        },
      }
    },
  ],
}
