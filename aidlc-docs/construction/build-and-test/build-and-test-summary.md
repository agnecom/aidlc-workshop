# Build and Test Summary

## Build Status
- **Build Tool**: Docker Compose
- **서비스**: backend (FastAPI), customer-frontend (Vue.js), admin-frontend (Vue.js), db (PostgreSQL)
- **빌드 명령**: `docker compose up --build`

## Test Execution Summary

### Unit Tests — Backend (pytest)
| 파일 | 테스트 수 | 범위 |
|------|-----------|------|
| test_auth_service.py | 기존 | 비밀번호 해싱, JWT |
| test_auth_router.py | 기존 | 로그인 API |
| test_models.py | 기존 | 모델 생성 |
| test_menu_router.py | 4 | 메뉴 CRUD |
| test_order_router.py | 6 | 주문 CRUD, 상태 전이 |
| test_table_router.py | 6 | 테이블 CRUD, 이용 완료 |

### Unit Tests — Admin Frontend (vitest)
| 파일 | 테스트 수 |
|------|-----------|
| LoginView.test.js | 기존 |
| MenuManageView.test.js | 3 |
| DashboardView.test.js | 3 |
| TableManageView.test.js | 3 |

### Integration Tests
- 시나리오 2개 (curl 기반 수동 테스트)
- 시나리오 1: 관리자 로그인 → 메뉴 등록 → 고객 조회
- 시나리오 2: 고객 주문 → 상태 변경 → 이용 완료 → 이력 확인

### Performance Tests
- 소규모 매장 대상 간단한 응답 시간 측정
- 목표: 주문 생성 < 500ms, 메뉴 조회 < 200ms

## 전체 아키텍처 요약

```
[Customer Tablet]  →  [Customer Frontend :3000]  →  [Backend API :8000]  →  [PostgreSQL :5432]
[Admin Browser]    →  [Admin Frontend :3001]     →       ↑
                                                    [SSE EventStream]
```

## 구현된 기능
- ✅ Unit 1: 프로젝트 기반 + 인증 (관리자/테이블 JWT)
- ✅ Unit 2: 메뉴 관리 + 조회 (CRUD, 이미지 업로드, 카테고리)
- ✅ Unit 3: 주문 + 실시간 통신 (장바구니, 주문 CRUD, SSE)
- ✅ Unit 4: 테이블 관리 (생성, 이용 완료, 과거 내역)

## Next Steps
- 테스트 실행 후 결과 확인
- 모든 테스트 통과 시 Operations 단계로 진행 가능
