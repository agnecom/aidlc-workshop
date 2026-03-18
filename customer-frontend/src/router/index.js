import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '@/services/auth'
import InitialSetupView from '@/views/InitialSetupView.vue'

const routes = [
  { path: '/setup', name: 'setup', component: InitialSetupView },
  { path: '/', name: 'menu', component: () => import('@/views/MenuView.vue'), meta: { requiresAuth: true } },
  { path: '/cart', name: 'cart', component: () => import('@/views/CartView.vue'), meta: { requiresAuth: true } },
  { path: '/order', name: 'order', component: () => import('@/views/OrderView.vue'), meta: { requiresAuth: true } },
  { path: '/orders', name: 'orders', component: () => import('@/views/OrderHistoryView.vue'), meta: { requiresAuth: true } },
  { path: '/chat', name: 'chat', component: () => import('@/views/ChatView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) return true
  if (authService.isAuthenticated()) return true
  const ok = await authService.autoLogin()
  if (ok) return true
  return { name: 'setup' }
})

export default router
