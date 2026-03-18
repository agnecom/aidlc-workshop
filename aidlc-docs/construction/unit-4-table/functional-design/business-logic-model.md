# Unit 4 - Business Logic Model

## 1. 테이블 생성/설정 플로우

```
Admin → POST /api/tables → TableService.create()
  1. table_number 중복 확인 (store_id 내)
  2. password bcrypt 해싱
  3. Table 생성
  4. TableSession 자동 생성 (is_active=True)
  5. return Table
```

## 2. 테이블 목록 조회

```
Admin → GET /api/tables → TableService.get_all()
  - store_id 기준 전체 테이블 + 활성 세션 주문 수/총액 요약
```

## 3. 테이블 상세 조회

```
Admin → GET /api/tables/{id} → TableService.get_detail()
  - 테이블 정보 + 활성 세션의 주문 목록 (items 포함)
```

## 4. 이용 완료 플로우

```
Admin → POST /api/tables/{id}/complete → TableService.complete()
  1. 활성 세션 확인
  2. 세션의 모든 주문 → OrderHistory로 복사 (items_snapshot JSON)
  3. 세션의 모든 주문 삭제
  4. 세션 종료 (is_active=False, ended_at 설정)
  5. 새 세션 생성 (is_active=True)
  6. SSE broadcast("session_completed", {table_id})
```

## 5. 과거 주문 내역 조회

```
Admin → GET /api/tables/{id}/history?date_from&date_to → TableService.get_history()
  - OrderHistory 테이블에서 table_id + 날짜 필터 조회
  - 시간 역순 정렬
```

## 6. 테이블 비밀번호 변경

```
Admin → PUT /api/tables/{id} → TableService.update()
  - password 변경 시 bcrypt 재해싱
```
