# Unit 3 (주문 및 실시간 통신) - Functional Design Plan

## Steps

- [x] Step 1: Business Logic Model — 주문 생성/상태 전이/삭제, SSE 이벤트 브로드캐스트, 장바구니 로직
- [x] Step 2: Business Rules — 주문 검증, 상태 전이 규칙, SSE 재연결 정책
- [x] Step 3: Frontend Components — CartView, OrderView, OrderHistoryView (고객), DashboardView 확장 (관리자), SSEClient
- [ ] Step 4: Review & Approval

## Questions

### Q1: 주문 번호 생성 방식
주문 번호(order_number)를 매장 내에서 어떻게 생성할까요?

- A) 매장별 자동 증가 (store_id 기준 max+1)
- B) 일별 리셋 (매일 1번부터 시작)
- C) 전체 시퀀스 (리셋 없이 계속 증가)

[Answer]: A

### Q2: SSE 이벤트 범위
관리자 SSE는 매장 전체 주문을 수신하고, 고객 SSE는 해당 테이블만 수신하는 것이 맞나요?

- A) 맞다 (관리자=매장 전체, 고객=테이블 한정)
- B) 관리자도 테이블별 필터링 필요

[Answer]: A

### Q3: 장바구니 수량 제한
메뉴 항목당 최대 수량 제한이 필요한가요?

- A) 제한 없음
- B) 항목당 최대 99개
- C) 항목당 최대 10개

[Answer]: B

### Q4: 주문 상태 변경 시 알림 방식
고객 화면에서 주문 상태 변경 시 어떤 방식으로 알릴까요?

- A) 주문 내역 화면에서 상태 텍스트만 실시간 업데이트
- B) 토스트/알림 팝업 + 상태 텍스트 업데이트
- C) 상태 텍스트 업데이트 + 사운드 알림

[Answer]: A

### Q5: 대시보드 테이블 카드 레이아웃
관리자 대시보드에서 테이블 카드를 어떻게 배치할까요?

- A) 그리드 레이아웃 (고정 열 수)
- B) 반응형 그리드 (화면 크기에 따라 자동 조절)

[Answer]: B
