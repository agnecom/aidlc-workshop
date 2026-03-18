# Business Rules - Unit 2 (메뉴)

## BR-M01: 메뉴 필수 필드
- name (1~100자), price (>= 0), category_id 필수

## BR-M02: 가격 범위
- price >= 0, 정수 (원 단위)

## BR-M03: 이미지 파일 형식
- 허용: jpg, jpeg, png, gif, webp
- 최대 크기: 5MB

## BR-M04: 메뉴 노출 순서
- display_order 기본값 0
- 같은 순서일 경우 생성 시간 순

## BR-M05: 카테고리 필수
- 메뉴는 반드시 하나의 카테고리에 속해야 함
- 카테고리 삭제 시 해당 메뉴도 삭제 (cascade)

## BR-M06: 매장 범위 제한
- 메뉴 조회/관리는 현재 인증된 매장의 데이터만 접근 가능
