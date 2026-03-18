# Infrastructure Design - Unit 3 (주문 및 실시간 통신)

Unit 1에서 정의된 인프라 그대로 사용. 추가 사항:

## SSE
- FastAPI StreamingResponse + asyncio.Queue (in-process, 별도 메시지 브로커 불필요)
- 소규모 단일 매장 (10테이블 이하) → 단일 프로세스 내 메모리 관리로 충분

## 변경 없음
- Docker Compose 구성 변경 없음
- DB 스키마는 Unit 1에서 이미 정의 완료 (Order, OrderItem, OrderHistory)
- 추가 인프라 서비스 불필요
