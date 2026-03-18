# 테이블오더 서비스 — 운영 가이드

## 서비스 시작

```bash
# 전체 서비스 시작
docker compose up --build -d

# Seed 데이터 생성 (최초 1회)
docker compose exec backend python -m seed.init_data
```

## 접속 URL

| 서비스 | URL |
|--------|-----|
| 고객 화면 | http://localhost:3000 |
| 관리자 화면 | http://localhost:3001 |
| API 문서 | http://localhost:8000/docs |

## 기본 관리자 계정

- 매장 식별자: `store001`
- 사용자명: `admin`
- 비밀번호: `admin1234`

## 서비스 관리

```bash
# 서비스 상태 확인
docker compose ps

# 로그 확인
docker compose logs -f backend
docker compose logs -f customer-frontend
docker compose logs -f admin-frontend

# 서비스 중지
docker compose down

# DB 데이터 포함 완전 삭제
docker compose down -v
```

## 헬스체크

```bash
curl http://localhost:8000/api/health
```

## 아키텍처 요약

```
┌─────────────┐  ┌──────────────┐  ┌──────────┐
│  Customer FE │  │   Admin FE   │  │ Backend  │
│  :3000       │  │   :3001      │  │ :8000    │
│  Vue 3       │  │   Vue 3      │  │ FastAPI  │
└──────┬───────┘  └──────┬───────┘  └────┬─────┘
       │                 │               │
       └────────────┬────┘               │
                    │    REST API         │
                    └────────────────────►│
                         SSE (실시간)     │
                    ◄────────────────────┤
                                         │
                                  ┌──────┴──────┐
                                  │ PostgreSQL   │
                                  │ :5432        │
                                  └─────────────┘
```

## 테스트 실행

```bash
# Backend (27 tests)
cd backend && source venv/bin/activate && UPLOAD_DIR=./uploads PYTHONPATH=. pytest -v

# Customer Frontend
cd customer-frontend && npm install && npm test

# Admin Frontend
cd admin-frontend && npm install && npm test
```

## 주요 기능

1. **고객 주문**: 테이블 태블릿에서 메뉴 조회 → 장바구니 → 주문
2. **실시간 알림**: SSE 기반 주문 상태 실시간 업데이트
3. **관리자 대시보드**: 주문 현황, 상태 변경 (pending → preparing → completed)
4. **메뉴 관리**: 카테고리/메뉴 CRUD, 이미지 업로드, 정렬
5. **테이블 관리**: 테이블 생성, 세션 관리, 이용 완료, 주문 이력

## 보안 사항

- JWT HS256 인증 (16시간 만료)
- bcrypt 비밀번호 해싱
- 서버 측 가격 재계산 (클라이언트 조작 방지)
- 주문 상태 전이 검증 (pending → preparing → completed만 허용)
- CORS 설정 적용
