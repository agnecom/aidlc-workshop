# Requirements Verification Questions

테이블오더 서비스 요구사항을 분석한 결과, 아래 질문들에 대한 답변이 필요합니다.
각 질문의 [Answer]: 태그 뒤에 선택지 알파벳을 입력해 주세요.

---

## Question 1
프로젝트의 기술 스택(backend)으로 어떤 것을 사용하시겠습니까?

A) Node.js (Express/Fastify)
B) Java (Spring Boot)
C) Python (FastAPI/Django)
D) Go
E) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 2
프론트엔드 기술 스택으로 어떤 것을 사용하시겠습니까?

A) React (Next.js)
B) React (Vite/CRA)
C) Vue.js
D) Svelte
E) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 3
데이터베이스로 어떤 것을 사용하시겠습니까?

A) PostgreSQL
B) MySQL
C) MongoDB
D) DynamoDB
E) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 4
배포 환경은 어떻게 계획하고 계십니까?

A) AWS (EC2, ECS, Lambda 등)
B) 로컬/온프레미스 서버
C) Docker Compose 기반 로컬 개발 환경만 (배포는 추후 결정)
D) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 5
메뉴 이미지 관리 방식은 어떻게 하시겠습니까? (요구사항에 이미지 URL이 언급되어 있습니다)

A) 외부 이미지 URL 직접 입력 (이미지 업로드 기능 없음)
B) 서버에 이미지 파일 업로드 후 URL 자동 생성
C) 클라우드 스토리지(S3 등)에 업로드 후 URL 자동 생성
D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 6
관리자 계정은 어떻게 생성됩니까?

A) 시스템 초기 설정 시 seed 데이터로 생성 (관리자 회원가입 없음)
B) 관리자 회원가입 기능 제공
C) CLI 또는 API를 통한 수동 생성
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 7
매장(store)은 단일 매장만 지원합니까, 다중 매장을 지원합니까?

A) 단일 매장만 지원 (MVP)
B) 다중 매장 지원 (매장별 독립 운영)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 8
동시 접속 사용자 규모는 어느 정도로 예상하십니까?

A) 소규모 (테이블 10개 이하, 관리자 1~2명)
B) 중규모 (테이블 10~50개, 관리자 2~5명)
C) 대규모 (테이블 50개 이상, 관리자 5명 이상)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 9
메뉴 관리 기능은 MVP에 포함됩니까? (요구사항 3.2.4에 정의되어 있으나 MVP 범위 섹션에는 명시되지 않았습니다)

A) 포함 - 메뉴 CRUD 기능 MVP에 포함
B) 제외 - seed 데이터로 메뉴 초기화, 메뉴 관리는 추후 구현
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 10
주문 상태 실시간 업데이트(고객 화면)는 MVP에 포함됩니까? (요구사항에 "선택사항"으로 표기됨)

A) 포함 - 고객 화면에서도 SSE로 주문 상태 실시간 업데이트
B) 제외 - 고객은 페이지 새로고침으로 상태 확인 (관리자 화면만 SSE)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 11: Security Extensions
이 프로젝트에 보안 extension 규칙을 적용하시겠습니까?

A) Yes — 모든 SECURITY 규칙을 blocking constraint로 적용 (프로덕션 수준 애플리케이션에 권장)
B) No — 모든 SECURITY 규칙 건너뛰기 (PoC, 프로토타입, 실험적 프로젝트에 적합)
C) Other (please describe after [Answer]: tag below)

[Answer]: A
