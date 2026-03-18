# Services

## Backend 서비스 레이어

각 Router는 대응하는 Service를 호출하여 비즈니스 로직을 처리합니다.

### AuthService
- **책임**: 인증/인가 로직
- **주요 기능**: 비밀번호 검증(bcrypt), JWT 토큰 발급/검증, 로그인 시도 제한
- **의존**: AdminRepository, TableRepository

### MenuService
- **책임**: 메뉴/카테고리 비즈니스 로직
- **주요 기능**: 메뉴 CRUD, 이미지 파일 저장, 노출 순서 관리, 입력 검증
- **의존**: MenuRepository, CategoryRepository, FileStorage

### OrderService
- **책임**: 주문 비즈니스 로직
- **주요 기능**: 주문 생성, 상태 전이(대기중→준비중→완료), 주문 삭제, 총 금액 계산
- **의존**: OrderRepository, TableSessionService, SSEManager

### TableService
- **책임**: 테이블/세션 비즈니스 로직
- **주요 기능**: 테이블 설정, 세션 시작/종료, 이용 완료(주문→이력 이동), 과거 내역 조회
- **의존**: TableRepository, OrderRepository, OrderHistoryRepository

### SSEManager
- **책임**: 실시간 이벤트 관리
- **주요 기능**: 클라이언트 연결 관리, 이벤트 브로드캐스트(주문 생성/상태 변경)
- **의존**: 없음 (다른 서비스에서 호출)

### FileStorage
- **책임**: 파일 저장 관리
- **주요 기능**: 이미지 파일 저장, URL 생성
- **의존**: 로컬 파일 시스템

---

## 서비스 오케스트레이션 패턴

### 주문 생성 플로우
```
Customer Frontend → ORDER Router → OrderService
  → OrderRepository.create()
  → SSEManager.broadcast(new_order)
  → return Order
```

### 주문 상태 변경 플로우
```
Admin Frontend → ORDER Router → OrderService
  → OrderRepository.update_status()
  → SSEManager.broadcast(order_updated)
  → return Order
```

### 이용 완료 플로우
```
Admin Frontend → TABLE Router → TableService
  → OrderRepository.get_by_session()
  → OrderHistoryRepository.bulk_create()
  → OrderRepository.delete_by_session()
  → TableSessionRepository.close()
  → SSEManager.broadcast(session_closed)
```
