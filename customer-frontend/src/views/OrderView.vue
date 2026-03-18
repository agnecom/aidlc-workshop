<template>
  <div class="order-page">
    <header class="page-header">
      <button class="back-btn" @click="$router.push('/cart')">← 장바구니</button>
      <h1>주문 확인</h1>
      <span></span>
    </header>

    <div class="order-body">
      <!-- Gift Toggle -->
      <div class="gift-section">
        <button :class="['gift-toggle', { active: isGift }]" @click="toggleGift">
          🎁 다른 테이블에 선물하기
        </button>
        <div v-if="isGift" class="gift-form">
          <div class="gift-field">
            <label>받는 테이블</label>
            <select v-model="giftToTable">
              <option :value="null" disabled>테이블 선택</option>
              <option v-for="t in activeTables" :key="t.table_number" :value="t.table_number">
                테이블 {{ t.table_number }}
              </option>
            </select>
          </div>
          <div class="gift-field">
            <label>메시지 (선택)</label>
            <input v-model="giftMessage" placeholder="맛있게 드세요! 🎉" maxlength="200" />
          </div>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="summary-card" data-testid="order-summary">
        <div v-for="item in cart.items" :key="item.menu_item_id" class="summary-row">
          <span class="s-name">{{ item.name }}</span>
          <span class="s-qty">{{ item.quantity }}개</span>
          <span class="s-price">{{ (item.price * item.quantity).toLocaleString() }}원</span>
        </div>
        <div class="summary-total">
          <span>총 결제금액</span>
          <span class="total" data-testid="order-total">{{ cart.total.toLocaleString() }}원</span>
        </div>
        <p v-if="isGift && giftToTable" class="gift-note">
          🎁 테이블 {{ giftToTable }}번에 선물 · 결제는 내 테이블
        </p>
      </div>

      <button @click="confirmOrder" class="btn-primary confirm-btn"
        :disabled="submitting || (isGift && !giftToTable)" data-testid="order-confirm-btn">
        {{ submitting ? '주문 처리 중...' : isGift ? `🎁 ${cart.total.toLocaleString()}원 선물하기` : `${cart.total.toLocaleString()}원 주문하기` }}
      </button>
      <p v-if="error" class="error" data-testid="order-error">{{ error }}</p>
    </div>

    <!-- Success Overlay -->
    <Transition name="fade">
      <div v-if="success" class="overlay" data-testid="order-success">
        <div class="success-card">
          <div class="check-circle">{{ isGiftSuccess ? '🎁' : '✓' }}</div>
          <h2>{{ isGiftSuccess ? '선물 완료!' : '주문 완료!' }}</h2>
          <p class="order-num">주문번호 <strong>#{{ orderNumber }}</strong></p>
          <p v-if="isGiftSuccess" class="gift-msg">테이블 {{ giftToTable }}번에 선물을 보냈습니다</p>
          <p class="sub">잠시 후 메뉴 화면으로 이동합니다</p>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { orderService } from '@/services/order'

const cart = useCartStore()
const router = useRouter()
const submitting = ref(false)
const error = ref('')
const success = ref(false)
const orderNumber = ref(null)
const isGift = ref(false)
const isGiftSuccess = ref(false)
const giftToTable = ref(null)
const giftMessage = ref('')
const activeTables = ref([])

function toggleGift() {
  isGift.value = !isGift.value
  if (!isGift.value) { giftToTable.value = null; giftMessage.value = '' }
}

onMounted(async () => {
  try { activeTables.value = await orderService.getActiveTables() } catch {}
})

async function confirmOrder() {
  submitting.value = true
  error.value = ''
  try {
    const items = cart.items.map(i => ({ menu_item_id: i.menu_item_id, quantity: i.quantity }))
    const order = await orderService.createOrder(
      items,
      isGift.value ? giftToTable.value : null,
      isGift.value ? giftMessage.value : null,
    )
    isGiftSuccess.value = isGift.value
    success.value = true
    orderNumber.value = order.order_number
    cart.clearCart()
    setTimeout(() => router.push('/'), 2500)
  } catch (e) {
    error.value = e.response?.data?.detail || '주문에 실패했습니다. 다시 시도해 주세요.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.order-page{min-height:100vh;background:var(--bg);display:flex;flex-direction:column}
.page-header{display:flex;align-items:center;justify-content:space-between;padding:.75rem 1rem;background:var(--bg-surface);border-bottom:1px solid var(--border)}
.page-header h1{font-size:1.1rem;font-weight:700}
.back-btn{background:transparent;color:var(--text-sub);font-size:.9rem;padding:.3rem .5rem}
.order-body{flex:1;padding:1rem}

/* Gift Section */
.gift-section{margin-bottom:1rem}
.gift-toggle{width:100%;padding:.75rem;background:var(--bg-card);border:1.5px dashed var(--border-light);border-radius:var(--radius-sm);color:var(--text-sub);font-size:.9rem;text-align:center;transition:all .15s}
.gift-toggle.active{border-color:var(--accent);color:var(--accent);background:var(--accent-light)}
.gift-form{background:var(--bg-card);border-radius:0 0 var(--radius-sm) var(--radius-sm);padding:1rem;display:flex;flex-direction:column;gap:.75rem;border:1px solid var(--border);border-top:none}
.gift-field{display:flex;flex-direction:column;gap:.3rem}
.gift-field label{font-size:.8rem;color:var(--text-sub);font-weight:600}
.gift-field select{appearance:none;background:var(--bg-surface);padding:.6rem .8rem}
.gift-note{text-align:center;color:var(--accent);font-size:.85rem;margin-top:.75rem;font-weight:500}

/* Summary */
.summary-card{background:var(--bg-card);border-radius:var(--radius);padding:1rem;margin-bottom:1.5rem}
.summary-row{display:flex;align-items:center;padding:.55rem 0;border-bottom:1px solid var(--border)}
.summary-row:last-of-type{border-bottom:none}
.s-name{flex:1;font-weight:500}
.s-qty{color:var(--text-sub);font-size:.85rem;margin-right:1rem}
.s-price{font-weight:600;min-width:80px;text-align:right}
.summary-total{display:flex;justify-content:space-between;padding-top:.75rem;margin-top:.5rem;border-top:2px solid var(--border-light);font-size:1.1rem}
.total{font-weight:700;color:var(--accent);font-size:1.2rem}
.confirm-btn{width:100%;padding:.9rem;font-size:1.05rem;border-radius:var(--radius-sm)}

/* Overlay */
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center;z-index:200}
.success-card{background:var(--bg-card);border-radius:var(--radius);padding:2.5rem 2rem;text-align:center;box-shadow:var(--shadow-lg);min-width:280px}
.check-circle{width:60px;height:60px;border-radius:50%;background:var(--success);color:#fff;font-size:1.8rem;font-weight:700;display:flex;align-items:center;justify-content:center;margin:0 auto .75rem}
.success-card h2{margin-bottom:.4rem}
.order-num{font-size:1.1rem;margin-bottom:.3rem}
.gift-msg{color:var(--accent);font-size:.9rem;margin-bottom:.3rem}
.sub{color:var(--text-sub);font-size:.85rem}
.fade-enter-active,.fade-leave-active{transition:opacity .3s}
.fade-enter-from,.fade-leave-to{opacity:0}
</style>
