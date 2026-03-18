<template>
  <div class="setup-page">
    <div class="setup-card">
      <div class="brand">
        <span class="brand-icon">🍽</span>
        <h1>테이블오더</h1>
      </div>
      <p class="subtitle">테이블 정보를 입력해주세요</p>
      <form @submit.prevent="handleSetup" data-testid="setup-form">
        <div class="field">
          <label for="storeId">매장 코드</label>
          <input id="storeId" v-model="storeId" placeholder="store001" required data-testid="setup-store-id" />
        </div>
        <div class="field">
          <label for="tableNumber">테이블 번호</label>
          <input id="tableNumber" v-model.number="tableNumber" type="number" min="1" required data-testid="setup-table-number" />
        </div>
        <div class="field">
          <label for="password">비밀번호</label>
          <input id="password" v-model="password" type="password" placeholder="••••" required data-testid="setup-password" />
        </div>
        <button type="submit" class="btn-primary btn-full" :disabled="loading" data-testid="setup-submit-button">
          {{ loading ? '연결 중...' : '주문 시작하기' }}
        </button>
        <p v-if="error" class="error" data-testid="setup-error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '@/services/auth'

const router = useRouter()
const storeId = ref('')
const tableNumber = ref(1)
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleSetup() {
  loading.value = true
  error.value = ''
  try {
    await authService.login(storeId.value, tableNumber.value, password.value)
    authService.saveCredentials(storeId.value, tableNumber.value, password.value)
    router.push({ name: 'menu' })
  } catch (e) {
    error.value = e.response?.status === 401
      ? '인증 정보가 올바르지 않습니다.'
      : '서버에 연결할 수 없습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.setup-page{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:1.5rem;background:var(--bg)}
.setup-card{background:var(--bg-card);border-radius:var(--radius);padding:2.5rem 2rem;width:100%;max-width:380px;box-shadow:var(--shadow-lg)}
.brand{text-align:center;margin-bottom:.25rem}
.brand-icon{font-size:2.5rem;display:block;margin-bottom:.3rem}
.brand h1{font-size:1.4rem;font-weight:700}
.subtitle{text-align:center;color:var(--text-sub);font-size:.85rem;margin-bottom:1.5rem}
.field{margin-bottom:1rem}
.field label{display:block;font-size:.8rem;font-weight:600;color:var(--text-sub);margin-bottom:.3rem;text-transform:uppercase;letter-spacing:.5px}
.btn-full{width:100%;padding:.8rem;font-size:1rem;margin-top:.5rem;border-radius:var(--radius-sm)}
</style>
