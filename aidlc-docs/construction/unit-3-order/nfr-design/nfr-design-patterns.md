# NFR Design - Unit 3 (주문 및 실시간 통신)

## SSE 패턴
- In-memory 연결 관리 (asyncio.Queue per client)
- 연결 키: "admin:{store_id}" 또는 "table:{table_id}"
- 브로드캐스트: store_id 기반 admin 전체 + table_id 기반 해당 테이블
- 연결 해제 시 큐 자동 정리
- 클라이언트: EventSource API + 자동 재연결 (3초, 최대 10회)

## 주문 검증 패턴
- Pydantic 스키마로 입력 검증 (items 최소 1개, quantity 1~99)
- 서비스 레이어에서 menu_item_id 존재 확인
- total_amount 서버 측 계산 (unit_price * quantity 합산)
- 상태 전이 검증: 허용된 전이만 수행 (pending→preparing→completed)

## 권한 분리
- POST /api/orders: get_current_table (고객)
- GET /api/orders: get_current_table (세션 필터) 또는 get_current_admin (매장 전체)
- PATCH /api/orders/{id}/status: get_current_admin
- DELETE /api/orders/{id}: get_current_admin
- GET /api/sse/orders: 인증 토큰 기반 (query param으로 token 전달)

## 장바구니 영속화
- Pinia store + localStorage watch
- 키: `cart_{table_id}` (테이블별 분리)
- 브라우저 새로고침 시 자동 복원
