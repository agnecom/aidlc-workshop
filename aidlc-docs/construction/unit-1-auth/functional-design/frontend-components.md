# Frontend Components - Unit 1 (인증)

## Customer Frontend

### AuthGuard (라우터 가드)
- **역할**: 자동 로그인 및 세션 유효성 검증
- **상태**: localStorage에 저장된 `{store_id, table_number, password, access_token}`
- **로직**:
  1. localStorage에서 인증 정보 로드
  2. access_token 존재 시 → API 호출로 유효성 확인
  3. 유효하면 → 메뉴 화면으로 이동
  4. 만료/무효 시 → 저장된 credentials로 재로그인 시도
  5. 재로그인 실패 시 → 에러 메시지 표시 ("관리자에게 문의")
- **API**: `POST /api/auth/table/login`

### InitialSetupView (초기 설정 - 1회)
- **역할**: 관리자가 태블릿에서 최초 인증 정보 입력
- **필드**: store_id (매장 식별자), table_number, password
- **동작**: 로그인 성공 시 credentials를 localStorage에 저장
- **이후**: AuthGuard가 자동 로그인 처리

---

## Admin Frontend

### LoginView
- **역할**: 관리자 로그인 화면
- **필드**: store_identifier, username, password
- **동작**:
  1. 입력값 클라이언트 검증 (빈 값 체크)
  2. `POST /api/auth/admin/login` 호출
  3. 성공 → JWT를 localStorage에 저장, 대시보드로 이동
  4. 실패 → 에러 메시지 표시
  5. 계정 잠금 → 잠금 안내 메시지 표시
- **API**: `POST /api/auth/admin/login`

### AuthGuard (라우터 가드)
- **역할**: JWT 세션 유효성 검증
- **로직**:
  1. localStorage에서 access_token 로드
  2. 토큰 없음/만료 → 로그인 화면으로 리다이렉트
  3. 유효 → 요청 진행
- **세션 유지**: 브라우저 새로고침 시 localStorage에서 복원
