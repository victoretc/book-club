import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { nextTick } from 'vue'
import { createPinia, setActivePinia } from 'pinia'
import { useClubsStore } from '@/stores/clubs'
import { api } from '@/api'
import ClubForm from './ClubForm.vue'

const push = vi.fn()

vi.mock('vue-router', () => ({
  useRouter: () => ({ push }),
}))

const { mockHandleSubmit } = vi.hoisted(() => ({
  mockHandleSubmit: vi.fn((cb: any) => {
    return (e?: Event) => {
      e?.preventDefault?.()
      cb({
        bookTitle: 'New Book',
        bookAuthors: 'New Author',
        publicationYear: 2024,
        description: 'New description',
        telegramChatLink: 'https://t.me/newclub',
      })
    }
  }),
}))

vi.mock('vee-validate', () => ({
  useForm: () => ({
    handleSubmit: mockHandleSubmit,
    setValues: vi.fn(),
  }),
  Field: {
    name: 'Field',
    props: ['id', 'name', 'type', 'as', 'disabled', 'placeholder'],
    template: '<input :id="id" :name="name" />',
  },
  ErrorMessage: {
    name: 'ErrorMessage',
    props: ['name'],
    template: '<span />',
  },
}))

function createWrapper(props: { clubId?: number | null } = {}) {
  return mount(ClubForm, {
    props: { clubId: props.clubId ?? null },
    global: {
      stubs: {
        BaseButton: {
          template: '<button :class="variant"><slot/></button>',
          props: ['variant', 'loading'],
        },
      },
    },
  })
}

const mockClub = {
  bookTitle: 'Test Book',
  bookAuthors: 'Test Author',
  publicationYear: 2020,
  description: 'Test description',
  telegramChatLink: 'https://t.me/test',
}

describe('ClubForm', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    push.mockClear()
  })

  it('renders create form title', () => {
    const wrapper = createWrapper()
    expect(wrapper.text()).toContain('Создать клуб')
  })

  it('renders edit form title when clubId provided', async () => {
    const clubsStore = useClubsStore()
    vi.spyOn(clubsStore, 'fetchClub').mockResolvedValue(mockClub as any)

    const wrapper = createWrapper({ clubId: 1 })
    await flushPromises()
    expect(wrapper.text()).toContain('Редактирование клуба')
  })

  it('renders all form fields', () => {
    const wrapper = createWrapper()
    expect(wrapper.find('#bookTitle').exists()).toBe(true)
    expect(wrapper.find('#bookAuthors').exists()).toBe(true)
    expect(wrapper.find('#publicationYear').exists()).toBe(true)
    expect(wrapper.find('#description').exists()).toBe(true)
    expect(wrapper.find('#telegramChatLink').exists()).toBe(true)
  })

  it('submits create form and navigates to clubs', async () => {
    vi.spyOn(api.api, 'clubsCreate').mockResolvedValue({ data: { id: 1 } } as any)

    const wrapper = createWrapper()

    await wrapper.find('form').trigger('submit')
    await flushPromises()
    await nextTick()

    expect(push).toHaveBeenCalledWith({ name: 'clubs' })
  })

  it('submits edit form and navigates to clubs', async () => {
    const clubsStore = useClubsStore()
    vi.spyOn(clubsStore, 'fetchClub').mockResolvedValue(mockClub as any)
    vi.spyOn(api.api, 'clubsUpdate').mockResolvedValue({ data: { id: 1 } } as any)

    const wrapper = createWrapper({ clubId: 1 })
    await flushPromises()

    await wrapper.find('form').trigger('submit')
    await flushPromises()
    await nextTick()

    expect(push).toHaveBeenCalledWith({ name: 'clubs' })
  })
})
