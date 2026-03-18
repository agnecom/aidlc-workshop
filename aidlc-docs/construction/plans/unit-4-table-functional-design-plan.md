# Unit 4 (테이블 관리) - Functional Design Plan

## Steps
- [x] Step 1: Business Logic Model
- [x] Step 2: Business Rules
- [x] Step 3: Frontend Components
- [x] Step 4: Approval

## Questions

### Q1: 테이블 비밀번호 변경
이용 완료 후 테이블 비밀번호를 변경할 수 있어야 하나요?
- A) 아니오, 초기 설정 시에만 가능
- B) 예, 관리자가 언제든 변경 가능

[Answer]: B

### Q2: 이용 완료 시 미완료 주문 처리
이용 완료 시 pending/preparing 상태의 주문이 있으면?
- A) 이용 완료 차단 (모든 주문 completed 필요)
- B) 강제 이용 완료 (모든 주문 상태 무관하게 이력으로 이동)

[Answer]: B
