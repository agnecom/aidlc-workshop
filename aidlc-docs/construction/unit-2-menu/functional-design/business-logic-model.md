# Business Logic Model - Unit 2 (메뉴)

## 메뉴 조회 (고객)

```
GET /api/categories → CategoryService.get_all(store_id)
  → Category 목록 반환 (display_order 순)

GET /api/menus?category_id → MenuService.get_by_category(store_id, category_id)
  → MenuItem 목록 반환 (display_order 순)

GET /api/menus → MenuService.get_all(store_id)
  → 전체 MenuItem 목록 반환 (카테고리별, display_order 순)
```

## 메뉴 CRUD (관리자)

```
POST /api/menus (multipart/form-data)
  → 입력 검증 (필수 필드, 가격 >= 0)
  → 이미지 파일 있으면 → FileStorage.save() → image_url 생성
  → MenuItem 생성
  → 201 반환

PUT /api/menus/{id} (multipart/form-data)
  → MenuItem 존재 확인 → 없으면 404
  → 입력 검증
  → 이미지 파일 있으면 → 기존 이미지 삭제 → FileStorage.save()
  → MenuItem 업데이트
  → 200 반환

DELETE /api/menus/{id}
  → MenuItem 존재 확인 → 없으면 404
  → 이미지 있으면 FileStorage.delete()
  → MenuItem 삭제
  → 204 반환

PATCH /api/menus/{id}/order
  → display_order 업데이트
  → 200 반환
```

## FileStorage

```
save(file, filename) → /uploads/{uuid}_{filename} 저장 → URL 반환
delete(image_url) → 파일 삭제
```
