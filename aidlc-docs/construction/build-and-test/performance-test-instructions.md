# Performance Test Instructions

## 목적
소규모 매장 환경 (10테이블 이하)에서 성능 요구사항 충족 여부 확인.

## 성능 요구사항
| 항목 | 목표 |
|------|------|
| 주문 생성 응답 | < 500ms |
| 메뉴 목록 조회 | < 200ms |
| SSE 이벤트 전달 | < 2초 |
| 동시 SSE 연결 | 20개 |

## 간단한 부하 테스트 (curl 기반)

```bash
# 사전 준비: docker compose up, seed data, 관리자/테이블 토큰 발급

# 메뉴 조회 응답 시간 측정 (10회)
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{time_total}\n" \
    http://localhost:8000/api/menus \
    -H "Authorization: Bearer $TABLE_TOKEN"
done

# 주문 생성 응답 시간 측정
for i in $(seq 1 10); do
  curl -s -o /dev/null -w "%{time_total}\n" \
    -X POST http://localhost:8000/api/orders \
    -H "Authorization: Bearer $TABLE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"items\":[{\"menu_item_id\":\"$MENU_ID\",\"quantity\":1}]}"
done
```

## 참고
- 소규모 단일 매장 대상이므로 대규모 부하 테스트는 불필요
- 위 간단한 측정으로 목표 충족 여부 확인 가능
