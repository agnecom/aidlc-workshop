# Application Design Plan

## Overview
테이블오더 서비스의 고수준 컴포넌트 식별 및 서비스 레이어 설계 계획입니다.

---

## Design Questions

아래 질문에 [Answer]: 태그 뒤에 선택지 알파벳을 입력해 주세요.

### Question 1
Backend API 구조를 어떻게 구성하시겠습니까?

A) 단일 FastAPI 앱에 Router로 도메인 분리 (auth, menu, order, table 등)
B) 도메인별 별도 FastAPI 앱 (마이크로서비스 스타일)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 2
Frontend 앱 구조를 어떻게 구성하시겠습니까?

A) 단일 Vue.js 앱에서 고객/관리자 화면을 라우팅으로 분리
B) 고객용과 관리자용을 별도 Vue.js 앱으로 분리
C) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 3
Backend과 Frontend 간 API 통신 방식은?

A) REST API (JSON) + SSE (실시간)
B) GraphQL + SSE (실시간)
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Generation Steps

- [x] components.md 생성 (컴포넌트 정의 및 책임)
- [x] component-methods.md 생성 (메서드 시그니처)
- [x] services.md 생성 (서비스 정의 및 오케스트레이션)
- [x] component-dependency.md 생성 (의존성 관계)
- [x] application-design.md 생성 (통합 문서)
- [x] 설계 완전성 및 일관성 검증
