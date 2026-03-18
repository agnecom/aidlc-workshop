# Integration Test Instructions

## 목적
Unit 간 상호작용이 올바르게 동작하는지 검증합니다.

## 사전 준비
```bash
docker compose up --build -d
docker compose exec backend python -m seed.init_data
```

## 시나리오 1: 관리자 로그인 → 메뉴 등록 → 고객 메뉴 조회

### 테스트 단계
```bash
# 1. 관리자 로그인
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{"store_identifier":"store001","username":"admin","password":"admin1234"}' | jq -r '.access_token')

# 2. 카테고리 생성
CAT_ID=$(curl -s -X POST http://localhost:8000/api/categories \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"메인메뉴","display_order":0}' | jq -r '.id')

# 3. 메뉴 등록
MENU_ID=$(curl -s -X POST http://localhost:8000/api/menus \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -F "name=불고기버거" -F "price=8000" -F "category_id=$CAT_ID" | jq -r '.id')

# 4. 테이블 생성
TABLE_ID=$(curl -s -X POST http://localhost:8000/api/tables \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"table_number":1,"password":"1234"}' | jq -r '.id')

# 5. 테이블 로그인
TABLE_RESP=$(curl -s -X POST http://localhost:8000/api/auth/table/login \
  -H "Content-Type: application/json" \
  -d '{"store_identifier":"store001","table_number":1,"password":"1234"}')
TABLE_TOKEN=$(echo $TABLE_RESP | jq -r '.access_token')

# 6. 고객 메뉴 조회
curl -s http://localhost:8000/api/menus \
  -H "Authorization: Bearer $TABLE_TOKEN" | jq .
# 예상: 불고기버거 메뉴가 포함된 배열
```

## 시나리오 2: 고객 주문 → 관리자 상태 변경 → 이용 완료

```bash
# 1. 고객 주문 생성
ORDER_ID=$(curl -s -X POST http://localhost:8000/api/orders \
  -H "Authorization: Bearer $TABLE_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"items\":[{\"menu_item_id\":\"$MENU_ID\",\"quantity\":2}]}" | jq -r '.id')

# 2. 관리자 주문 확인
curl -s http://localhost:8000/api/orders/admin \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .

# 3. 상태 변경: pending → preparing
curl -s -X PATCH "http://localhost:8000/api/orders/$ORDER_ID/status" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"preparing"}' | jq .status
# 예상: "preparing"

# 4. 상태 변경: preparing → completed
curl -s -X PATCH "http://localhost:8000/api/orders/$ORDER_ID/status" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}' | jq .status
# 예상: "completed"

# 5. 이용 완료
curl -s -X POST "http://localhost:8000/api/tables/$TABLE_ID/complete" \
  -H "Authorization: Bearer $ADMIN_TOKEN" -w "%{http_code}"
# 예상: 204

# 6. 과거 내역 확인
curl -s "http://localhost:8000/api/tables/$TABLE_ID/history" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq .
# 예상: 이력 1건 (불고기버거 x2)
```

## 정리
```bash
docker compose down
```
