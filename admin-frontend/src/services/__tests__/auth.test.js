import { describe, it, expect, beforeEach } from 'vitest'
import { authService } from '../auth'

describe('authService', () => {
  beforeEach(() => { localStorage.clear() })

  it('isAuthenticated returns false without token', () => {
    expect(authService.isAuthenticated()).toBe(false)
  })

  it('isAuthenticated returns true with token', () => {
    localStorage.setItem('admin_token', 'test')
    expect(authService.isAuthenticated()).toBe(true)
  })

  it('logout removes token', () => {
    localStorage.setItem('admin_token', 'test')
    authService.logout()
    expect(authService.isAuthenticated()).toBe(false)
  })
})
