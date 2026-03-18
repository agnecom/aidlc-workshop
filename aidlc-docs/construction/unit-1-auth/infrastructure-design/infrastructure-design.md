# Infrastructure Design - Unit 1 (인증)

## 배포 환경
Docker Compose 기반 로컬 개발 환경

## 컨테이너 구성

| 서비스 | 이미지 | 포트 | 설명 |
|--------|--------|------|------|
| backend | python:3.12-slim (커스텀) | 8000 | FastAPI API 서버 |
| customer-frontend | node:20-slim (빌드) + nginx:alpine | 3000 | 고객용 Vue.js |
| admin-frontend | node:20-slim (빌드) + nginx:alpine | 3001 | 관리자용 Vue.js |
| db | postgres:16-alpine | 5432 | PostgreSQL |

## 네트워크
- 단일 Docker 네트워크 (`table-order-network`)
- 컨테이너 간 서비스명으로 통신 (예: `db:5432`)

## 볼륨
- `postgres-data`: PostgreSQL 데이터 영속화
- `./backend/uploads`: 이미지 업로드 디렉토리 (호스트 마운트)

## 환경 변수

### Backend
```
DATABASE_URL=postgresql://tableorder:tableorder@db:5432/tableorder
JWT_SECRET_KEY=<generated-secret>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=16
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
UPLOAD_DIR=/app/uploads
LOG_LEVEL=INFO
```

### Customer Frontend
```
VITE_API_BASE_URL=http://localhost:8000
```

### Admin Frontend
```
VITE_API_BASE_URL=http://localhost:8000
```

### PostgreSQL
```
POSTGRES_USER=tableorder
POSTGRES_PASSWORD=tableorder
POSTGRES_DB=tableorder
```

## 서비스 의존성
```
customer-frontend → backend → db
admin-frontend → backend → db
```

## 헬스체크
- backend: `GET /health` (200 OK)
- db: `pg_isready`
