import api from './api'

export const menuService = {
  async getCategories() {
    const { data } = await api.get('/api/categories/admin')
    return data
  },
  async getMenus(categoryId) {
    const params = categoryId ? { category_id: categoryId } : {}
    const { data } = await api.get('/api/menus/admin', { params })
    return data
  },
  async createMenu(formData) {
    const { data } = await api.post('/api/menus', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    return data
  },
  async updateMenu(id, formData) {
    const { data } = await api.put(`/api/menus/${id}`, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    return data
  },
  async deleteMenu(id) {
    await api.delete(`/api/menus/${id}`)
  },
  async updateOrder(id, displayOrder) {
    const { data } = await api.patch(`/api/menus/${id}/order`, { display_order: displayOrder })
    return data
  },
}
