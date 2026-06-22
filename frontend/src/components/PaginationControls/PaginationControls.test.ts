import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { useClubsStore } from '@/stores/clubs'
import PaginationControls from './PaginationControls.vue'

function createWrapper() {
  return mount(PaginationControls)
}

describe('PaginationControls', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('renders page buttons based on total pages', () => {
    const store = useClubsStore()
    store.$patch({
      pagination: { count: 50, currentPage: 1, pageSize: 10, next: '...', previous: null },
    })

    const wrapper = createWrapper()
    const buttons = wrapper.findAll('.page-btn')
    expect(buttons.length).toBeGreaterThan(1)
  })

  it('disables previous button on first page', () => {
    const store = useClubsStore()
    store.$patch({
      pagination: { count: 50, currentPage: 1, pageSize: 10, next: '...', previous: null },
    })

    const wrapper = createWrapper()
    const buttons = wrapper.findAll('.page-btn')
    const prevBtn = buttons.at(0)
    expect(prevBtn?.attributes('disabled')).toBeDefined()
  })

  it('disables next button on last page', () => {
    const store = useClubsStore()
    store.$patch({
      pagination: { count: 50, currentPage: 5, pageSize: 10, next: null, previous: '...' },
    })

    const wrapper = createWrapper()
    const buttons = wrapper.findAll('.page-btn')
    const nextBtn = buttons.at(buttons.length - 1)
    expect(nextBtn?.attributes('disabled')).toBeDefined()
  })

  it('highlights current page button', () => {
    const store = useClubsStore()
    store.$patch({
      pagination: { count: 50, currentPage: 3, pageSize: 10, next: '...', previous: '...' },
    })

    const wrapper = createWrapper()
    const active = wrapper.find('.page-btn.active')
    expect(active.exists()).toBe(true)
    expect(active.text()).toBe('3')
  })

  it('opens page size selector on click', async () => {
    const store = useClubsStore()
    store.$patch({
      pagination: { count: 50, currentPage: 1, pageSize: 10, next: '...', previous: null },
    })

    const wrapper = createWrapper()
    await wrapper.find('.select-header').trigger('click')
    expect(wrapper.find('.select-dropdown').classes()).toContain('open')
  })
})
