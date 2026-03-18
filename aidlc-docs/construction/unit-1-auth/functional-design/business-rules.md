# Business Rules - Unit 1 (인증)

## BR-01: 비밀번호 해싱
- 모든 비밀번호는 bcrypt로 해싱하여 저장
- 평문 비밀번호는 절대 저장하지 않음

## BR-02: 로그인 시도 제한
- 연속 5회 실패 시 계정 15분 잠금
- 성공 시 실패 횟수 초기화
- 잠금 시간 경과 후 자동 해제

## BR-03: JWT 토큰 규칙
- 만료 시간: 16시간
- 알고리즘: HS256
- Payload 필수 필드: sub (사용자 ID), store_id, role, exp
- 테이블 토큰 추가 필드: table_id, session_id

## BR-04: 테이블 번호 유일성
- 동일 매장 내 테이블 번호 중복 불가
- (store_id, table_number) UNIQUE 제약

## BR-05: 관리자 계정 유일성
- 동일 매장 내 사용자명 중복 불가
- (store_id, username) UNIQUE 제약

## BR-06: 세션 관리
- 테이블당 활성 세션은 최대 1개
- 이용 완료 시 세션 종료 (is_active=false, ended_at 설정)
- 새 로그인 시 활성 세션이 없으면 새 세션 생성

## BR-07: 인증 에러 메시지
- 로그인 실패 시 구체적 실패 원인을 노출하지 않음 (보안)
- 통합 메시지: "매장 식별자, 사용자명 또는 비밀번호가 올바르지 않습니다."

## BR-08: 주문 번호 채번
- 매장 내 순차 증가 (auto increment 또는 sequence)
- 전역 고유가 아닌 매장 내 고유

## BR-09: 주문 항목 스냅샷
- OrderItem에 주문 시점의 menu_name, unit_price 저장
- 메뉴 가격 변경 시 기존 주문에 영향 없음

## BR-10: 주문 상태 전이
- pending → preparing → completed (단방향)
- 역방향 전이 불가
