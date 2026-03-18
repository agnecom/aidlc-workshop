import api from './api'

export const orderService = {
  async createOrder(items, giftToTable = null, giftMessage = null) {
    const body = { items }
    if (giftToTable) body.gift_to_table = giftToTable
    if (giftMessage) body.gift_message = giftMessage
    const { data } = await api.post('/api/orders', body)
    return data
  },
  async getOrders() {
    const { data } = await api.get('/api/orders')
    return data
  },
  async getActiveTables() {
    const { data } = await api.get('/api/tables/list/active')
    return data
  },
}
