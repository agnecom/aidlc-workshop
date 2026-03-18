<template>
  <div class="admin-shell">
    <aside v-if="showSidebar" class="sidebar">
      <div class="sidebar-brand">🏪 테이블오더</div>
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-link" active-class="active" :exact="true">📊 대시보드</router-link>
        <router-link to="/menus" class="nav-link" active-class="active">🍽 메뉴 관리</router-link>
        <router-link to="/tables" class="nav-link" active-class="active">🪑 테이블 관리</router-link>
      </nav>
      <button class="logout-btn" @click="logout">로그아웃</button>
    </aside>
    <main :class="['main-content', { 'no-sidebar': !showSidebar }]">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authService } from '@/services/auth'

const route = useRoute()
const router = useRouter()
const showSidebar = computed(() => route.name !== 'login')

function logout() {
  authService.logout()
  router.push({ name: 'login' })
}
</script>

<style scoped>
.admin-shell{display:flex;min-height:100vh}
.sidebar{width:220px;background:#fff;border-right:1px solid var(--gray-200);display:flex;flex-direction:column;padding:1.25rem 0;position:fixed;top:0;bottom:0;z-index:50}
.sidebar-brand{padding:0 1.25rem .75rem;font-size:1.1rem;font-weight:700;color:var(--primary);border-bottom:1px solid var(--gray-100);margin-bottom:.5rem;padding-bottom:1rem}
.sidebar-nav{flex:1;display:flex;flex-direction:column;gap:.15rem;padding:0 .75rem}
.nav-link{display:block;padding:.6rem .75rem;border-radius:var(--radius-sm);color:var(--gray-700);font-size:.9rem;transition:all .15s}
.nav-link:hover{background:var(--gray-100)}
.nav-link.active{background:var(--primary-light);color:var(--primary);font-weight:600}
.logout-btn{margin:.75rem 1rem 0;background:var(--gray-100);color:var(--gray-700);font-size:.85rem}
.logout-btn:hover{background:var(--gray-200)}
.main-content{margin-left:220px;flex:1;padding:1.5rem 2rem}
.main-content.no-sidebar{margin-left:0}
</style>
