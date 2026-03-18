# Frontend Components - Unit 2 (메뉴)

## Customer Frontend - MenuView
- 카테고리 탭/버튼 목록 (상단)
- 메뉴 카드 그리드 (카테고리별 필터)
- 카드: 이미지, 메뉴명, 가격, 설명
- 카드 클릭 → 장바구니 추가 (Unit 3에서 구현, 여기서는 UI만)
- 터치 친화적 (44x44px 최소)
- API: `GET /api/categories`, `GET /api/menus`

## Admin Frontend - MenuManageView
- 카테고리별 메뉴 목록 테이블
- 메뉴 등록 폼 (모달/페이지): name, price, description, category, image upload
- 메뉴 수정 폼
- 메뉴 삭제 버튼 + 확인 팝업
- 노출 순서 변경 (드래그 또는 버튼)
- 검증 에러 표시
- API: `GET/POST/PUT/DELETE /api/menus`, `PATCH /api/menus/{id}/order`
