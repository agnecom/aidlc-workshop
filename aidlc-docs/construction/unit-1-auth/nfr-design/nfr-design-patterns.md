# NFR Design Patterns - Unit 1 (인증)

## 보안 패턴

### Authentication Middleware 패턴
- FastAPI `Depends`를 활용한 JWT 검증 미들웨어
- role 기반 분기: `get_current_admin`, `get_current_table`
- 모든 보호된 엔드포인트에 의존성 주입

### Rate Limiting 패턴
- 로그인 엔드포인트에 IP 기반 rate limiting
- DB 레벨 브루트포스 보호 (failed_login_attempts + locked_until)

### Security Headers Middleware
- FastAPI middleware로 모든 응답에 보안 헤더 추가
- CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy

### CORS Configuration
- 허용 origin: Customer Frontend, Admin Frontend URL만 명시적 허용
- credentials: true (JWT 전달)

## 에러 처리 패턴

### Global Exception Handler
- FastAPI `exception_handler`로 전역 에러 처리
- 프로덕션: 내부 정보 미노출, 일반 에러 메시지 반환
- 모든 에러 구조화된 로깅 (structlog)

### Fail-Closed 패턴
- JWT 검증 실패 → 401 (접근 거부)
- DB 연결 실패 → 503 (서비스 불가)
- 예외 발생 시 기본 동작: 거부

## 로깅 패턴

### Structured Logging
- structlog 사용
- 필수 필드: timestamp, request_id, level, message
- 민감 정보 필터링 (password, token 마스킹)
- 요청별 correlation ID (X-Request-ID 헤더)

## 데이터 검증 패턴

### Input Validation (Pydantic)
- 모든 API 입력을 Pydantic 모델로 검증
- 타입 체크, 길이 제한, 형식 검증
- 커스텀 validator로 비즈니스 규칙 검증
