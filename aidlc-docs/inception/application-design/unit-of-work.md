# Unit of Work

## 분해 전략
기능 슬라이스별 분해 - 각 단위에서 Backend API + Frontend를 함께 개발하여 기능 단위로 완결성 확보.

---

## Unit 1: 프로젝트 기반 및 인증

**범위**: 프로젝트 초기 설정, DB 스키마, 관리자 인증, 테이블 태블릿 인증

**Backend**:
- FastAPI 프로젝트 구조 설정
- SQLAlchemy 모델 전체 정의 (9개 엔티티)
- DB 마이그레이션 (Alembic)
- AUTH Router + AuthService (관리자 로그인, 테이블 로그인)
- JWT 토큰 발급/검증, bcrypt 해싱
- 로그인 시도 제한
- seed 데이터 (관리자 계정, 매장 정보)
- Docker Compose 설정 (Backend + PostgreSQL)

**Customer Frontend**:
- Vue.js 프로젝트 구조 설정
- 자동 로그인 (AuthGuard)
- Docker 설정

**Admin Frontend**:
- Vue.js 프로젝트 구조 설정
- 로그인 화면 (LoginView)
- JWT 세션 관리 (AuthGuard)
- Docker 설정

---

## Unit 2: 메뉴 관리 및 조회

**범위**: 메뉴/카테고리 CRUD, 이미지 업로드, 고객 메뉴 조회

**Backend**:
- MENU Router + MenuService
- 카테고리/메뉴 CRUD API
- 이미지 파일 업로드 + FileStorage
- 메뉴 노출 순서 관리
- 입력 검증 (필수 필드, 가격 범위)

**Customer Frontend**:
- MenuView (카테고리별 메뉴 조회, 카드 레이아웃)

**Admin Frontend**:
- MenuManageView (메뉴 CRUD, 이미지 업로드, 순서 조정)

---

## Unit 3: 주문 및 실시간 통신

**범위**: 장바구니, 주문 생성/조회, SSE 실시간 통신, 주문 모니터링, 주문 상태 변경

**Backend**:
- ORDER Router + OrderService
- SSE Router + SSEManager
- 주문 생성, 조회, 상태 변경, 삭제 API
- SSE 이벤트 브로드캐스트

**Customer Frontend**:
- CartView + CartStore (장바구니 관리, localStorage)
- OrderView (주문 확인/생성)
- OrderHistoryView (주문 내역 조회)
- SSEClient (주문 상태 실시간 수신)

**Admin Frontend**:
- DashboardView (테이블별 그리드, 실시간 주문 모니터링)
- 주문 상태 변경 기능
- SSEClient (신규 주문/상태 변경 수신)

---

## Unit 4: 테이블 관리

**범위**: 테이블 설정, 세션 관리, 이용 완료, 과거 내역 조회

**Backend**:
- TABLE Router + TableService
- 테이블 생성/설정 API
- 이용 완료 처리 (주문 → 이력 이동)
- 과거 주문 내역 조회 API (날짜 필터)

**Admin Frontend**:
- TableManageView (테이블 설정, 주문 삭제, 이용 완료, 과거 내역)

---

## 코드 조직 전략

```
table-order/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── repositories/
│   │   └── dependencies/
│   ├── migrations/
│   ├── uploads/
│   ├── seed/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── customer-frontend/
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── services/
│   │   └── router/
│   ├── package.json
│   └── Dockerfile
├── admin-frontend/
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── services/
│   │   └── router/
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml
```
