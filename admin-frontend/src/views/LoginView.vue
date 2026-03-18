<template>
  <div class="login-page">
    <div class="login-card">
      <div class="logo">🏪</div>
      <h1>관리자 로그인</h1>
      <form @submit.prevent="handleLogin" data-testid="login-form">
        <div class="form-group">
          <label for="storeIdentifier">매장 식별자</label>
          <input id="storeIdentifier" v-model="storeIdentifier" placeholder="store001" required data-testid="login-store-identifier" />
        </div>
        <div class="form-group">
          <label for="username">사용자명</label>
          <input id="username" v-model="username" placeholder="admin" required data-testid="login-username" />
        </div>
        <div class="form-group">
          <label for="password">비밀번호</label>
          <input id="password" v-model="password" type="password" required data-testid="login-password" />
        </div>
        <button type="submit" class="btn-primary btn-full" :disabled="loading" data-testid="login-submit-button">
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>
        <p v-if="error" class="error" data-testid="login-error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '@/services/auth'

const router = useRouter()
const storeIdentifier = ref('')
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await authService.login(storeIdentifier.value, username.value, password.value)
    router.push({ name: 'dashboard' })
  } catch (e) {
    const status = e.response?.status
    if (status === 401) error.value = '매장 식별자, 사용자명 또는 비밀번호가 올바르지 않습니다.'
    else if (status === 423) error.value = '계정이 잠겼습니다. 잠시 후 다시 시도해 주세요.'
    else error.value = '서버에 연결할 수 없습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page{min-height:100vh;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--primary-light),#fff)}
.login-card{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow-md);padding:2.5rem 2rem;width:100%;max-width:400px;text-align:center}
.logo{font-size:3rem;margin-bottom:.5rem}
h1{font-size:1.4rem;margin-bottom:1.5rem;color:var(--gray-900)}
.form-group{text-align:left;margin-bottom:1rem}
.form-group label{display:block;font-size:.85rem;font-weight:600;color:var(--gray-700);margin-bottom:.3rem}
.btn-full{width:100%;padding:.75rem;font-size:1rem;margin-top:.5rem}
</style>
