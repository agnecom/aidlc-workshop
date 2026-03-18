import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const tableId = localStorage.getItem('table_id') || ''
  const storageKey = `cart_${tableId}`
  const items = ref(JSON.parse(localStorage.getItem(storageKey) || '[]'))

  const total = computed(() => items.value.reduce((s, i) => s + i.price * i.quantity, 0))
  const itemCount = computed(() => items.value.reduce((s, i) => s + i.quantity, 0))

  watch(items, (v) => localStorage.setItem(storageKey, JSON.stringify(v)), { deep: true })

  function addItem(menuItem, qty = 1) {
    const existing = items.value.find(i => i.menu_item_id === menuItem.id)
    if (existing) {
      existing.quantity = Math.min(existing.quantity + qty, 99)
    } else {
      items.value.push({ menu_item_id: menuItem.id, name: menuItem.name, price: menuItem.price, quantity: qty, image_url: menuItem.image_url })
    }
  }

  function removeItem(menuItemId) {
    items.value = items.value.filter(i => i.menu_item_id !== menuItemId)
  }

  function updateQuantity(menuItemId, qty) {
    if (qty < 1) return removeItem(menuItemId)
    const item = items.value.find(i => i.menu_item_id === menuItemId)
    if (item) item.quantity = Math.min(qty, 99)
  }

  function clearCart() {
    items.value = []
  }

  return { items, total, itemCount, addItem, removeItem, updateQuantity, clearCart }
})
