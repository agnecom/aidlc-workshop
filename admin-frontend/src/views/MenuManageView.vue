<template>
  <div class="menu-manage">
    <div class="page-top">
      <h1>메뉴 관리</h1>
      <button class="btn-primary" @click="showForm = true" data-testid="menu-add-button">+ 메뉴 등록</button>
    </div>

    <!-- Form Modal -->
    <div v-if="showForm" class="modal-overlay" @click.self="resetForm">
      <div class="modal" data-testid="menu-form">
        <h2>{{ editingId ? '메뉴 수정' : '메뉴 등록' }}</h2>
        <form @submit.prevent="handleSubmit" class="form-grid">
          <div class="form-group">
            <label>메뉴명</label>
            <input v-model="form.name" required data-testid="menu-form-name" />
          </div>
          <div class="form-group">
            <label>가격</label>
            <input v-model.number="form.price" type="number" min="0" required data-testid="menu-form-price" />
          </div>
          <div class="form-group full">
            <label>설명</label>
            <textarea v-model="form.description" rows="2" data-testid="menu-form-description"></textarea>
          </div>
          <div class="form-group">
            <label>카테고리</label>
            <select v-model="form.category_id" required data-testid="menu-form-category">
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>순서</label>
            <input v-model.number="form.display_order" type="number" min="0" data-testid="menu-form-order" />
          </div>
          <div class="form-group full">
            <label>이미지</label>
            <input type="file" @change="onFileChange" accept="image/*" data-testid="menu-form-image" />
          </div>
          <div class="form-actions full">
            <button type="button" class="btn-outline" @click="resetForm" data-testid="menu-form-cancel">취소</button>
            <button type="submit" class="btn-primary" data-testid="menu-form-submit">{{ editingId ? '수정' : '등록' }}</button>
          </div>
          <p v-if="formError" class="error full">{{ formError }}</p>
        </form>
      </div>
    </div>

    <!-- Table -->
    <div class="table-wrap">
      <table data-testid="menu-table">
        <thead><tr><th>메뉴명</th><th>가격</th><th>카테고리</th><th>순서</th><th>작업</th></tr></thead>
        <tbody>
          <tr v-for="item in menus" :key="item.id" :data-testid="`menu-row-${item.id}`">
            <td class="name-cell">{{ item.name }}</td>
            <td>{{ item.price.toLocaleString() }}원</td>
            <td>{{ getCategoryName(item.category_id) }}</td>
            <td>{{ item.display_order }}</td>
            <td class="action-cell">
              <button class="btn-sm btn-outline" @click="editMenu(item)" :data-testid="`menu-edit-${item.id}`">수정</button>
              <button class="btn-sm btn-danger" @click="confirmDelete(item.id)" :data-testid="`menu-delete-${item.id}`">삭제</button>
            </td>
          </tr>
          <tr v-if="menus.length === 0"><td colspan="5" class="empty-row">등록된 메뉴가 없습니다</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { menuService } from '@/services/menu'

const categories = ref([])
const menus = ref([])
const showForm = ref(false)
const editingId = ref(null)
const formError = ref('')
const imageFile = ref(null)
const form = ref({ name: '', price: 0, description: '', category_id: '', display_order: 0 })

function resetForm() {
  form.value = { name: '', price: 0, description: '', category_id: '', display_order: 0 }
  editingId.value = null
  imageFile.value = null
  showForm.value = false
  formError.value = ''
}

function getCategoryName(id) {
  return categories.value.find(c => c.id === id)?.name || ''
}

function onFileChange(e) { imageFile.value = e.target.files[0] }

function editMenu(item) {
  form.value = { name: item.name, price: item.price, description: item.description || '', category_id: item.category_id, display_order: item.display_order }
  editingId.value = item.id
  showForm.value = true
}

async function handleSubmit() {
  formError.value = ''
  const fd = new FormData()
  fd.append('name', form.value.name)
  fd.append('price', form.value.price)
  fd.append('description', form.value.description)
  fd.append('category_id', form.value.category_id)
  fd.append('display_order', form.value.display_order)
  if (imageFile.value) fd.append('image', imageFile.value)
  try {
    if (editingId.value) await menuService.updateMenu(editingId.value, fd)
    else await menuService.createMenu(fd)
    resetForm()
    await loadMenus()
  } catch (e) {
    formError.value = e.response?.data?.detail || '저장에 실패했습니다.'
  }
}

async function confirmDelete(id) {
  if (!confirm('이 메뉴를 삭제하시겠습니까?')) return
  try {
    await menuService.deleteMenu(id)
    await loadMenus()
  } catch { formError.value = '삭제에 실패했습니다.' }
}

async function loadMenus() {
  menus.value = await menuService.getMenus()
}

onMounted(async () => {
  categories.value = await menuService.getCategories()
  await loadMenus()
})
</script>

<style scoped>
.page-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem}
.page-top h1{font-size:1.5rem}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;z-index:100}
.modal{background:#fff;border-radius:var(--radius);padding:1.5rem;width:100%;max-width:500px;box-shadow:var(--shadow-md)}
.modal h2{font-size:1.15rem;margin-bottom:1rem}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:.75rem}
.form-group{display:flex;flex-direction:column;gap:.25rem}
.form-group label{font-size:.8rem;font-weight:600;color:var(--gray-700)}
.form-group.full,.form-actions.full,.error.full{grid-column:1/-1}
.form-actions{display:flex;gap:.75rem;justify-content:flex-end;margin-top:.5rem}
.table-wrap{background:#fff;border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow)}
table{width:100%;border-collapse:collapse}
th{background:var(--gray-50);text-align:left;padding:.65rem 1rem;font-size:.8rem;color:var(--gray-500);font-weight:600;text-transform:uppercase;border-bottom:1px solid var(--gray-200)}
td{padding:.65rem 1rem;border-bottom:1px solid var(--gray-100);font-size:.9rem}
.name-cell{font-weight:600}
.action-cell{display:flex;gap:.4rem}
.empty-row{text-align:center;color:var(--gray-500);padding:2rem}
</style>
