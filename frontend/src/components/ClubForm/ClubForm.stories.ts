import type { Meta, StoryObj } from '@storybook/vue3-vite'
import { createPinia, setActivePinia } from 'pinia'
import { provide } from 'vue'
import { routerKey, routeLocationKey } from 'vue-router'
import { useClubsStore } from '@/stores/clubs'
import ClubForm from './ClubForm.vue'

const meta = {
  title: 'Components/ClubForm',
  component: ClubForm,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
} satisfies Meta<typeof ClubForm>

export default meta
type Story = StoryObj<typeof meta>

const mockRouter = { push: () => {} }
const mockRoute = { path: '/', query: {}, params: {}, hash: '', fullPath: '/', matched: [] }

export const Create: Story = {
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

export const Edit: Story = {
  decorators: [
    (story) => {
      const pinia = createPinia()
      setActivePinia(pinia)
      const clubsStore = useClubsStore()
      clubsStore.fetchClub = async () => ({
        id: 1,
        bookTitle: 'Test Book',
        bookAuthors: 'Test Author',
        publicationYear: 2020,
        description: 'Test description',
        telegramChatLink: 'https://t.me/test',
      })
      return {
        components: { story },
        template: '<story :clubId="1" />',
        setup() {
          provide(routerKey, mockRouter)
          provide(routeLocationKey, mockRoute)
        },
      }
    },
  ],
}
