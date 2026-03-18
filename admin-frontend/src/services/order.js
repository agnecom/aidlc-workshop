import api from './api'

export const orderService = {
  async getOrders(tableId) {
    const params = tableId ? { table_id: tableId } : {}
    const { data } = await api.get('/api/orders/admin', { params })
    return data
  },
  async updateStatus(orderId, status) {
    const { data } = await api.patch(`/api/orders/${orderId}/status`, { status })
    return data
  },
  async deleteOrder(orderId) {
    await api.delete(`/api/orders/${orderId}`)
  },
}
