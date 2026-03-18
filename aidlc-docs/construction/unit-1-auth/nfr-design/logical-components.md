# Logical Components - Unit 1 (인증)

## Backend 논리 컴포넌트

### Middleware Layer
- **SecurityHeadersMiddleware**: HTTP 보안 헤더 설정
- **CORSMiddleware**: CORS 정책 적용
- **RequestIdMiddleware**: 요청별 correlation ID 생성/전파

### Dependencies (FastAPI DI)
- **get_db**: DB 세션 생성/해제 (try/finally)
- **get_current_user**: JWT 토큰 검증 + 사용자 정보 반환
- **get_current_admin**: admin role 검증
- **get_current_table**: table role 검증

### Auth Module
- **AuthService**: 인증 비즈니스 로직
- **JWTHandler**: 토큰 생성/검증 유틸리티
- **PasswordHandler**: bcrypt 해싱/검증 유틸리티

### Repository Layer
- **AdminRepository**: Admin CRUD
- **TableRepository**: Table CRUD
- **TableSessionRepository**: TableSession CRUD
- **StoreRepository**: Store 조회

### Error Handling
- **GlobalExceptionHandler**: 전역 예외 처리
- **AppException**: 커스텀 예외 클래스 (status_code, message, error_code)

### Logging
- **LoggerFactory**: structlog 설정 및 로거 생성
- 요청/응답 로깅 미들웨어

## Frontend 논리 컴포넌트

### Customer Frontend
- **AuthService**: 로그인 API 호출, 토큰 관리
- **HttpClient**: Axios 인스턴스 (JWT 자동 첨부, 에러 인터셉터)
- **AuthGuard**: 라우터 가드 (세션 검증, 자동 재로그인)

### Admin Frontend
- **AuthService**: 로그인 API 호출, 토큰 관리
- **HttpClient**: Axios 인스턴스 (JWT 자동 첨부, 에러 인터셉터)
- **AuthGuard**: 라우터 가드 (세션 검증, 만료 시 리다이렉트)
