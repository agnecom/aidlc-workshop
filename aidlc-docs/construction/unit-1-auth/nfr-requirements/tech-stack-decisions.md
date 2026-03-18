# Tech Stack Decisions - Unit 1 (인증)

## Backend

| 기술 | 버전 | 용도 |
|------|------|------|
| Python | 3.12 | 런타임 |
| FastAPI | 0.115.x | 웹 프레임워크 |
| Uvicorn | 0.34.x | ASGI 서버 |
| SQLAlchemy | 2.0.x | ORM |
| Alembic | 1.14.x | DB 마이그레이션 |
| Pydantic | 2.x | 데이터 검증 |
| python-jose | 3.3.x | JWT 처리 |
| passlib[bcrypt] | 1.7.x | 비밀번호 해싱 |
| psycopg2-binary | 2.9.x | PostgreSQL 드라이버 |
| python-multipart | 0.0.x | 파일 업로드 |
| structlog | 24.x | 구조화된 로깅 |

## Frontend (공통)

| 기술 | 버전 | 용도 |
|------|------|------|
| Vue.js | 3.5.x | UI 프레임워크 |
| Vue Router | 4.x | 라우팅 |
| Pinia | 2.x | 상태 관리 |
| Axios | 1.x | HTTP 클라이언트 |
| Vite | 6.x | 빌드 도구 |

## Infrastructure

| 기술 | 버전 | 용도 |
|------|------|------|
| PostgreSQL | 16 | 데이터베이스 |
| Docker | latest | 컨테이너화 |
| Docker Compose | v2 | 로컬 오케스트레이션 |

## 선택 근거
- **FastAPI**: 비동기 지원, SSE 네이티브, Pydantic 통합, 자동 API 문서
- **SQLAlchemy 2.0**: 타입 힌트 지원, 비동기 지원, 성숙한 ORM
- **Vue.js 3**: Composition API, 가벼운 번들, 학습 곡선 완만
- **PostgreSQL 16**: ACID, JSON 지원, 성숙한 생태계
