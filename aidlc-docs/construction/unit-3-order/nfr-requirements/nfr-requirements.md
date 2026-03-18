# NFR Requirements - Unit 3 (주문 및 실시간 통신)

Unit 1에서 정의된 NFR 기반 적용. 추가 사항:

## 보안
- SECURITY-05: 주문 입력 검증 (items 비어있지 않음, quantity 1~99, menu_item_id 존재 확인)
- SECURITY-08: 주문 생성은 table role, 상태 변경/삭제는 admin role만 허용
- SECURITY-10: total_amount 서버 측 재계산 (클라이언트 값 무시, 가격 조작 방지)
- SECURITY-11: 주문 조회 시 session_id/store_id 기반 데이터 격리

## 성능
- 주문 생성 응답: 500ms 이내
- 주문 목록 조회: 200ms 이내
- SSE 이벤트 전달: 주문 생성/변경 후 2초 이내
- SSE 동시 연결: 20개 이하 (소규모 단일 매장)

## 가용성
- SSE 연결 끊김 시 클라이언트 자동 재연결 (3초 간격, 최대 10회)
- 재연결 실패 시 사용자에게 새로고침 안내
- 장바구니 localStorage 영속화 (브라우저 새로고침 시 복원)
