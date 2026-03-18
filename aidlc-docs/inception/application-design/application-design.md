# Application Design - 통합 문서

## 아키텍처 개요

테이블오더 서비스는 3-tier 아키텍처로 구성됩니다:
- **Presentation**: Customer Frontend (Vue.js) + Admin Frontend (Vue.js)
- **Application**: Backend API (FastAPI, 단일 앱 + Router 분리)
- **Data**: PostgreSQL

통신: REST API (JSON) + SSE (실시간)

---

## 시스템 구성도

```
+-------------------+          +-------------------+
| Customer Frontend |          |  Admin Frontend   |
|    (Vue.js)       |          |    (Vue.js)       |
+--------+----------+          +--------+----------+
         |                              |
         |  REST API + SSE              |  REST API + SSE
         |                              |
+--------+------------------------------+----------+
|              Backend API (FastAPI)                |
|                                                   |
|  +-------+ +------+ +-------+ +-------+ +-----+  |
|  | AUTH  | | MENU | | ORDER | | TABLE | | SSE |  |
|  |Router | |Router| |Router | |Router | |Route|  |
|  +---+---+ +--+---+ +---+---+ +---+---+ +--+--+  |
|      |        |          |         |        |     |
|  +---+---+ +--+---+ +---+---+ +---+---+    |     |
|  | Auth  | | Menu | |Order | |Table |    |     |
|  |Service| |Serv. | |Serv. | |Serv. |    |     |
|  +---+---+ +--+---+ +---+---+ +---+---+    |     |
|      |        |          |         |        |     |
|  +---+--------+----------+---------+--------+--+ |
|  |           SQLAlchemy ORM + Repositories      | |
|  +----------------------------------------------+ |
+-------------------------+-------------------------+
                          |
                 +--------+--------+
                 |   PostgreSQL    |
                 +-----------------+
```

---

## 컴포넌트 요약

| 컴포넌트 | 기술 | 책임 |
|----------|------|------|
| Backend API | FastAPI | REST API + SSE, 비즈니스 로직, 인증 |
| Customer Frontend | Vue.js | 메뉴 조회, 장바구니, 주문, 내역 조회 |
| Admin Frontend | Vue.js | 로그인, 주문 모니터링, 테이블/메뉴 관리 |
| PostgreSQL | PostgreSQL | 데이터 영속화 |

## Backend 도메인 구조

| Router | Service | 주요 기능 |
|--------|---------|-----------|
| AUTH | AuthService | 관리자/테이블 인증, JWT, bcrypt |
| MENU | MenuService | 메뉴 CRUD, 이미지 업로드, 순서 관리 |
| ORDER | OrderService | 주문 생성/조회/상태 변경/삭제 |
| TABLE | TableService | 테이블 설정, 세션 관리, 이용 완료 |
| SSE | SSEManager | 실시간 이벤트 브로드캐스트 |

## 핵심 설계 결정

1. **단일 FastAPI 앱 + Router 분리**: 소규모 MVP에 적합, 배포 단순화
2. **별도 Frontend 앱**: 고객/관리자 관심사 분리, 독립 배포 가능
3. **REST + SSE**: 표준적이고 구현이 단순한 통신 방식
4. **Repository 패턴**: Service와 DB 접근 분리, 테스트 용이성

## 상세 문서 참조

- [components.md](components.md) - 컴포넌트 정의 및 책임
- [component-methods.md](component-methods.md) - 메서드 시그니처
- [services.md](services.md) - 서비스 정의 및 오케스트레이션
- [component-dependency.md](component-dependency.md) - 의존성 관계
