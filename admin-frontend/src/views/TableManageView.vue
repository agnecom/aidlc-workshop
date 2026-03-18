<template>
  <div class="table-manage">
    <div class="page-top">
      <h1>테이블 관리</h1>
      <button class="btn-primary" @click="showForm = true" data-testid="table-add-btn">+ 테이블 추가</button>
    </div>

    <!-- Create Form -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal" data-testid="table-form">
        <h2>테이블 추가</h2>
        <div class="form-stack">
          <div class="form-group">
            <label>테이블 번호</label>
            <input v-model.number="form.tableNumber" type="number" min="1" data-testid="table-form-number" />
          </div>
          <div class="form-group">
            <label>비밀번호</label>
            <input v-model="form.password" type="password" data-testid="table-form-password" />
          </div>
          <div class="form-actions">
            <button class="btn-outline" @click="showForm = false" data-testid="table-form-cancel">취소</button>
            <button class="btn-primary" @click="handleCreate" data-testid="table-form-submit">생성</button>
          </div>
          <p v-if="formError" class="error">{{ formError }}</p>
        </div>
      </div>
    </div>

    <!-- Table Grid -->
    <div class="card-grid" data-testid="table-list">
      <div v-for="t in tables" :key="t.id" class="t-card" :data-testid="`table-card-${t.id}`">
        <div class="t-header">
          <span class="t-num">T{{ t.table_number }}</span>
          <span class="t-stats">{{ t.order_count }}건 · {{ t.total_amount.toLocaleString() }}원</span>
        </div>
        <div class="t-actions">
          <button class="btn-sm btn-outline" @click="viewDetail(t.id)" :data-testid="`table-detail-${t.id}`">상세</button>
          <button class="btn-sm btn-success" @click="completeTable(t.id)" :data-testid="`table-complete-${t.id}`">이용 완료</button>
          <button class="btn-sm btn-outline" @click="showPasswordChange(t.id)" :data-testid="`table-pw-${t.id}`">비밀번호</button>
          <button class="btn-sm btn-outline" @click="viewHistory(t.id)" :data-testid="`table-history-${t.id}`">내역</button>
        </div>
      </div>
      <div v-if="tables.length === 0" class="empty-state">등록된 테이블이 없습니다</div>
    </div>

    <!-- Detail Panel -->
    <div v-if="detail" class="modal-overlay" @click.self="detail = null">
      <div class="modal" data-testid="table-detail-panel">
        <div class="modal-top">
          <h2>테이블 {{ detail.table_number }} 주문</h2>
          <button class="btn-sm btn-outline" @click="detail = null" data-testid="close-detail">✕</button>
        </div>
        <div v-for="order in detail.orders" :key="order.id" class="detail-order">
          <span class="order-num">#{{ order.order_number }}</span>
          <span class="status-badge" :class="order.status">{{ order.status }}</span>
          <ul><li v-for="item in order.items" :key="item.id">{{ item.menu_name }} × {{ item.quantity }}</li></ul>
        </div>
        <p v-if="!detail.orders?.length" class="empty-msg">주문이 없습니다</p>
      </div>
    </div>

    <!-- Password Change -->
    <div v-if="pwChangeId" class="modal-overlay" @click.self="pwChangeId = null">
      <div class="modal">
        <h2>비밀번호 변경</h2>
        <div class="form-stack">
          <div class="form-group">
            <label>새 비밀번호</label>
            <input v-model="newPassword" type="password" data-testid="pw-change-input" />
          </div>
          <div class="form-actions">
            <button class="btn-outline" @click="pwChangeId = null" data-testid="pw-change-cancel">취소</button>
            <button class="btn-primary" @click="changePassword" data-testid="pw-change-submit">변경</button>
          </div>
        </div>
      </div>
    </div>

    <!-- History Panel -->
    <div v-if="history" class="modal-overlay" @click.self="history = null">
      <div class="modal wide" data-testid="history-panel">
        <div class="modal-top">
          <h2>과거 주문 내역</h2>
          <button class="btn-sm btn-outline" @click="history = null" data-testid="history-close">✕</button>
        </div>
        <div class="filter-row">
          <input v-model="historyFrom" type="date" data-testid="history-date-from" />
          <span>~</span>
          <input v-model="historyTo" type="date" data-testid="history-date-to" />
          <button class="btn-sm btn-primary" @click="filterHistory" data-testid="history-filter-btn">조회</button>
        </div>
        <div v-for="h in history" :key="h.id" class="history-item">
          <span class="order-num">#{{ h.order_number }}</span>
          <span>{{ h.total_amount.toLocaleString() }}원</span>
          <span class="status-badge" :class="h.status">{{ h.status }}</span>
        </div>
        <p v-if="history.length === 0" class="empty-msg">내역이 없습니다</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { tableService } from '@/services/table'

const tables = ref([])
const showForm = ref(false)
const form = ref({ tableNumber: 1, password: '' })
const formError = ref('')
const detail = ref(null)
const pwChangeId = ref(null)
const newPassword = ref('')
const history = ref(null)
const historyTableId = ref(null)
const historyFrom = ref('')
const historyTo = ref('')

async function loadTables() { tables.value = await tableService.getTables() }

async function handleCreate() {
  formError.value = ''
  try {
    await tableService.createTable(form.value.tableNumber, form.value.password)
    showForm.value = false
    form.value = { tableNumber: 1, password: '' }
    await loadTables()
  } catch (e) { formError.value = e.response?.data?.detail || '생성 실패' }
}

async function viewDetail(id) { detail.value = await tableService.getTableDetail(id) }

async function completeTable(id) {
  if (!confirm('이용 완료 처리하시겠습니까?')) return
  try { await tableService.completeTable(id); await loadTables() }
  catch (e) { alert(e.response?.data?.detail || '처리 실패') }
}

function showPasswordChange(id) { pwChangeId.value = id; newPassword.value = '' }

async function changePassword() {
  try { await tableService.updateTable(pwChangeId.value, newPassword.value); pwChangeId.value = null; alert('비밀번호가 변경되었습니다.') }
  catch (e) { alert(e.response?.data?.detail || '변경 실패') }
}

async function viewHistory(id) {
  historyTableId.value = id
  history.value = await tableService.getHistory(id)
}

async function filterHistory() {
  history.value = await tableService.getHistory(historyTableId.value, historyFrom.value || undefined, historyTo.value || undefined)
}

onMounted(loadTables)
</script>

<style scoped>
.page-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem}
.page-top h1{font-size:1.5rem}
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:.75rem}
.t-card{background:#fff;border-radius:var(--radius);padding:1rem;box-shadow:var(--shadow)}
.t-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:.75rem}
.t-num{font-size:1.2rem;font-weight:700;color:var(--primary)}
.t-stats{font-size:.85rem;color:var(--gray-500)}
.t-actions{display:flex;gap:.4rem;flex-wrap:wrap}
.empty-state{grid-column:1/-1;text-align:center;padding:2rem;color:var(--gray-500)}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;z-index:100}
.modal{background:#fff;border-radius:var(--radius);padding:1.5rem;width:100%;max-width:420px;box-shadow:var(--shadow-md)}
.modal.wide{max-width:560px}
.modal-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem}
.form-stack{display:flex;flex-direction:column;gap:.75rem}
.form-group{display:flex;flex-direction:column;gap:.25rem}
.form-group label{font-size:.8rem;font-weight:600;color:var(--gray-700)}
.form-actions{display:flex;gap:.75rem;justify-content:flex-end}
.filter-row{display:flex;align-items:center;gap:.5rem;margin-bottom:1rem}
.filter-row input{max-width:160px}
.detail-order,.history-item{padding:.5rem 0;border-bottom:1px solid var(--gray-100);display:flex;align-items:center;gap:.75rem;flex-wrap:wrap}
.detail-order ul{width:100%;list-style:none;font-size:.85rem;color:var(--gray-500)}
.order-num{font-weight:700}
.status-badge{font-size:.7rem;padding:.2rem .5rem;border-radius:10px;font-weight:600}
.status-badge.pending{background:#FEF3C7;color:#92400E}
.status-badge.preparing{background:#DBEAFE;color:#1E40AF}
.status-badge.completed{background:#D1FAE5;color:#065F46}
.empty-msg{text-align:center;color:var(--gray-500);padding:1rem}
</style>
