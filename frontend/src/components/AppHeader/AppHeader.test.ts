import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import AppHeader from './AppHeader.vue'

const RouterLinkStub = {
  props: { to: { type: [String, Object], default: '' } },
  template: '<a :href="typeof to === \'string\' ? to : \'/\'"><slot /></a>',
}

function createWrapper() {
  return mount(AppHeader, {
    global: {
      stubs: {
        RouterLink: RouterLinkStub,
      },
    },
  })
}

describe('AppHeader', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders the brand logo linking to home', () => {
    const wrapper = createWrapper()
    const logo = wrapper.find('[data-testid="logo-link"]')
    expect(logo.exists()).toBe(true)
    expect(logo.text()).toBe('Читальная')
    expect(logo.attributes('href')).toBe('/')
  })

  describe('when not authenticated', () => {
    it('shows "Войти" link', () => {
      const wrapper = createWrapper()
      expect(wrapper.text()).toContain('Войти')
    })

    it('hides auth-only links', () => {
      const wrapper = createWrapper()
      expect(wrapper.find('[data-testid="create-club-link"]').exists()).toBe(false)
      expect(wrapper.find('[data-testid="profile-link"]').exists()).toBe(false)
    })

    it('shows "Клубы" link', () => {
      const wrapper = createWrapper()
      const clubsLink = wrapper.find('[data-testid="clubs-link"]')
      expect(clubsLink.exists()).toBe(true)
      expect(clubsLink.text()).toContain('Клубы')
    })
  })

  describe('when authenticated', () => {
    it('shows "Создать клуб" and "Профиль" links', () => {
      const authStore = useAuthStore()
      authStore.$patch({ accessToken: 'test-token' })

      const wrapper = createWrapper()

      expect(wrapper.find('[data-testid="create-club-link"]').exists()).toBe(true)
      expect(wrapper.find('[data-testid="profile-link"]').exists()).toBe(true)
    })

    it('hides "Войти" link', () => {
      const authStore = useAuthStore()
      authStore.$patch({ accessToken: 'test-token' })

      const wrapper = createWrapper()

      expect(wrapper.text()).not.toContain('Войти')
    })
  })
})
