import api from './api'

const STORAGE_KEY = 'table_credentials'
const TOKEN_KEY = 'table_token'
const SESSION_KEY = 'table_session_id'

export const authService = {
  saveCredentials(storeId, tableNumber, password) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ storeId, tableNumber, password }))
  },

  getCredentials() {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : null
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY)
  },

  getSessionId() {
    return localStorage.getItem(SESSION_KEY)
  },

  async login(storeId, tableNumber, password) {
    const { data } = await api.post('/api/auth/table/login', {
      store_id: storeId,
      table_number: tableNumber,
      password,
    })
    localStorage.setItem(TOKEN_KEY, data.access_token)
    localStorage.setItem(SESSION_KEY, data.session_id)
    // Decode table_id and table_number from JWT
    try {
      const payload = JSON.parse(atob(data.access_token.split('.')[1]))
      if (payload.table_id) localStorage.setItem('table_id', payload.table_id)
      if (payload.table_number) localStorage.setItem('table_number', payload.table_number)
    } catch {}
    return data
  },

  async autoLogin() {
    const creds = this.getCredentials()
    if (!creds) return false
    try {
      await this.login(creds.storeId, creds.tableNumber, creds.password)
      return true
    } catch {
      return false
    }
  },

  isAuthenticated() {
    return !!localStorage.getItem(TOKEN_KEY)
  },
}
