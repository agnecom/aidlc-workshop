<template>
  <div class="cart-page">
    <header class="page-header">
      <button class="back-btn" @click="$router.push('/')">← 메뉴</button>
      <h1>장바구니</h1>
      <span></span>
    </header>

    <div v-if="cart.items.length === 0" class="empty" data-testid="cart-empty">
      <span class="empty-icon">🛒</span>
      <p>장바구니가 비어있습니다</p>
      <router-link to="/" class="btn-primary" style="display:inline-block;margin-top:1rem">메뉴 보기</router-link>
    </div>

    <ul v-else class="cart-list" data-testid="cart-list">
      <li v-for="item in cart.items" :key="item.menu_item_id" class="cart-item" :data-testid="`cart-item-${item.menu_item_id}`">
        <div class="item-top">
          <span class="item-name">{{ item.name }}</span>
          <button class="remove-btn" @click="cart.removeItem(item.menu_item_id)" data-testid="cart-remove">✕</button>
        </div>
        <div class="item-bottom">
          <div class="qty-control">
            <button class="qty-btn" @click="cart.updateQuantity(item.menu_item_id, item.quantity - 1)" data-testid="cart-qty-minus">−</button>
            <span class="qty" data-testid="cart-qty">{{ item.quantity }}</span>
            <button class="qty-btn" @click="cart.updateQuantity(item.menu_item_id, item.quantity + 1)" data-testid="cart-qty-plus">+</button>
          </div>
          <span class="item-price">{{ (item.price * item.quantity).toLocaleString() }}원</span>
        </div>
      </li>
    </ul>

    <div v-if="cart.items.length" class="cart-footer">
      <div class="total-row">
        <span>총 주문금액</span>
        <span class="total-price" data-testid="cart-total">{{ cart.total.toLocaleString() }}원</span>
      </div>
      <div class="footer-btns">
        <button class="btn-outline" @click="cart.clearCart()" data-testid="cart-clear-btn">전체 삭제</button>
        <router-link to="/order" class="btn-primary order-btn" data-testid="cart-order-btn">주문하기</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
const cart = useCartStore()
</script>

<style scoped>
.cart-page{min-height:100vh;background:var(--bg);display:flex;flex-direction:column}
.page-header{display:flex;align-items:center;justify-content:space-between;padding:.75rem 1rem;background:var(--bg-surface);border-bottom:1px solid var(--border)}
.page-header h1{font-size:1.1rem;font-weight:700}
.back-btn{background:transparent;color:var(--text-sub);font-size:.9rem;padding:.3rem .5rem}
.empty{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--text-sub)}
.empty-icon{font-size:3rem;margin-bottom:.5rem}
.cart-list{list-style:none;padding:1rem;flex:1;overflow-y:auto}
.cart-item{background:var(--bg-card);border-radius:var(--radius-sm);padding:1rem;margin-bottom:.6rem}
.item-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem}
.item-name{font-weight:600;font-size:.95rem}
.remove-btn{background:transparent;color:var(--text-dim);font-size:.9rem;padding:.2rem .4rem}
.remove-btn:hover{color:#EF4444}
.item-bottom{display:flex;align-items:center;justify-content:space-between}
.qty-control{display:flex;align-items:center;gap:.5rem;background:var(--bg-surface);border-radius:var(--radius-xs);padding:.2rem}
.qty-btn{width:32px;height:32px;border-radius:var(--radius-xs);background:var(--border);color:var(--text);font-size:1.1rem;display:flex;align-items:center;justify-content:center;font-weight:700;padding:0}
.qty-btn:hover{background:var(--border-light)}
.qty{min-width:28px;text-align:center;font-weight:700;font-size:.95rem}
.item-price{font-weight:700;color:var(--accent);font-size:1rem}
.cart-footer{background:var(--bg-surface);border-top:1px solid var(--border);padding:1rem}
.total-row{display:flex;justify-content:space-between;margin-bottom:.75rem;font-size:1rem}
.total-price{font-weight:700;color:var(--accent);font-size:1.2rem}
.footer-btns{display:flex;gap:.6rem}
.footer-btns .btn-outline{flex:1;text-align:center}
.order-btn{flex:2;text-align:center;padding:.75rem;font-weight:700;border-radius:var(--radius-sm);text-decoration:none;font-size:1rem}
</style>
