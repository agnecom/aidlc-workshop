<template>
  <div class="history-page">
    <header class="page-header">
      <button class="back-btn" @click="$router.push('/')">← 메뉴</button>
      <h1>주문 내역</h1>
      <span></span>
    </header>

    <div v-if="orders.length === 0" class="empty" data-testid="order-history-empty">
      <span class="empty-icon">📋</span>
      <p>주문 내역이 없습니다</p>
    </div>

    <div v-else class="order-list" data-testid="order-history-list">
      <div v-for="order in orders" :key="order.id" class="order-card" :data-testid="`order-item-${order.id}`"
        :class="{ 'gift-received': isGiftReceived(order), 'gift-sent': isGiftSent(order) }">

        <!-- Gift Badge -->
        <div v-if="isGiftReceived(order)" class="gift-banner received">
          🎁 테이블 {{ order.gift_from_table_number }}번에서 선물 받음
          <p v-if="order.gift_message" class="gift-msg">"{{ order.gift_message }}"</p>
        </div>
        <div v-else-if="isGiftSent(order)" class="gift-banner sent">
          🎁 테이블 {{ order.gift_to_table_number }}번에 선물 보냄
        </div>

        <div class="order-top">
          <span class="order-num">#{{ order.order_number }}</span>
          <span class="badge" :class="order.status" :data-testid="`order-status-${order.id}`">
            {{ statusLabel[order.status] }}
          </span>
        </div>
        <ul class="items">
          <li v-for="item in order.items" :key="item.id">{{ item.menu_name }} × {{ item.quantity }}</li>
        </ul>
        <div class="order-bottom">
          <span v-if="isGiftReceived(order)" class="free-label">무료</span>
          <span v-else class="order-total">{{ order.total_amount.toLocaleString() }}원</span>
        </div>
      </div>
    </div>

    <!-- Gift Notification Toast -->
    <Transition name="slide">
      <div v-if="giftToast" class="gift-toast" @click="giftToast = null">
        🎁 선물이 도착했습니다!
      </div>
    </Transition>

    <p v-if="sseError" class="warning" style="padding:1rem" data-testid="sse-error">실시간 업데이트가 중단되었습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { orderService } from '@/services/order'

const orders = ref([])
const sseError = ref(false)
const giftToast = ref(null)
const statusLabel = { pending: '접수 대기', preparing: '준비 중', completed: '완료' }
const myTableId = localStorage.getItem('table_id')

function isGiftReceived(order) {
  return order.is_gift && order.gift_to_table_id && order.table_id !== myTableId && order.gift_to_table_id !== order.table_id
}

function isGiftSent(order) {
  return order.is_gift && order.gift_to_table_id && order.table_id === myTableId
}

async function loadOrders() {
  orders.value = await orderService.getOrders()
}

onMounted(async () => {
  await loadOrders()
  const handlers = {
    'sse:new_order': () => loadOrders(),
    'sse:order_updated': () => loadOrders(),
    'sse:order_deleted': () => loadOrders(),
    'sse:gift_received': () => { giftToast.value = true; loadOrders(); setTimeout(() => { giftToast.value = null }, 4000) },
  }
  for (const [evt, fn] of Object.entries(handlers)) window.addEventListener(evt, fn)
  onUnmounted(() => { for (const [evt, fn] of Object.entries(handlers)) window.removeEventListener(evt, fn) })
})
</script>

<style scoped>
.history-page{min-height:100vh;background:var(--bg);display:flex;flex-direction:column}
.page-header{display:flex;align-items:center;justify-content:space-between;padding:.75rem 1rem;background:var(--bg-surface);border-bottom:1px solid var(--border)}
.page-header h1{font-size:1.1rem;font-weight:700}
.back-btn{background:transparent;color:var(--text-sub);font-size:.9rem;padding:.3rem .5rem}
.empty{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--text-sub)}
.empty-icon{font-size:3rem;margin-bottom:.5rem}
.order-list{padding:1rem;display:flex;flex-direction:column;gap:.6rem}
.order-card{background:var(--bg-card);border-radius:var(--radius-sm);padding:1rem;transition:all .15s}
.order-card.gift-received{border:1.5px solid #F59E0B;background:rgba(245,158,11,.08)}
.order-card.gift-sent{border:1.5px solid var(--accent);background:var(--accent-light)}
.gift-banner{font-size:.85rem;font-weight:600;margin-bottom:.6rem;padding:.4rem .6rem;border-radius:var(--radius-xs)}
.gift-banner.received{background:rgba(245,158,11,.15);color:#FBBF24}
.gift-banner.sent{background:var(--accent-light);color:var(--accent)}
.gift-msg{font-weight:400;font-size:.8rem;margin-top:.2rem;font-style:italic;color:var(--text-sub)}
.order-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem}
.order-num{font-weight:700;font-size:1rem}
.badge{font-size:.72rem;padding:.2rem .55rem;border-radius:10px;font-weight:600}
.badge.pending{background:rgba(251,191,36,.15);color:#FBBF24}
.badge.preparing{background:rgba(59,130,246,.15);color:#60A5FA}
.badge.completed{background:rgba(34,197,94,.15);color:#22C55E}
.items{list-style:none;font-size:.85rem;color:var(--text-sub);margin-bottom:.5rem}
.items li{padding:.12rem 0}
.order-bottom{text-align:right}
.order-total{font-weight:700;color:var(--accent)}
.free-label{font-weight:700;color:#22C55E;font-size:.9rem}

/* Gift Toast */
.gift-toast{position:fixed;top:1rem;left:50%;transform:translateX(-50%);background:#F59E0B;color:#000;padding:.75rem 1.5rem;border-radius:var(--radius);font-weight:700;font-size:.95rem;box-shadow:var(--shadow-lg);z-index:300;cursor:pointer}
.slide-enter-active,.slide-leave-active{transition:all .3s}
.slide-enter-from{opacity:0;transform:translateX(-50%) translateY(-20px)}
.slide-leave-to{opacity:0;transform:translateX(-50%) translateY(-20px)}
</style>
