<template>
  <div class="app-shell">
    <router-view />

    <!-- Cart Bar -->
    <div v-if="showCart" class="cart-bar">
      <div class="cart-bar-inner">
        <div class="cart-left" @click="$router.push('/cart')">
          <span class="cart-icon">🛒</span>
          <span class="cart-count">{{ cartCount }}개</span>
          <span class="cart-total">{{ cart.total.toLocaleString() }}원</span>
        </div>
        <button class="order-btn" @click="$router.push('/order')">주문하기</button>
      </div>
    </div>

    <!-- AI 추천 팝업 -->
    <Transition name="fade">
      <div v-if="recs" class="rec-overlay" @click.self="recs = null">
        <div class="rec-modal">
          <div class="rec-header">
            <span>🤖 AI 메뉴 추천</span>
            <button class="rec-close" @click="recs = null">✕</button>
          </div>
          <p class="rec-sub">주문 #{{ recs.order_number }} 완료! 이런 메뉴는 어떠세요?</p>
          <div class="rec-list">
            <div v-for="r in recs.recommendations" :key="r.menu_item_id" class="rec-card">
              <img v-if="r.image_url" :src="apiBase + r.image_url" class="rec-img" alt="">
              <div class="rec-info">
                <div class="rec-name">{{ r.name }}</div>
                <div class="rec-price">{{ r.price.toLocaleString() }}원</div>
                <div class="rec-reason">{{ r.reason }}</div>
              </div>
              <button class="rec-add" @click="addRec(r)">담기</button>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Global Toast Notifications -->
    <Transition name="slide">
      <div v-if="toast" class="toast" :class="toast.type" @click="onToastClick">
        {{ toast.text }}
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { SSEClient } from '@/services/sse'

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const route = useRoute()
const router = useRouter()
const cart = useCartStore()
const cartCount = computed(() => cart.items.reduce((s, i) => s + i.quantity, 0))
const showCart = computed(() => route.name !== 'setup' && route.name !== 'chat' && cartCount.value > 0)

const toast = ref(null)
const recs = ref(null)
let toastTimer = null
const sse = new SSEClient()

function showToast(text, type = 'info', duration = 4000, action = null) {
  toast.value = { text, type, action }
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.value = null }, duration)
}

function onToastClick() {
  if (toast.value?.action) toast.value.action()
  toast.value = null
}

function addRec(r) {
  cart.addItem({ id: r.menu_item_id, name: r.name, price: r.price, image_url: r.image_url })
  showToast(`✅ ${r.name} 장바구니에 추가!`, 'success', 2000)
}

onMounted(() => {
  const tableId = localStorage.getItem('table_id')
  if (!tableId) return

  sse.connect(tableId)

  sse.on('new_message', (data) => {
    const myNum = Number(localStorage.getItem('table_number'))
    if (data.from_table_number !== myNum) {
      showToast(`💬 테이블 ${data.from_table_number}번: ${data.message.substring(0, 40)}`, 'message', 5000,
        () => router.push(`/chat?t=${data.from_table_number}`))
    }
    window.dispatchEvent(new CustomEvent('sse:new_message', { detail: data }))
  })

  sse.on('gift_received', (data) => {
    showToast(`🎁 테이블 ${data.gift_from_table_number}번에서 선물이 도착했습니다!`, 'gift', 5000,
      () => router.push('/orders'))
    window.dispatchEvent(new CustomEvent('sse:gift_received', { detail: data }))
  })

  sse.on('new_order', (data) => {
    window.dispatchEvent(new CustomEvent('sse:new_order', { detail: data }))
  })

  sse.on('order_updated', (data) => {
    const status = data.status
    if (status === 'preparing') showToast(`🍳 주문 #${data.order_number} 준비가 시작되었습니다`, 'info')
    else if (status === 'completed') showToast(`✅ 주문 #${data.order_number} 준비 완료!`, 'success')
    window.dispatchEvent(new CustomEvent('sse:order_updated', { detail: data }))
  })

  sse.on('order_deleted', (data) => {
    window.dispatchEvent(new CustomEvent('sse:order_deleted', { detail: data }))
  })

  sse.on('menu_recommendation', (data) => {
    recs.value = data
  })
})

onUnmounted(() => sse.disconnect())
</script>

<style scoped>
.app-shell{min-height:100vh;min-height:100dvh}

/* Cart Bar */
.cart-bar{position:fixed;bottom:0;left:0;right:0;padding:.6rem .8rem;z-index:100}
.cart-bar-inner{background:var(--accent);border-radius:var(--radius);padding:.7rem 1rem;display:flex;align-items:center;box-shadow:var(--shadow-lg)}
.cart-left{display:flex;align-items:center;gap:.5rem;flex:1;cursor:pointer}
.cart-icon{font-size:1.2rem}
.cart-count{background:rgba(255,255,255,.2);padding:.15rem .5rem;border-radius:10px;font-size:.8rem;font-weight:600}
.cart-total{font-weight:700;font-size:1rem}
.order-btn{background:#fff;color:var(--accent);font-weight:700;padding:.55rem 1.2rem;border-radius:var(--radius-sm);font-size:.95rem}

/* Toast */
.toast{position:fixed;top:.8rem;left:50%;transform:translateX(-50%);padding:.75rem 1.2rem;border-radius:var(--radius);font-weight:600;font-size:.9rem;z-index:300;cursor:pointer;max-width:90%;text-align:center;box-shadow:var(--shadow-lg);white-space:pre-line}
.toast.info{background:var(--bg-card);color:var(--text);border:1px solid var(--border)}
.toast.message{background:#4F46E5;color:#fff}
.toast.gift{background:#F59E0B;color:#000}
.toast.success{background:#22C55E;color:#fff}
.slide-enter-active,.slide-leave-active{transition:all .3s}
.slide-enter-from{opacity:0;transform:translateX(-50%) translateY(-20px)}
.slide-leave-to{opacity:0;transform:translateX(-50%) translateY(-20px)}

/* Recommendation Modal */
.rec-overlay{position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:200;display:flex;align-items:flex-end;justify-content:center}
.rec-modal{background:var(--bg-card);border-radius:var(--radius) var(--radius) 0 0;width:100%;max-width:480px;max-height:70vh;overflow-y:auto;padding:1.2rem}
.rec-header{display:flex;justify-content:space-between;align-items:center;font-size:1.1rem;font-weight:700}
.rec-close{background:none;color:var(--text-muted);font-size:1.2rem;padding:.2rem}
.rec-sub{color:var(--text-muted);font-size:.85rem;margin:.4rem 0 1rem}
.rec-list{display:flex;flex-direction:column;gap:.8rem}
.rec-card{display:flex;align-items:center;gap:.8rem;background:var(--bg);border-radius:var(--radius-sm);padding:.7rem}
.rec-img{width:60px;height:60px;border-radius:var(--radius-sm);object-fit:cover}
.rec-info{flex:1;min-width:0}
.rec-name{font-weight:700;font-size:.95rem}
.rec-price{color:var(--accent);font-weight:600;font-size:.9rem}
.rec-reason{color:var(--text-muted);font-size:.8rem;margin-top:.15rem}
.rec-add{background:var(--accent);color:#fff;font-weight:700;padding:.45rem .9rem;border-radius:var(--radius-sm);font-size:.85rem;white-space:nowrap}
.fade-enter-active,.fade-leave-active{transition:opacity .3s}
.fade-enter-from,.fade-leave-to{opacity:0}
</style>
