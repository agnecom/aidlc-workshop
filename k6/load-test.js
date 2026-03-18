import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const BASE = 'http://localhost:8000';

// Custom metrics
const orderRate = new Rate('order_success');
const loginTrend = new Trend('login_duration');
const menuTrend = new Trend('menu_duration');
const orderTrend = new Trend('order_duration');

export const options = {
  scenarios: {
    customer_flow: {
      executor: 'ramping-vus',
      startVUs: 1,
      stages: [
        { duration: '10s', target: 10 },
        { duration: '30s', target: 10 },
        { duration: '10s', target: 30 },
        { duration: '30s', target: 30 },
        { duration: '10s', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.05'],
    order_success: ['rate>0.9'],
  },
};

const HEADERS = { 'Content-Type': 'application/json' };

export default function () {
  const tableNum = ((__VU % 3) + 1);

  // 1. Login
  let res = http.post(`${BASE}/api/auth/table/login`, JSON.stringify({
    store_id: 'store001', table_number: tableNum, password: '1234',
  }), { headers: HEADERS, tags: { name: 'login' } });
  loginTrend.add(res.timings.duration);

  if (!check(res, { 'login 200': (r) => r.status === 200 })) return;
  const token = res.json('access_token');
  const auth = { headers: { ...HEADERS, Authorization: `Bearer ${token}` } };

  sleep(0.5);

  // 2. Get categories
  res = http.get(`${BASE}/api/categories`, { headers: auth.headers, tags: { name: 'categories' } });
  check(res, { 'categories 200': (r) => r.status === 200 });

  // 3. Get menus
  res = http.get(`${BASE}/api/menus`, { headers: auth.headers, tags: { name: 'menus' } });
  menuTrend.add(res.timings.duration);
  check(res, { 'menus 200': (r) => r.status === 200 });

  const menus = res.json();
  if (!menus || menus.length === 0) return;

  sleep(1);

  // 4. Create order (random 1~3 items)
  const count = Math.floor(Math.random() * 3) + 1;
  const items = [];
  const used = new Set();
  for (let i = 0; i < count && i < menus.length; i++) {
    let idx = Math.floor(Math.random() * menus.length);
    while (used.has(idx)) idx = (idx + 1) % menus.length;
    used.add(idx);
    items.push({ menu_item_id: menus[idx].id, quantity: Math.floor(Math.random() * 3) + 1 });
  }

  res = http.post(`${BASE}/api/orders`, JSON.stringify({ items }), {
    headers: auth.headers, tags: { name: 'create_order' },
  });
  orderTrend.add(res.timings.duration);
  orderRate.add(res.status === 201);
  check(res, { 'order 201': (r) => r.status === 201 });

  sleep(0.5);

  // 5. Get order history
  res = http.get(`${BASE}/api/orders`, { headers: auth.headers, tags: { name: 'order_history' } });
  check(res, { 'orders 200': (r) => r.status === 200 });

  sleep(1);
}
