import api from './api'

export const menuService = {
  async getCategories() {
    const { data } = await api.get('/api/categories')
    return data
  },
  async getMenus(categoryId) {
    const params = categoryId ? { category_id: categoryId } : {}
    const { data } = await api.get('/api/menus', { params })
    return data
  },
}
