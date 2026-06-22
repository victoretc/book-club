import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useClubsStore } from '@/stores/clubs'
import ClubFilters from './ClubFilters.vue'

const push = vi.fn()

vi.mock('vue-router', () => ({
  useRouter: () => ({ push }),
}))

function createWrapper() {
  return mount(ClubFilters, {
    global: {
      stubs: {
        BaseButton: {
          template: '<button :class="variant" @click="$emit(\'click\')"><slot/></button>',
          props: ['variant', 'loading'],
        },
      },
    },
  })
}

describe('ClubFilters', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    push.mockClear()
  })

  it('renders search input', () => {
    const wrapper = createWrapper()
    expect(wrapper.find('input[placeholder="Найти книжный клуб"]').exists()).toBe(true)
  })

  it('renders filter tabs', () => {
    const wrapper = createWrapper()
    expect(wrapper.text()).toContain('Все клубы')
    expect(wrapper.text()).toContain('Участвую')
    expect(wrapper.text()).toContain('Мои клубы')
  })

  it('updates search query on input', async () => {
    const wrapper = createWrapper()
    const input = wrapper.find('input')
    await input.setValue('test')
    expect((input.element as HTMLInputElement).value).toBe('test')
  })

  it('redirects to signin when unauthenticated user clicks member filter', async () => {
    const wrapper = createWrapper()
    const buttons = wrapper.findAll('.filter-tab')
    const memberBtn = buttons.find((b) => b.text() === 'Участвую')
    expect(memberBtn).toBeDefined()
    await memberBtn!.trigger('click')
    expect(push).toHaveBeenCalledWith('/signin')
  })

  it('redirects to signin when unauthenticated user clicks my clubs filter', async () => {
    const wrapper = createWrapper()
    const buttons = wrapper.findAll('.filter-tab')
    const myClubsBtn = buttons.find((b) => b.text() === 'Мои клубы')
    expect(myClubsBtn).toBeDefined()
    await myClubsBtn!.trigger('click')
    expect(push).toHaveBeenCalledWith('/signin')
  })

  it('calls filterByMembership when authenticated user clicks filter', async () => {
    const authStore = useAuthStore()
    authStore.$patch({ accessToken: 'test', user: { id: 1, username: 'test' } } as any)
    const clubsStore = useClubsStore()
    vi.spyOn(clubsStore, 'filterByMembership').mockResolvedValue(undefined)

    const wrapper = createWrapper()
    const buttons = wrapper.findAll('.filter-tab')
    const memberBtn = buttons.find((b) => b.text() === 'Участвую')
    await memberBtn!.trigger('click')

    expect(clubsStore.filterByMembership).toHaveBeenCalledWith('member')
  })

  it('does not redirect when authenticated user clicks filter', async () => {
    const authStore = useAuthStore()
    authStore.$patch({ accessToken: 'test', user: { id: 1, username: 'test' } } as any)
    const clubsStore = useClubsStore()
    vi.spyOn(clubsStore, 'filterByMembership').mockResolvedValue(undefined)

    const wrapper = createWrapper()
    const buttons = wrapper.findAll('.filter-tab')
    const memberBtn = buttons.find((b) => b.text() === 'Участвую')
    await memberBtn!.trigger('click')

    expect(push).not.toHaveBeenCalled()
  })

  it('calls searchClubs when search button is clicked', async () => {
    const clubsStore = useClubsStore()
    vi.spyOn(clubsStore, 'searchClubs').mockResolvedValue(undefined)

    const wrapper = createWrapper()
    const input = wrapper.find('input')
    await input.setValue('fantasy')
    await wrapper.find('.search-btn').trigger('click')

    expect(clubsStore.searchClubs).toHaveBeenCalledWith('fantasy')
  })
})
