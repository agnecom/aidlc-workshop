# Unit 3 - Business Logic Model

## 1. 주문 생성 플로우

```
Customer CartView → POST /api/orders → OrderService.create()
  1. 장바구니 항목 검증 (빈 장바구니 거부)
  2. 메뉴 존재 여부 확인 (menu_item_id 유효성)
  3. order_number 생성 (store_id 기준 max+1)
  4. total_amount 계산 (서버 측 가격 기준)
  5. Order + OrderItem 생성
  6. SSEManager.broadcast("new_order", order_data)
  7. return Order
```

## 2. 주문 상태 전이 플로우

```
Admin Dashboard → PATCH /api/orders/{id}/status → OrderService.update_status()
  1. 주문 존재 확인
  2. 상태 전이 유효성 검증 (pending→preparing→completed만 허용)
  3. status 업데이트
  4. SSEManager.broadcast("order_updated", order_data)
  5. return Order
```

## 3. 주문 삭제 플로우

```
Admin Dashboard → DELETE /api/orders/{id} → OrderService.delete()
  1. 주문 존재 확인
  2. Order + OrderItem cascade 삭제
  3. SSEManager.broadcast("order_deleted", {order_id, table_id})
```

## 4. SSE 이벤트 관리

```
SSEManager (싱글톤)
  - connections: dict[str, list[Queue]]  # key: "admin:{store_id}" 또는 "table:{table_id}"
  - connect(client_type, id) → Queue
  - disconnect(client_type, id, queue)
  - broadcast(event_type, data, store_id, table_id)
    → admin:{store_id} 연결에 전송
    → table:{table_id} 연결에 전송
```

### SSE 이벤트 타입

| 이벤트 | 데이터 | 수신자 |
|--------|--------|--------|
| new_order | Order (items 포함) | admin, 해당 table |
| order_updated | Order (status 변경) | admin, 해당 table |
| order_deleted | {order_id, table_id} | admin, 해당 table |

## 5. 장바구니 (Client-Side Only)

```
CartStore (Pinia + localStorage)
  - items: [{menu_item_id, name, price, quantity, image_url}]
  - addItem(menuItem, qty=1)
  - removeItem(menuItemId)
  - updateQuantity(menuItemId, qty)  # 1~99 범위
  - clearCart()
  - total: computed (sum of price * quantity)
  - persist: watch → localStorage
  - restore: onMounted → localStorage
```

## 6. 주문 조회

- 고객: GET /api/orders?session_id={session_id} → 현재 세션 주문만
- 관리자: GET /api/orders?table_id={table_id} → 테이블별 활성 주문
