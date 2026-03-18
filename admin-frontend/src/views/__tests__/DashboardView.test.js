import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import DashboardView from '../DashboardView.vue'

describe('DashboardView', () => {
  it('renders dashboard grid', () => {
    const wrapper = mount(DashboardView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="dashboard-grid"]').exists()).toBe(true)
  })

  it('renders nav link to menus', () => {
    const wrapper = mount(DashboardView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="nav-menus"]').exists()).toBe(true)
  })

  it('does not show order detail initially', () => {
    const wrapper = mount(DashboardView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="order-detail-panel"]').exists()).toBe(false)
  })
})
