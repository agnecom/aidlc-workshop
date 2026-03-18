# NFR Design - Unit 4 (테이블 관리)

## 이용 완료 트랜잭션 패턴
- 단일 DB 트랜잭션 내에서 주문→이력 이동 + 세션 종료 + 새 세션 생성
- 실패 시 전체 롤백

## 권한 분리
- 모든 TABLE Router 엔드포인트: get_current_admin 의존성
