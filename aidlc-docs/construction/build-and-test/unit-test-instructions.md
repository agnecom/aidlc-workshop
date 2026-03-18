# Unit Test Execution

## Backend (pytest)

### 실행
```bash
cd backend
pip install -r requirements.txt
pytest -v
```

### 테스트 파일
| 파일 | 테스트 수 | 범위 |
|------|-----------|------|
| test_auth_router.py | 기존 | 관리자/테이블 로그인, 인증 실패 |
| test_auth_service.py | 기존 | 비밀번호 해싱, JWT 토큰 |
| test_models.py | 기존 | 모델 생성 |
| test_menu_router.py | 4 | 메뉴 CRUD, 순서 변경 |
| test_order_router.py | 6 | 주문 생성/조회/상태변경/삭제, 잘못된 전이, 빈 장바구니 |
| test_table_router.py | 6 | 테이블 생성/중복/목록/이용완료/비밀번호변경/이력조회 |

### 예상 결과
- 모든 테스트 PASS
- SQLite in-memory DB 사용 (conftest.py)

## Customer Frontend (vitest)

### 실행
```bash
cd customer-frontend
npm install
npm test
```

## Admin Frontend (vitest)

### 실행
```bash
cd admin-frontend
npm install
npm test
```

### 테스트 파일
| 파일 | 테스트 수 | 범위 |
|------|-----------|------|
| LoginView.test.js | 기존 | 로그인 폼 렌더링 |
| MenuManageView.test.js | 3 | 메뉴 추가 버튼, 폼 표시, 테이블 렌더링 |
| DashboardView.test.js | 3 | 그리드 렌더링, 네비게이션, 상세 패널 |
| TableManageView.test.js | 3 | 추가 버튼, 폼 표시, 목록 렌더링 |

## 실패 시 대응
1. 에러 메시지 확인
2. 해당 테스트 파일 단독 실행: `pytest tests/test_xxx.py -v`
3. 코드 수정 후 재실행
