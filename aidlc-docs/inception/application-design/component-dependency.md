# Component Dependencies

## 의존성 매트릭스

```
                  Auth  Menu  Order  Table  SSE   FileStorage  DB
Auth Router        ✓                                           ✓
Menu Router              ✓                         ✓           ✓
Order Router                    ✓                  (via SSE)   ✓
Table Router                           ✓           (via SSE)   ✓
SSE Router                                    ✓
Customer FE       ✓     ✓      ✓              ✓
Admin FE          ✓     ✓      ✓       ✓      ✓
```

## 통신 패턴

### Frontend → Backend
- **프로토콜**: HTTP REST (JSON)
- **인증**: JWT Bearer Token (Authorization 헤더)
- **실시간**: SSE (Server-Sent Events)

### Backend 내부
- **Router → Service**: 직접 함수 호출
- **Service → Repository**: 직접 함수 호출
- **Service → SSEManager**: 직접 함수 호출 (이벤트 브로드캐스트)

### 데이터 흐름

```
+------------------+     REST/SSE     +------------------+
| Customer Frontend| <--------------> |                  |
+------------------+                  |                  |
                                      |   Backend API    |
+------------------+     REST/SSE     |   (FastAPI)      |
| Admin Frontend   | <--------------> |                  |
+------------------+                  +--------+---------+
                                               |
                                          SQLAlchemy
                                               |
                                      +--------+---------+
                                      |   PostgreSQL     |
                                      +------------------+
```

## 컴포넌트 간 이벤트 흐름 (SSE)

```
OrderService.create_order()
  → SSEManager.broadcast("order_created", order_data)
    → Admin Frontend (대시보드 업데이트)
    → Customer Frontend (해당 테이블만)

OrderService.update_status()
  → SSEManager.broadcast("order_updated", order_data)
    → Admin Frontend (대시보드 업데이트)
    → Customer Frontend (해당 테이블만)

TableService.complete_session()
  → SSEManager.broadcast("session_closed", table_data)
    → Customer Frontend (해당 테이블만)
```
