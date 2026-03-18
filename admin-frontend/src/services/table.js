import api from './api'

export const tableService = {
  async getTables() {
    const { data } = await api.get('/api/tables')
    return data
  },
  async getTableDetail(tableId) {
    const { data } = await api.get(`/api/tables/${tableId}`)
    return data
  },
  async createTable(tableNumber, password) {
    const { data } = await api.post('/api/tables', { table_number: tableNumber, password })
    return data
  },
  async updateTable(tableId, password) {
    const { data } = await api.put(`/api/tables/${tableId}`, { password })
    return data
  },
  async completeTable(tableId) {
    await api.post(`/api/tables/${tableId}/complete`)
  },
  async getHistory(tableId, dateFrom, dateTo) {
    const params = {}
    if (dateFrom) params.date_from = dateFrom
    if (dateTo) params.date_to = dateTo
    const { data } = await api.get(`/api/tables/${tableId}/history`, { params })
    return data
  },
}
