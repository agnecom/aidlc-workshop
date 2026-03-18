# Components

## 시스템 구성

| 컴포넌트 | 유형 | 설명 |
|----------|------|------|
| Backend API | FastAPI 앱 | 단일 앱, Router로 도메인 분리 |
| Customer Frontend | Vue.js SPA | 고객용 주문 인터페이스 |
| Admin Frontend | Vue.js SPA | 관리자용 운영 인터페이스 |
| PostgreSQL | Database | 데이터 저장소 |

---

## Backend API 컴포넌트 (도메인별 Router)

### AUTH Router
- **책임**: 관리자 인증, 테이블 태블릿 인증, JWT 토큰 관리
- **인터페이스**: REST API (`/api/auth/*`)

### MENU Router
- **책임**: 메뉴/카테고리 CRUD, 이미지 업로드, 노출 순서 관리
- **인터페이스**: REST API (`/api/menus/*`, `/api/categories/*`)

### ORDER Router
- **책임**: 주문 생성, 주문 조회, 주문 상태 변경, 주문 삭제
- **인터페이스**: REST API (`/api/orders/*`)

### TABLE Router
- **책임**: 테이블 설정, 세션 관리, 이용 완료 처리, 과거 내역 조회
- **인터페이스**: REST API (`/api/tables/*`)

### SSE Router
- **책임**: 실시간 이벤트 스트리밍 (주문 생성/상태 변경)
- **인터페이스**: SSE (`/api/sse/*`)

### 공통 레이어
- **Models**: SQLAlchemy ORM 모델 (9개 엔티티)
- **Schemas**: Pydantic 요청/응답 스키마
- **Dependencies**: 인증 미들웨어, DB 세션 관리
- **Config**: 환경 설정, 보안 설정

---

## Customer Frontend 컴포넌트

### Views
- **MenuView**: 카테고리별 메뉴 조회/탐색
- **CartView**: 장바구니 관리
- **OrderView**: 주문 확인/생성
- **OrderHistoryView**: 주문 내역 조회

### 공통
- **AuthGuard**: 자동 로그인/세션 관리
- **CartStore**: 장바구니 상태 관리 (localStorage)
- **SSEClient**: 실시간 주문 상태 수신

---

## Admin Frontend 컴포넌트

### Views
- **LoginView**: 관리자 로그인
- **DashboardView**: 실시간 주문 모니터링 (테이블별 그리드)
- **TableManageView**: 테이블 설정/세션 관리/과거 내역
- **MenuManageView**: 메뉴 CRUD/이미지 업로드/순서 조정

### 공통
- **AuthGuard**: JWT 인증/세션 관리
- **SSEClient**: 실시간 주문 수신
