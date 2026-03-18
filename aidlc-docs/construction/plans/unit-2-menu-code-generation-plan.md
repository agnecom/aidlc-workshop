# Unit 2 Code Generation Plan (메뉴 관리 및 조회)

## Stories: US-02, US-12

## Steps

### Step 1: Backend - 메뉴 스키마 및 서비스
- [ ] `backend/app/schemas/menu.py`
- [ ] `backend/app/schemas/category.py`
- [ ] `backend/app/services/menu_service.py`
- [ ] `backend/app/services/file_storage.py`
- [ ] `backend/app/repositories/menu_repository.py`
- [ ] `backend/app/repositories/category_repository.py`

### Step 2: Backend - 메뉴 라우터
- [ ] `backend/app/routers/menu.py`
- [ ] `backend/app/routers/category.py`
- [ ] main.py에 라우터 등록

### Step 3: Backend Unit Tests
- [ ] `backend/tests/test_menu_router.py`

### Step 4: Customer Frontend - MenuView
- [ ] `customer-frontend/src/views/MenuView.vue` (실제 구현)
- [ ] `customer-frontend/src/services/menu.js`

### Step 5: Admin Frontend - MenuManageView
- [ ] `admin-frontend/src/views/MenuManageView.vue`
- [ ] `admin-frontend/src/services/menu.js`
- [ ] 라우터에 메뉴 관리 경로 추가

### Step 6: Frontend Tests
- [ ] `admin-frontend/src/views/__tests__/MenuManageView.test.js`
