# NFR Requirements - Unit 2 (메뉴)

Unit 1에서 정의된 NFR 기반 적용. 추가 사항:

## 보안
- SECURITY-05: 메뉴 입력 검증 (name 길이, price 범위, 이미지 파일 형식/크기)
- SECURITY-08: 메뉴 CRUD는 admin role만 접근, 조회는 table role도 가능
- SECURITY-09: 이미지 업로드 시 파일 확장자 화이트리스트 검증

## 성능
- 메뉴 목록 조회: 200ms 이내 (소규모 데이터)
- 이미지 업로드: 5MB 제한
