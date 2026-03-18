# Unit 3 - Frontend Components

## Customer Frontend

### CartView
- 장바구니 항목 목록 (메뉴명, 수량 +-버튼, 단가, 소계)
- 총 금액 표시
- 주문하기 버튼 → OrderView로 이동
- 장바구니 비우기 버튼
- data-testid: cart-list, cart-item-{id}, cart-total, cart-order-btn, cart-clear-btn

### OrderView
- 주문 확인 화면 (장바구니 내용 요약)
- 주문 확정 버튼 → POST /api/orders
- 성공 시 장바구니 비우고 메뉴 화면으로 리다이렉트
- 실패 시 에러 메시지 + 장바구니 유지
- data-testid: order-confirm-btn, order-success, order-error

### OrderHistoryView
- 현재 세션 주문 목록 (시간 역순)
- 각 주문: 번호, 시각, 메뉴/수량, 금액, 상태 뱃지
- SSE로 상태 실시간 업데이트
- data-testid: order-history-list, order-item-{id}, order-status-{id}

### SSEClient (서비스)
- connect(tableId) → EventSource(/api/sse/orders?table_id={tableId})
- onmessage → 이벤트 타입별 콜백 실행
- onerror → 자동 재연결 (3초, 최대 10회)
- disconnect() → EventSource.close()

### CartStore (Pinia)
- state: items[], 
- getters: total, itemCount
- actions: addItem, removeItem, updateQuantity, clearCart
- localStorage 자동 동기화

## Admin Frontend

### DashboardView (확장)
- 테이블별 카드 그리드 (반응형)
- 각 카드: 테이블 번호, 총 주문액, 최신 주문 미리보기, 주문 수
- 카드 클릭 → 주문 상세 모달/패널
- 주문 상세: 메뉴 목록, 상태 변경 버튼 (pending→preparing→completed)
- 주문 삭제 버튼 (확인 팝업)
- SSE로 실시간 업데이트 (새 주문 시 카드 강조)
- data-testid: dashboard-grid, table-card-{id}, order-detail-{id}, status-btn-{status}

### SSEClient (서비스)
- connect(storeId) → EventSource(/api/sse/orders)
- 이벤트 핸들링: new_order, order_updated, order_deleted
- 자동 재연결 (3초, 최대 10회)
