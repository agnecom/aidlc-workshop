# NFR Requirements - Unit 4 (테이블 관리)

Unit 1에서 정의된 NFR 기반 적용. 추가 사항:

## 보안
- SECURITY-05: 테이블 번호 양수 정수, 비밀번호 최소 4자
- SECURITY-08: 모든 테이블 관리 API는 admin role만 허용
- SECURITY-12: 이용 완료 시 주문 데이터 이력 보존 (삭제 아닌 이동)

## 성능
- 이용 완료 처리: 1초 이내 (소규모 주문 수)
- 과거 내역 조회: 500ms 이내
