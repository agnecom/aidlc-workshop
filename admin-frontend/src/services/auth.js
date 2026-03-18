import api from './api'

const TOKEN_KEY = 'admin_token'

export const authService = {
  async login(storeIdentifier, username, password) {
    const { data } = await api.post('/api/auth/admin/login', {
      store_identifier: storeIdentifier,
      username,
      password,
    })
    localStorage.setItem(TOKEN_KEY, data.access_token)
    return data
  },

  logout() {
    localStorage.removeItem(TOKEN_KEY)
  },

  isAuthenticated() {
    return !!localStorage.getItem(TOKEN_KEY)
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY)
  },
}
