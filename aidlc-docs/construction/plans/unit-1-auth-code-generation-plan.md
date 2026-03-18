# Unit 1 Code Generation Plan (프로젝트 기반 및 인증)

## Unit Context
- **Stories**: US-01, US-06, US-09, US-ERR-01, US-ERR-04
- **Dependencies**: 없음 (첫 번째 Unit)
- **Scope**: 프로젝트 구조, DB 모델 전체, 인증 시스템, Docker Compose

## Code Location
- **Workspace Root**: /Users/agne/AI/aidlc-workshop
- **Backend**: `backend/`
- **Customer Frontend**: `customer-frontend/`
- **Admin Frontend**: `admin-frontend/`
- **Docker Compose**: 루트

---

## Steps

### Step 1: Backend 프로젝트 구조 설정
- [x] `backend/app/` 디렉토리 구조 생성
- [x] `backend/app/main.py`
- [x] `backend/app/config.py`
- [x] `backend/app/database.py`
- [x] `backend/requirements.txt`
- [x] `backend/Dockerfile`

### Step 2: DB 모델 정의
- [x] `backend/app/models/__init__.py`
- [x] `backend/app/models/store.py`
- [x] `backend/app/models/admin.py`
- [x] `backend/app/models/table.py`
- [x] `backend/app/models/category.py`
- [x] `backend/app/models/menu_item.py`
- [x] `backend/app/models/order.py`

### Step 3: Pydantic 스키마
- [x] `backend/app/schemas/auth.py`
- [x] `backend/app/schemas/table.py`
- [x] `backend/app/schemas/common.py`

### Step 4: 인증 모듈
- [x] `backend/app/dependencies/auth.py`
- [x] `backend/app/services/auth_service.py`
- [x] `backend/app/repositories/admin_repository.py`
- [x] `backend/app/repositories/store_repository.py`
- [x] `backend/app/repositories/table_repository.py`

### Step 5: AUTH Router
- [x] `backend/app/routers/auth.py`
- [x] `backend/app/routers/health.py`

### Step 6: Seed 데이터 및 마이그레이션
- [x] `backend/seed/init_data.py`
- [x] `backend/alembic.ini` + `backend/migrations/`

### Step 7: Backend Unit Tests
- [x] `backend/tests/conftest.py`
- [x] `backend/tests/test_auth_service.py`
- [x] `backend/tests/test_auth_router.py`
- [x] `backend/tests/test_models.py`

### Step 8: Customer Frontend 프로젝트 설정
- [x] Vue.js 프로젝트 구조
- [x] `customer-frontend/src/main.js`
- [x] `customer-frontend/src/router/index.js`
- [x] `customer-frontend/src/services/api.js`
- [x] `customer-frontend/src/services/auth.js`
- [x] `customer-frontend/src/views/InitialSetupView.vue`
- [x] `customer-frontend/Dockerfile` + `nginx.conf`

### Step 9: Customer Frontend Unit Tests
- [x] `customer-frontend/src/services/__tests__/auth.test.js`

### Step 10: Admin Frontend 프로젝트 설정
- [x] Vue.js 프로젝트 구조
- [x] `admin-frontend/src/main.js`
- [x] `admin-frontend/src/router/index.js`
- [x] `admin-frontend/src/services/api.js`
- [x] `admin-frontend/src/services/auth.js`
- [x] `admin-frontend/src/views/LoginView.vue`
- [x] `admin-frontend/Dockerfile` + `nginx.conf`

### Step 11: Admin Frontend Unit Tests
- [x] `admin-frontend/src/services/__tests__/auth.test.js`
- [x] `admin-frontend/src/views/__tests__/LoginView.test.js`

### Step 12: Docker Compose 및 문서
- [x] `docker-compose.yml`
- [x] `README.md`
