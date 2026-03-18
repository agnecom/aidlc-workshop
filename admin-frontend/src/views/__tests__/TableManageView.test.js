import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TableManageView from '../TableManageView.vue'

describe('TableManageView', () => {
  it('renders add button', () => {
    const wrapper = mount(TableManageView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="table-add-btn"]').exists()).toBe(true)
  })

  it('shows form when add button clicked', async () => {
    const wrapper = mount(TableManageView, { global: { stubs: { RouterLink: true } } })
    await wrapper.find('[data-testid="table-add-btn"]').trigger('click')
    expect(wrapper.find('[data-testid="table-form"]').exists()).toBe(true)
  })

  it('renders table list', () => {
    const wrapper = mount(TableManageView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="table-list"]').exists()).toBe(true)
  })
})
