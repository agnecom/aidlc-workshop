import api from './api'

export const messageService = {
  async send(toTableNumber, message) {
    const { data } = await api.post('/api/messages', { to_table_number: toTableNumber, message })
    return data
  },
  async getMessages(tableNumber) {
    const { data } = await api.get(`/api/messages/${tableNumber}`)
    return data
  },
  async getActiveTables() {
    const { data } = await api.get('/api/tables/list/active')
    return data
  },
}
