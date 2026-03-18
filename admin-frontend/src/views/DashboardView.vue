<template>
  <div class="dashboard">
    <h1>대시보드</h1>

    <div class="table-grid" data-testid="dashboard-grid">
      <div v-for="table in tables" :key="table.table_id"
        class="table-card" :class="{ highlight: table.highlight, selected: selectedTable?.table_id === table.table_id }"
        :data-testid="`table-card-${table.table_id}`"
        @click="selectTable(table)">
        <div class="table-num">T{{ table.table_number || '?' }}</div>
        <div class="table-info">
          <span class="table-total">{{ table.total.toLocaleString() }}원</span>
          <span class="table-count">{{ table.orders.length }}건</span>
        </div>
      </div>
      <div v-if="tables.length === 0" class="empty-grid">
        <p>활성 주문이 없습니다</p>
      </div>
    </div>

    <div v-if="selectedTable" class="order-panel" data-testid="order-detail-panel">
      <div class="panel-header">
        <h2>테이블 {{ selectedTable.table_number }} 주문</h2>
        <button class="btn-sm btn-outline" @click="selectedTable = null" data-testid="close-detail">✕</button>
      </div>
      <div v-for="order in selectedTable.orders" :key="order.id" class="order-card" :data-testid="`order-detail-${order.id}`">
        <div class="order-top">
          <span class="order-num">#{{ order.order_number }}</span>
          <span class="status-badge" :class="order.status">{{ statusLabel[order.status] }}</span>
          <span class="order-amount">{{ order.total_amount.toLocaleString() }}원</span>
        </div>
        <ul class="order-items"><li v-for="item in order.items" :key="item.id">{{ item.menu_name }} × {{ item.quantity }}</li></ul>
        <div class="order-actions">
          <button v-if="order.status === 'pending'" class="btn-sm btn-warning" @click="changeStatus(order.id, 'preparing')"
            :data-testid="`status-btn-preparing-${order.id}`">준비 시작</button>
          <button v-if="order.status === 'preparing'" class="btn-sm btn-success" @click="changeStatus(order.id, 'completed')"
            :data-testid="`status-btn-completed-${order.id}`">완료</button>
          <button class="btn-sm btn-danger" @click="removeOrder(order.id)" :data-testid="`order-delete-${order.id}`">삭제</button>
        </div>
      </div>
    </div>

    <p v-if="sseError" class="warning" data-testid="sse-error">실시간 연결이 끊어졌습니다. 페이지를 새로고침해 주세요.</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { orderService } from '@/services/order'
import { SSEClient } from '@/services/sse'

const tables = ref([])
const selectedTable = ref(null)
const sseError = ref(false)
const statusLabel = { pending: '대기중', preparing: '준비중', completed: '완료' }
const sse = new SSEClient()

function groupByTable(orders) {
  const map = {}
  for (const o of orders) {
    if (!map[o.table_id]) map[o.table_id] = { table_id: o.table_id, table_number: null, orders: [], total: 0, highlight: false }
    map[o.table_id].orders.push(o)
    map[o.table_id].total += o.total_amount
  }
  return Object.values(map)
}

async function loadOrders() {
  const orders = await orderService.getOrders()
  tables.value = groupByTable(orders)
  if (selectedTable.value) {
    selectedTable.value = tables.value.find(t => t.table_id === selectedTable.value.table_id) || null
  }
}

function selectTable(table) { selectedTable.value = table }

async function changeStatus(orderId, status) {
  await orderService.updateStatus(orderId, status)
  await loadOrders()
}

async function removeOrder(orderId) {
  if (!confirm('이 주문을 삭제하시겠습니까?')) return
  await orderService.deleteOrder(orderId)
  await loadOrders()
}

onMounted(async () => {
  await loadOrders()
  sse.connect()
  sse.on('new_order', async () => { await loadOrders(); highlightTable() })
  sse.on('order_updated', () => loadOrders())
  sse.on('order_deleted', () => loadOrders())
  sse.on('error', () => { sseError.value = true })
})

function highlightTable() {
  if (tables.value.length) {
    tables.value[0].highlight = true
    setTimeout(() => { tables.value[0].highlight = false }, 2000)
  }
}

onUnmounted(() => sse.disconnect())
</script>

<style scoped>
.dashboard h1{font-size:1.5rem;margin-bottom:1.25rem}
.table-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:.75rem;margin-bottom:1.5rem}
.table-card{background:#fff;border:2px solid var(--gray-200);border-radius:var(--radius);padding:1rem;text-align:center;cursor:pointer;transition:all .15s}
.table-card:hover{border-color:var(--primary);box-shadow:var(--shadow)}
.table-card.selected{border-color:var(--primary);background:var(--primary-light)}
.table-card.highlight{animation:pulse .6s ease-in-out 3}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.05);box-shadow:0 0 12px rgba(79,70,229,.3)}}
.table-num{font-size:1.3rem;font-weight:700;color:var(--primary);margin-bottom:.25rem}
.table-total{font-weight:600;font-size:.9rem}
.table-count{font-size:.8rem;color:var(--gray-500);display:block}
.empty-grid{grid-column:1/-1;text-align:center;padding:2rem;color:var(--gray-500)}
.order-panel{background:#fff;border-radius:var(--radius);padding:1.25rem;box-shadow:var(--shadow-md)}
.panel-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem}
.panel-header h2{font-size:1.15rem}
.order-card{border:1px solid var(--gray-200);border-radius:var(--radius-sm);padding:.75rem;margin-bottom:.5rem}
.order-top{display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem}
.order-num{font-weight:700}
.status-badge{font-size:.7rem;padding:.2rem .5rem;border-radius:10px;font-weight:600}
.status-badge.pending{background:#FEF3C7;color:#92400E}
.status-badge.preparing{background:#DBEAFE;color:#1E40AF}
.status-badge.completed{background:#D1FAE5;color:#065F46}
.order-amount{margin-left:auto;font-weight:600}
.order-items{list-style:none;font-size:.85rem;color:var(--gray-500);margin-bottom:.5rem}
.order-items li{padding:.1rem 0}
.order-actions{display:flex;gap:.5rem}
</style>
