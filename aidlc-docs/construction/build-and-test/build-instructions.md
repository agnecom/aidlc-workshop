# Build Instructions

## Prerequisites
- Docker & Docker Compose
- Node.js 18+ (로컬 개발/테스트 시)
- Python 3.12+ (로컬 개발/테스트 시)

## 방법 1: Docker Compose (권장)

### 1. 전체 서비스 빌드 및 시작
```bash
cd /Users/agne/AI/aidlc-workshop
docker compose up --build
```

### 2. Seed 데이터 생성 (최초 1회)
```bash
docker compose exec backend python -m seed.init_data
```

### 3. 빌드 확인
- Backend API: http://localhost:8000/docs
- Customer Frontend: http://localhost:3000
- Admin Frontend: http://localhost:3001
- Health Check: http://localhost:8000/health

## 방법 2: 로컬 개발 환경

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# PostgreSQL 실행 필요 (또는 docker compose up db)
export DATABASE_URL="postgresql://tableorder:tableorder@localhost:5432/tableorder"
export JWT_SECRET_KEY="dev-secret-key"
export CORS_ORIGINS="http://localhost:3000,http://localhost:3001"

uvicorn app.main:app --reload --port 8000
```

### Customer Frontend
```bash
cd customer-frontend
npm install
npm run dev  # http://localhost:3000
```

### Admin Frontend
```bash
cd admin-frontend
npm install
npm run dev  # http://localhost:3001
```

## Troubleshooting

### Port 충돌
```bash
# 사용 중인 포트 확인
lsof -i :8000
lsof -i :3000
lsof -i :3001
```

### DB 연결 실패
- Docker Compose에서 db 서비스가 healthy 상태인지 확인
- `docker compose logs db`로 로그 확인
