# NFR Design - Unit 2 (메뉴)

## 파일 업로드 패턴
- UUID prefix로 파일명 충돌 방지
- 확장자 화이트리스트 검증 (서버 측)
- 파일 크기 제한 (FastAPI UploadFile)

## 권한 분리
- 조회 API: get_current_table 또는 get_current_admin
- CRUD API: get_current_admin만 허용
