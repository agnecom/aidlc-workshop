<template>
  <div class="chat-page">
    <header class="page-header">
      <button class="back-btn" @click="$router.push('/')">← 메뉴</button>
      <h1 v-if="!chatTarget">메시지</h1>
      <h1 v-else>테이블 {{ chatTarget }}번</h1>
      <span></span>
    </header>

    <!-- Table List -->
    <div v-if="!chatTarget" class="table-list">
      <div v-for="t in tables" :key="t.table_number" class="table-item" @click="openChat(t.table_number)">
        <div class="table-avatar">T{{ t.table_number }}</div>
        <span class="table-label">테이블 {{ t.table_number }}번</span>
        <span v-if="unread[t.table_number]" class="unread-dot"></span>
        <span class="arrow">›</span>
      </div>
      <div v-if="tables.length === 0" class="empty">
        <p>다른 활성 테이블이 없습니다</p>
      </div>
    </div>

    <!-- Chat Room -->
    <div v-else class="chat-room">
      <div class="messages" ref="messagesEl">
        <div v-for="msg in messages" :key="msg.id" :class="['msg', msg.is_mine ? 'mine' : 'theirs']">
          <div class="bubble">{{ msg.message }}</div>
          <span class="time">{{ formatTime(msg.created_at) }}</span>
        </div>
        <div v-if="messages.length === 0" class="empty-chat">
          <p>첫 메시지를 보내보세요! 👋</p>
        </div>
      </div>
      <form class="input-bar" @submit.prevent="sendMessage">
        <input v-model="newMsg" placeholder="메시지 입력..." maxlength="300" autofocus />
        <button type="submit" class="send-btn" :disabled="!newMsg.trim()">전송</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { messageService } from '@/services/message'

const route = useRoute()
const router = useRouter()
const tables = ref([])
const chatTarget = ref(null)
const messages = ref([])
const newMsg = ref('')
const messagesEl = ref(null)
const unread = ref({})
const myTableId = localStorage.getItem('table_id')

function formatTime(dt) {
  const d = new Date(dt)
  return d.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
}

async function loadTables() {
  tables.value = await messageService.getActiveTables()
}

async function openChat(tableNumber) {
  chatTarget.value = tableNumber
  router.replace({ query: { t: tableNumber } })
  unread.value[tableNumber] = false
  messages.value = await messageService.getMessages(tableNumber)
  await nextTick()
  scrollBottom()
}

function scrollBottom() {
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

async function sendMessage() {
  if (!newMsg.value.trim() || !chatTarget.value) return
  const text = newMsg.value.trim()
  newMsg.value = ''
  await messageService.send(chatTarget.value, text)
  messages.value = await messageService.getMessages(chatTarget.value)
  await nextTick()
  scrollBottom()
}

onMounted(async () => {
  await loadTables()
  if (route.query.t) openChat(Number(route.query.t))

  const handler = async (e) => {
    const data = e.detail
    if (chatTarget.value && (data.from_table_number === chatTarget.value || data.to_table_number === chatTarget.value)) {
      messages.value = await messageService.getMessages(chatTarget.value)
      await nextTick()
      scrollBottom()
    } else if (data.from_table_number) {
      unread.value[data.from_table_number] = true
    }
  }
  window.addEventListener('sse:new_message', handler)
  onUnmounted(() => window.removeEventListener('sse:new_message', handler))
})

watch(() => route.query.t, (val) => {
  if (!val) chatTarget.value = null
})
</script>

<style scoped>
.chat-page{display:flex;flex-direction:column;height:100vh;height:100dvh;background:var(--bg)}
.page-header{display:flex;align-items:center;justify-content:space-between;padding:.75rem 1rem;background:var(--bg-surface);border-bottom:1px solid var(--border)}
.page-header h1{font-size:1.1rem;font-weight:700}
.back-btn{background:transparent;color:var(--text-sub);font-size:.9rem;padding:.3rem .5rem}

/* Table List */
.table-list{flex:1;overflow-y:auto;padding:.5rem}
.table-item{display:flex;align-items:center;gap:.75rem;padding:.85rem 1rem;background:var(--bg-card);border-radius:var(--radius-sm);margin-bottom:.4rem;cursor:pointer;transition:background .12s}
.table-item:hover{background:var(--bg-card-hover)}
.table-avatar{width:40px;height:40px;border-radius:50%;background:var(--accent);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.85rem;flex-shrink:0}
.table-label{flex:1;font-weight:500}
.unread-dot{width:10px;height:10px;border-radius:50%;background:var(--accent)}
.arrow{color:var(--text-dim);font-size:1.2rem}
.empty{flex:1;display:flex;align-items:center;justify-content:center;color:var(--text-sub)}

/* Chat Room */
.chat-room{flex:1;display:flex;flex-direction:column;overflow:hidden}
.messages{flex:1;overflow-y:auto;padding:1rem;display:flex;flex-direction:column;gap:.4rem}
.msg{display:flex;flex-direction:column;max-width:75%}
.msg.mine{align-self:flex-end;align-items:flex-end}
.msg.theirs{align-self:flex-start;align-items:flex-start}
.bubble{padding:.55rem .85rem;border-radius:16px;font-size:.9rem;line-height:1.4;word-break:break-word}
.mine .bubble{background:var(--accent);color:#fff;border-bottom-right-radius:4px}
.theirs .bubble{background:var(--bg-card);color:var(--text);border-bottom-left-radius:4px}
.time{font-size:.65rem;color:var(--text-dim);margin-top:.15rem;padding:0 .3rem}
.empty-chat{flex:1;display:flex;align-items:center;justify-content:center;color:var(--text-dim)}

/* Input Bar */
.input-bar{display:flex;gap:.5rem;padding:.6rem .8rem;background:var(--bg-surface);border-top:1px solid var(--border)}
.input-bar input{flex:1;background:var(--bg-card);border:1px solid var(--border);border-radius:20px;padding:.55rem 1rem}
.send-btn{background:var(--accent);color:#fff;border-radius:20px;padding:.55rem 1.2rem;font-weight:600;font-size:.9rem}
.send-btn:disabled{opacity:.3}
</style>
