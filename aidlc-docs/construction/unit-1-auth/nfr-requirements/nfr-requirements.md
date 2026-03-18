# NFR Requirements - Unit 1 (인증)

## 성능
- 로그인 API 응답: 500ms 이내
- JWT 토큰 검증: 50ms 이내
- 동시 접속: 테이블 10개 + 관리자 2명 (소규모)

## 보안 (SECURITY 규칙 적용)

| 규칙 | Unit 1 적용 사항 |
|------|-----------------|
| SECURITY-01 | PostgreSQL TLS 연결, 저장 시 암호화 |
| SECURITY-03 | 구조화된 로깅 (timestamp, request_id, level) |
| SECURITY-04 | HTTP 보안 헤더 (CSP, HSTS, X-Content-Type-Options 등) |
| SECURITY-05 | 로그인 입력 검증 (타입, 길이, 형식) |
| SECURITY-06 | 최소 권한 원칙 (admin/table role 분리) |
| SECURITY-08 | JWT 서버 측 검증, role 기반 접근 제어, CORS 제한 |
| SECURITY-09 | 기본 credentials 없음 (seed 데이터도 변경 권장), 에러 시 내부 정보 미노출 |
| SECURITY-10 | 의존성 버전 고정 (requirements.txt, package-lock.json) |
| SECURITY-11 | 인증 로직 전용 모듈 분리, rate limiting |
| SECURITY-12 | bcrypt 해싱, 세션 만료, 브루트포스 보호 (5회/15분), HttpOnly/Secure 쿠키 속성 |
| SECURITY-15 | 전역 에러 핸들러, fail-closed, 리소스 정리 |

## 가용성
- 로컬 개발 환경 (Docker Compose) — 고가용성 불필요
- 서비스 재시작 시 세션 유지 (JWT 기반, 서버 stateless)

## 유지보수성
- Repository 패턴으로 DB 접근 분리
- Pydantic 스키마로 입출력 검증
- 구조화된 프로젝트 레이아웃 (routers/services/repositories/models)
