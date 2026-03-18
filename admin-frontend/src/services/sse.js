const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export class SSEClient {
  constructor() {
    this._es = null
    this._retries = 0
    this._maxRetries = 10
    this._handlers = {}
  }

  connect() {
    const token = localStorage.getItem('admin_token')
    this._es = new EventSource(`${API_BASE}/api/sse/admin?token=${token}`)
    this._es.addEventListener('new_order', (e) => this._dispatch(e))
    this._es.addEventListener('order_updated', (e) => this._dispatch(e))
    this._es.addEventListener('order_deleted', (e) => this._dispatch(e))
    this._es.onerror = () => this._reconnect()
    this._retries = 0
  }

  on(event, cb) { this._handlers[event] = cb }

  _dispatch(e) {
    const handler = this._handlers[e.type]
    if (handler) handler(JSON.parse(e.data))
  }

  _reconnect() {
    this.disconnect()
    if (this._retries < this._maxRetries) {
      this._retries++
      setTimeout(() => this.connect(), 3000)
    } else if (this._handlers['error']) {
      this._handlers['error']()
    }
  }

  disconnect() {
    if (this._es) { this._es.close(); this._es = null }
  }
}
