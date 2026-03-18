const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const EVENT_TYPES = ['new_order', 'order_updated', 'order_deleted', 'gift_received', 'new_message', 'menu_recommendation']

export class SSEClient {
  constructor() {
    this._es = null
    this._retries = 0
    this._maxRetries = 10
    this._handlers = {}
  }

  connect(tableId) {
    const token = localStorage.getItem('table_token')
    this._es = new EventSource(`${API_BASE}/api/sse/table?token=${token}`)
    for (const type of EVENT_TYPES) {
      this._es.addEventListener(type, (e) => {
        const handler = this._handlers[type]
        if (handler) handler(JSON.parse(e.data))
      })
    }
    this._es.onerror = () => this._reconnect(tableId)
    this._retries = 0
  }

  on(event, cb) { this._handlers[event] = cb }

  _reconnect(tableId) {
    this.disconnect()
    if (this._retries < this._maxRetries) {
      this._retries++
      setTimeout(() => this.connect(tableId), 3000)
    } else if (this._handlers['error']) {
      this._handlers['error']()
    }
  }

  disconnect() {
    if (this._es) { this._es.close(); this._es = null }
  }
}
