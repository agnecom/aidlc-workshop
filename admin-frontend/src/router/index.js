import { createRouter, createWebHistory } from 'vue-router'
import { authService } from '@/services/auth'
import LoginView from '@/views/LoginView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView },
  { path: '/', name: 'dashboard', component: () => import('@/views/DashboardView.vue'), meta: { requiresAuth: true } },
  { path: '/menus', name: 'menus', component: () => import('@/views/MenuManageView.vue'), meta: { requiresAuth: true } },
  { path: '/tables', name: 'tables', component: () => import('@/views/TableManageView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to) => {
  if (!to.meta.requiresAuth) return true
  if (authService.isAuthenticated()) return true
  return { name: 'login' }
})

export default router
