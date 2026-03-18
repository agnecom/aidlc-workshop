# Deployment Architecture - Unit 1 (인증)

## 아키텍처 다이어그램

```
+--------------------------------------------------+
|              Docker Compose Host                  |
|                                                   |
|  +-------------+  +-------------+  +-----------+  |
|  |  customer   |  |   admin     |  |           |  |
|  |  frontend   |  |  frontend   |  |  backend  |  |
|  |  (nginx)    |  |  (nginx)    |  |  (uvicorn)|  |
|  |  :3000      |  |  :3001      |  |  :8000    |  |
|  +------+------+  +------+------+  +-----+-----+  |
|         |                |               |         |
|         +--------+-------+               |         |
|                  |  HTTP/SSE             |         |
|                  +----------> backend    |         |
|                                    |              |
|                              +-----+-----+       |
|                              |    db      |       |
|                              | (postgres) |       |
|                              |   :5432    |       |
|                              +-----+------+       |
|                                    |              |
|                              [postgres-data]      |
+--------------------------------------------------+
```

## Dockerfile 전략

### Backend
- Base: `python:3.12-slim`
- 멀티스테이지 불필요 (인터프리터 언어)
- `requirements.txt` 먼저 복사 → 캐시 활용
- Uvicorn으로 실행

### Frontend (Customer / Admin 동일 패턴)
- Stage 1: `node:20-slim` — npm install + vite build
- Stage 2: `nginx:alpine` — 빌드 결과물만 복사
- nginx.conf: SPA 라우팅 (모든 경로 → index.html)

## 시작 순서
1. `db` (PostgreSQL) — 헬스체크 통과 대기
2. `backend` (FastAPI) — DB 마이그레이션 + seed 데이터 실행
3. `customer-frontend`, `admin-frontend` — 동시 시작
