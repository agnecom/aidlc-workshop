import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import MenuManageView from '../MenuManageView.vue'

describe('MenuManageView', () => {
  it('renders add button', () => {
    const wrapper = mount(MenuManageView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="menu-add-button"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="menu-add-button"]').text()).toBe('메뉴 등록')
  })

  it('shows form when add button clicked', async () => {
    const wrapper = mount(MenuManageView, { global: { stubs: { RouterLink: true } } })
    await wrapper.find('[data-testid="menu-add-button"]').trigger('click')
    expect(wrapper.find('[data-testid="menu-form"]').exists()).toBe(true)
  })

  it('renders menu table', () => {
    const wrapper = mount(MenuManageView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="menu-table"]').exists()).toBe(true)
  })
})
