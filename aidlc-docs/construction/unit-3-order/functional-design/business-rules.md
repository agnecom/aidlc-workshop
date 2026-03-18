# Unit 3 - Business Rules

## BR-01: 주문 생성 검증
- 장바구니가 비어있으면 주문 거부 (400)
- 모든 menu_item_id가 해당 store_id에 존재해야 함 (404)
- total_amount는 서버에서 재계산 (클라이언트 값 무시)

## BR-02: 주문 번호 생성
- store_id 기준 max(order_number) + 1
- 첫 주문은 1번

## BR-03: 주문 상태 전이
- 허용 전이: pending → preparing → completed
- 역방향 전이 불가 (400)
- 동일 상태 전이 불가 (400)

## BR-04: 주문 삭제
- 관리자만 삭제 가능
- 모든 상태의 주문 삭제 가능
- cascade로 OrderItem도 삭제

## BR-05: 장바구니 수량
- 최소 1, 최대 99
- 0 이하 시 항목 자동 제거

## BR-06: SSE 연결 관리
- 연결 끊김 시 클라이언트 자동 재연결 (3초 간격, 최대 10회)
- 재연결 실패 시 사용자에게 새로고침 안내

## BR-07: 주문 조회 범위
- 고객: 현재 session_id의 주문만 조회 가능
- 관리자: store_id 내 모든 활성 주문 조회 가능
