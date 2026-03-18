import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import LoginView from '../LoginView.vue'

describe('LoginView', () => {
  it('renders login form', () => {
    const wrapper = mount(LoginView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="login-form"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="login-store-identifier"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="login-username"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="login-password"]').exists()).toBe(true)
    expect(wrapper.find('[data-testid="login-submit-button"]').exists()).toBe(true)
  })

  it('submit button text is 로그인', () => {
    const wrapper = mount(LoginView, { global: { stubs: { RouterLink: true } } })
    expect(wrapper.find('[data-testid="login-submit-button"]').text()).toBe('로그인')
  })
})
