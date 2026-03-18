import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE = 'http://localhost:8000';
const H = { 'Content-Type': 'application/json' };

export const options = {
  vus: 5,
  iterations: 15,
};

export default function () {
  const tNum = (__VU % 3) + 1;

  // --- Health ---
  check(http.get(`${BASE}/health`), { 'health': r => r.status === 200 });

  // --- Admin login ---
  let res = http.post(`${BASE}/api/auth/admin/login`, JSON.stringify({
    store_identifier: 'store001', username: 'admin', password: 'admin1234',
  }), { headers: H });
  check(res, { 'admin login': r => r.status === 200 });
  const adminToken = res.json('access_token');
  const AH = { ...H, Authorization: `Bearer ${adminToken}` };

  // --- Table login ---
  res = http.post(`${BASE}/api/auth/table/login`, JSON.stringify({
    store_id: 'store001', table_number: tNum, password: '1234',
  }), { headers: H });
  check(res, { 'table login': r => r.status === 200 });
  const tableToken = res.json('access_token');
  const TH = { ...H, Authorization: `Bearer ${tableToken}` };

  // --- Categories ---
  res = http.get(`${BASE}/api/categories`, { headers: TH });
  check(res, { 'categories': r => r.status === 200 });

  // --- Menus (customer) ---
  res = http.get(`${BASE}/api/menus`, { headers: TH });
  check(res, { 'menus': r => r.status === 200 });
  const menus = res.json();

  // --- Tables (admin) ---
  res = http.get(`${BASE}/api/tables`, { headers: AH });
  check(res, { 'tables admin': r => r.status === 200 });

  // --- Active tables (customer) ---
  res = http.get(`${BASE}/api/tables/list/active`, { headers: TH });
  check(res, { 'active tables': r => r.status === 200 });

  // --- Create order ---
  if (menus && menus.length >= 2) {
    const i1 = Math.floor(Math.random() * menus.length);
    let i2 = (i1 + 1) % menus.length;
    res = http.post(`${BASE}/api/orders`, JSON.stringify({
      items: [
        { menu_item_id: menus[i1].id, quantity: 2 },
        { menu_item_id: menus[i2].id, quantity: 1 },
      ],
    }), { headers: TH });
    check(res, { 'create order': r => r.status === 201 });
    const orderId = res.json('id');

    // --- Get orders (customer) ---
    res = http.get(`${BASE}/api/orders`, { headers: TH });
    check(res, { 'get orders': r => r.status === 200 });

    // --- Get orders (admin) ---
    res = http.get(`${BASE}/api/orders/admin`, { headers: AH });
    check(res, { 'orders admin': r => r.status === 200 });

    // --- Update status: preparing ---
    if (orderId) {
      res = http.patch(`${BASE}/api/orders/${orderId}/status`,
        JSON.stringify({ status: 'preparing' }), { headers: AH });
      check(res, { 'status preparing': r => r.status === 200 });

      // --- Update status: completed (triggers recommendation) ---
      res = http.patch(`${BASE}/api/orders/${orderId}/status`,
        JSON.stringify({ status: 'completed' }), { headers: AH });
      check(res, { 'status completed': r => r.status === 200 });
    }
  }

  // --- Send message ---
  const toTable = tNum === 1 ? 2 : 1;
  res = http.post(`${BASE}/api/messages`, JSON.stringify({
    to_table_number: toTable, message: `k6 테스트 메시지 from table ${tNum}`,
  }), { headers: TH });
  check(res, { 'send message': r => r.status === 200 || r.status === 201 });

  // --- Get messages ---
  res = http.get(`${BASE}/api/messages/${toTable}`, { headers: TH });
  check(res, { 'get messages': r => r.status === 200 });

  sleep(0.5);
}
