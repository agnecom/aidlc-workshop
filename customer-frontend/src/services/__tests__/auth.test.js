import { describe, it, expect, vi, beforeEach } from 'vitest'
import { authService } from '../auth'

describe('authService', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it('saveCredentials stores to localStorage', () => {
    authService.saveCredentials('s1', 1, 'pw')
    const stored = JSON.parse(localStorage.getItem('table_credentials'))
    expect(stored).toEqual({ storeId: 's1', tableNumber: 1, password: 'pw' })
  })

  it('getCredentials returns null when empty', () => {
    expect(authService.getCredentials()).toBeNull()
  })

  it('isAuthenticated returns false without token', () => {
    expect(authService.isAuthenticated()).toBe(false)
  })

  it('isAuthenticated returns true with token', () => {
    localStorage.setItem('table_token', 'test-token')
    expect(authService.isAuthenticated()).toBe(true)
  })
})
