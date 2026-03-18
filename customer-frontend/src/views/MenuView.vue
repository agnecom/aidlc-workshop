<template>
  <div class="menu-page">
    <!-- Header -->
    <header class="top-bar">
      <span class="store-name">🍽 테이블 {{ tableNumber }}번</span>
      <div class="header-actions">
        <router-link to="/chat" class="header-btn">💬</router-link>
        <router-link to="/orders" class="header-btn">주문내역</router-link>
        <button class="header-btn" @click="logout">로그아웃</button>
      </div>
    </header>

    <div class="menu-body">
      <!-- Left: Category Tabs -->
      <aside class="cat-sidebar">
        <button v-for="cat in categories" :key="cat.id"
          :class="['cat-tab', { active: selectedCategory === cat.id }]"
          @click="selectedCategory = cat.id"
          :data-testid="`category-btn-${cat.id}`">
          {{ cat.name }}
        </button>
      </aside>

      <!-- Right: Menu Grid -->
      <section class="menu-area">
        <div class="menu-grid" data-testid="menu-grid">
          <div v-for="item in filteredMenus" :key="item.id" class="menu-card" :data-testid="`menu-card-${item.id}`" @click="addToCart(item)">
            <div class="card-img">
              <img v-if="item.image_url" :src="apiBase + item.image_url" :alt="item.name" loading="lazy" />
              <div v-else class="img-placeholder">🍽</div>
            </div>
            <div class="card-info">
              <h3 class="card-name">{{ item.name }}</h3>
              <p v-if="item.description" class="card-desc">{{ item.description }}</p>
              <div class="card-bottom">
                <span class="card-price">{{ item.price.toLocaleString() }}원</span>
                <button class="add-btn" :data-testid="`menu-add-cart-${item.id}`">
                  <span class="plus">+</span>
                </button>
              </div>
            </div>
            <!-- Quantity badge -->
            <div v-if="getQty(item.id)" class="qty-badge">{{ getQty(item.id) }}</div>
          </div>
        </div>
      </section>
    </div>

    <p v-if="error" class="error" style="padding:1rem" data-testid="menu-error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { menuService } from '@/services/menu'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const cart = useCartStore()
const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const categories = ref([])
const menus = ref([])
const selectedCategory = ref(null)
const error = ref('')
const tableNumber = localStorage.getItem('table_number') || '?'

const filteredMenus = computed(() => {
  if (!selectedCategory.value) return menus.value
  return menus.value.filter(m => m.category_id === selectedCategory.value)
})

function getQty(menuId) {
  const item = cart.items.find(i => i.menu_item_id === menuId)
  return item ? item.quantity : 0
}

onMounted(async () => {
  try {
    categories.value = await menuService.getCategories()
    menus.value = await menuService.getMenus()
    if (categories.value.length) selectedCategory.value = categories.value[0].id
  } catch {
    error.value = '메뉴를 불러올 수 없습니다.'
  }
})

function addToCart(item) {
  cart.addItem(item)
}

function logout() {
  localStorage.clear()
  router.push('/setup')
}
</script>

<style scoped>
.menu-page{display:flex;flex-direction:column;height:100vh;height:100dvh;background:var(--bg);padding-bottom:70px}

/* Top Bar */
.top-bar{display:flex;align-items:center;justify-content:space-between;padding:.75rem 1rem;background:var(--bg-surface);border-bottom:1px solid var(--border)}
.store-name{font-weight:700;font-size:1.05rem}
.header-actions{display:flex;gap:.4rem}
.header-btn{font-size:.85rem;color:var(--text-sub);padding:.4rem .7rem;border:1px solid var(--border);border-radius:var(--radius-xs);text-decoration:none}
.header-btn:hover{color:var(--accent);border-color:var(--accent)}

/* Body Layout */
.menu-body{display:flex;flex:1;overflow:hidden}

/* Category Sidebar */
.cat-sidebar{width:90px;min-width:90px;background:var(--bg-surface);border-right:1px solid var(--border);overflow-y:auto;display:flex;flex-direction:column}
.cat-tab{padding:.85rem .4rem;text-align:center;font-size:.8rem;font-weight:500;color:var(--text-sub);background:transparent;border-radius:0;border-left:3px solid transparent;transition:all .15s;word-break:keep-all;line-height:1.3}
.cat-tab:hover{color:var(--text);background:var(--bg-card)}
.cat-tab.active{color:var(--accent);background:var(--bg-card);border-left-color:var(--accent);font-weight:700}

/* Menu Area */
.menu-area{flex:1;overflow-y:auto;padding:.75rem}
.menu-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:.65rem}

/* Menu Card */
.menu-card{background:var(--bg-card);border-radius:var(--radius-sm);overflow:hidden;cursor:pointer;transition:transform .12s,box-shadow .12s;position:relative}
.menu-card:active{transform:scale(.97)}
.menu-card:hover{box-shadow:var(--shadow)}
.card-img{height:120px;overflow:hidden;background:#1E1E1E}
.card-img img{width:100%;height:100%;object-fit:cover;transition:transform .2s}
.menu-card:hover .card-img img{transform:scale(1.05)}
.img-placeholder{height:100%;display:flex;align-items:center;justify-content:center;font-size:2rem;color:var(--text-dim)}
.card-info{padding:.6rem .7rem .7rem}
.card-name{font-size:.88rem;font-weight:600;margin-bottom:.15rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card-desc{font-size:.7rem;color:var(--text-sub);margin-bottom:.4rem;display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}
.card-bottom{display:flex;align-items:center;justify-content:space-between}
.card-price{font-weight:700;color:var(--accent);font-size:.95rem}
.add-btn{width:30px;height:30px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;padding:0}
.add-btn:hover{background:var(--accent-dark)}
.plus{color:#fff;font-size:1.2rem;font-weight:700;line-height:1}

/* Quantity Badge */
.qty-badge{position:absolute;top:6px;right:6px;background:var(--accent);color:#fff;min-width:22px;height:22px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;padding:0 5px;box-shadow:0 2px 6px rgba(0,0,0,.3)}
</style>
