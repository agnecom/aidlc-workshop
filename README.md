# 테이블오더 서비스

디지털 주문 시스템 — 고객 주문 + 관리자 운영 플랫폼

## 기술 스택
- Backend: Python 3.12 + FastAPI
- Frontend: Vue.js 3 (고객용 + 관리자용)
- Database: PostgreSQL 16
- Infrastructure: Docker Compose

## 실행 방법

```bash
# 전체 서비스 시작
docker compose up --build

# Seed 데이터 생성 (최초 1회)
docker compose exec backend python -m seed.init_data
```

## 접속 URL
- 고객 화면: http://localhost:3000
- 관리자 화면: http://localhost:3001
- API 문서: http://localhost:8000/docs

## 기본 관리자 계정
- 매장 식별자: `store001`
- 사용자명: `admin`
- 비밀번호: `admin1234`

## 테스트 실행

```bash
# Backend 테스트
cd backend && pip install -r requirements.txt && pytest

# Customer Frontend 테스트
cd customer-frontend && npm install && npm test

# Admin Frontend 테스트
cd admin-frontend && npm install && npm test
```
