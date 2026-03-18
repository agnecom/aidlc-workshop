# Business Logic Model - Unit 1 (인증)

## 관리자 로그인 플로우

```
1. 입력: store_identifier, username, password
2. Store 조회 (store_identifier) → 없으면 401
3. Admin 조회 (store_id + username) → 없으면 401
4. 계정 잠금 확인 (locked_until > now) → 잠겨있으면 423
5. 비밀번호 검증 (bcrypt.verify)
   → 실패: failed_login_attempts += 1
     → 5회 이상: locked_until = now + 15분
     → 401 반환
   → 성공: failed_login_attempts = 0, locked_until = null
6. JWT 토큰 발급 (payload: admin_id, store_id, role="admin", exp=16h)
7. 200 + {access_token, token_type: "bearer"} 반환
```

## 테이블 태블릿 로그인 플로우

```
1. 입력: store_id, table_number, password
2. Table 조회 (store_id + table_number) → 없으면 401
3. 비밀번호 검증 (bcrypt.verify) → 실패 시 401
4. 활성 세션 확인:
   → 활성 세션 있음: 기존 session_id 사용
   → 활성 세션 없음: 새 TableSession 생성 (첫 주문 시 시작이 아닌 로그인 시 시작)
5. JWT 토큰 발급 (payload: table_id, store_id, session_id, role="table", exp=16h)
6. 200 + {access_token, token_type: "bearer", session_id} 반환
```

## 테이블 초기 설정 플로우 (관리자)

```
1. 입력: table_number, password (관리자 인증 필요)
2. 중복 확인 (store_id + table_number) → 중복 시 409
3. password → bcrypt.hash
4. Table 생성
5. 201 + Table 정보 반환
```

## JWT 토큰 검증 (미들웨어)

```
1. Authorization 헤더에서 Bearer 토큰 추출
2. JWT 디코딩 + 서명 검증 + 만료 확인
3. payload에서 role 확인 (admin/table)
4. 해당 엔티티 존재 확인
5. 요청 컨텍스트에 사용자 정보 주입
```

## Seed 데이터

```
1. Store: 기본 매장 1개 (store_identifier: "store001")
2. Admin: 기본 관리자 1개 (username: "admin", password: bcrypt("admin1234"))
```
