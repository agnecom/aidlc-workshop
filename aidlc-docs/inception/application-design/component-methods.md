# Component Methods

## Backend API

### AUTH Router

| Method | Endpoint | Input | Output | 설명 |
|--------|----------|-------|--------|------|
| POST | `/api/auth/admin/login` | `{store_id, username, password}` | `{access_token, token_type}` | 관리자 로그인 |
| POST | `/api/auth/table/login` | `{store_id, table_number, password}` | `{access_token, token_type, session_id}` | 테이블 태블릿 로그인 |

### MENU Router

| Method | Endpoint | Input | Output | 설명 |
|--------|----------|-------|--------|------|
| GET | `/api/categories` | - | `Category[]` | 카테고리 목록 조회 |
| GET | `/api/menus` | `?category_id` | `MenuItem[]` | 메뉴 목록 조회 |
| GET | `/api/menus/{id}` | - | `MenuItem` | 메뉴 상세 조회 |
| POST | `/api/menus` | `MenuCreate + image file` | `MenuItem` | 메뉴 등록 (관리자) |
| PUT | `/api/menus/{id}` | `MenuUpdate + image file` | `MenuItem` | 메뉴 수정 (관리자) |
| DELETE | `/api/menus/{id}` | - | `204` | 메뉴 삭제 (관리자) |
| PATCH | `/api/menus/{id}/order` | `{display_order}` | `MenuItem` | 노출 순서 변경 (관리자) |

### ORDER Router

| Method | Endpoint | Input | Output | 설명 |
|--------|----------|-------|--------|------|
| POST | `/api/orders` | `OrderCreate` | `Order` | 주문 생성 (고객) |
| GET | `/api/orders` | `?table_id&session_id` | `Order[]` | 주문 목록 조회 |
| GET | `/api/orders/{id}` | - | `Order` | 주문 상세 조회 |
| PATCH | `/api/orders/{id}/status` | `{status}` | `Order` | 주문 상태 변경 (관리자) |
| DELETE | `/api/orders/{id}` | - | `204` | 주문 삭제 (관리자) |

### TABLE Router

| Method | Endpoint | Input | Output | 설명 |
|--------|----------|-------|--------|------|
| POST | `/api/tables` | `TableCreate` | `Table` | 테이블 생성/설정 (관리자) |
| GET | `/api/tables` | - | `Table[]` | 테이블 목록 조회 (관리자) |
| GET | `/api/tables/{id}` | - | `TableDetail` | 테이블 상세 (주문 포함) |
| POST | `/api/tables/{id}/complete` | - | `204` | 이용 완료 처리 (관리자) |
| GET | `/api/tables/{id}/history` | `?date_from&date_to` | `OrderHistory[]` | 과거 주문 내역 (관리자) |

### SSE Router

| Method | Endpoint | Input | Output | 설명 |
|--------|----------|-------|--------|------|
| GET | `/api/sse/orders` | `?table_id` | `EventStream` | 주문 이벤트 스트림 (고객/관리자) |

---

## Customer Frontend

### AuthGuard
- `autoLogin()`: 저장된 인증 정보로 자동 로그인
- `checkSession()`: 세션 유효성 확인

### CartStore (Pinia)
- `addItem(menuItem, quantity)`: 장바구니 추가
- `removeItem(menuItemId)`: 장바구니 삭제
- `updateQuantity(menuItemId, quantity)`: 수량 변경
- `clearCart()`: 장바구니 비우기
- `getTotal()`: 총 금액 계산
- `persistToStorage()`: localStorage 저장
- `loadFromStorage()`: localStorage 복원

### SSEClient
- `connect(tableId)`: SSE 연결
- `onOrderUpdate(callback)`: 주문 상태 변경 이벤트 핸들러
- `reconnect()`: 자동 재연결

---

## Admin Frontend

### AuthGuard
- `login(storeId, username, password)`: 관리자 로그인
- `checkSession()`: JWT 세션 확인
- `logout()`: 로그아웃

### SSEClient
- `connect()`: SSE 연결 (전체 매장 주문)
- `onNewOrder(callback)`: 신규 주문 이벤트 핸들러
- `onOrderUpdate(callback)`: 주문 상태 변경 이벤트 핸들러
- `reconnect()`: 자동 재연결
