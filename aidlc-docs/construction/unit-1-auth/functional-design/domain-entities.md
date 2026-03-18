# Domain Entities (전체 시스템)

Unit 1에서 전체 DB 모델을 정의합니다. 후속 Unit에서 이 모델을 사용합니다.

---

## Store (매장)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 매장 고유 식별자 |
| name | String(100) | NOT NULL | 매장명 |
| store_identifier | String(50) | UNIQUE, NOT NULL | 매장 식별자 (로그인용) |
| created_at | DateTime | NOT NULL, DEFAULT NOW | 생성 시각 |

---

## Admin (관리자)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 관리자 고유 식별자 |
| store_id | UUID | FK(Store), NOT NULL | 소속 매장 |
| username | String(50) | NOT NULL | 사용자명 |
| password_hash | String(255) | NOT NULL | bcrypt 해시 비밀번호 |
| failed_login_attempts | Integer | DEFAULT 0 | 연속 로그인 실패 횟수 |
| locked_until | DateTime | NULLABLE | 잠금 해제 시각 |
| created_at | DateTime | NOT NULL, DEFAULT NOW | 생성 시각 |

**UNIQUE**: (store_id, username)

---

## Table (테이블)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 테이블 고유 식별자 |
| store_id | UUID | FK(Store), NOT NULL | 소속 매장 |
| table_number | Integer | NOT NULL | 테이블 번호 |
| password_hash | String(255) | NOT NULL | bcrypt 해시 비밀번호 |
| created_at | DateTime | NOT NULL, DEFAULT NOW | 생성 시각 |

**UNIQUE**: (store_id, table_number)

---

## TableSession (테이블 세션)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 세션 고유 식별자 |
| table_id | UUID | FK(Table), NOT NULL | 테이블 |
| started_at | DateTime | NOT NULL, DEFAULT NOW | 세션 시작 시각 |
| ended_at | DateTime | NULLABLE | 세션 종료 시각 (이용 완료 시) |
| is_active | Boolean | DEFAULT TRUE | 활성 세션 여부 |

---

## Category (카테고리)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 카테고리 고유 식별자 |
| store_id | UUID | FK(Store), NOT NULL | 소속 매장 |
| name | String(50) | NOT NULL | 카테고리명 |
| display_order | Integer | DEFAULT 0 | 노출 순서 |

---

## MenuItem (메뉴 항목)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 메뉴 고유 식별자 |
| category_id | UUID | FK(Category), NOT NULL | 소속 카테고리 |
| store_id | UUID | FK(Store), NOT NULL | 소속 매장 |
| name | String(100) | NOT NULL | 메뉴명 |
| price | Integer | NOT NULL, >= 0 | 가격 (원) |
| description | Text | NULLABLE | 메뉴 설명 |
| image_url | String(500) | NULLABLE | 이미지 URL |
| display_order | Integer | DEFAULT 0 | 노출 순서 |
| created_at | DateTime | NOT NULL, DEFAULT NOW | 생성 시각 |

---

## Order (주문)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 주문 고유 식별자 |
| order_number | Integer | NOT NULL, AUTO INCREMENT | 주문 번호 (매장 내 순번) |
| table_id | UUID | FK(Table), NOT NULL | 테이블 |
| session_id | UUID | FK(TableSession), NOT NULL | 테이블 세션 |
| store_id | UUID | FK(Store), NOT NULL | 매장 |
| status | Enum | NOT NULL, DEFAULT 'pending' | 상태: pending/preparing/completed |
| total_amount | Integer | NOT NULL | 총 금액 |
| created_at | DateTime | NOT NULL, DEFAULT NOW | 주문 시각 |

---

## OrderItem (주문 항목)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 주문 항목 고유 식별자 |
| order_id | UUID | FK(Order), NOT NULL | 소속 주문 |
| menu_item_id | UUID | FK(MenuItem), NOT NULL | 메뉴 항목 |
| menu_name | String(100) | NOT NULL | 주문 시점 메뉴명 (스냅샷) |
| quantity | Integer | NOT NULL, >= 1 | 수량 |
| unit_price | Integer | NOT NULL, >= 0 | 주문 시점 단가 (스냅샷) |

---

## OrderHistory (과거 주문 이력)

| 필드 | 타입 | 제약 | 설명 |
|------|------|------|------|
| id | UUID | PK | 이력 고유 식별자 |
| original_order_id | UUID | NOT NULL | 원본 주문 ID |
| order_number | Integer | NOT NULL | 주문 번호 |
| table_id | UUID | FK(Table), NOT NULL | 테이블 |
| session_id | UUID | NOT NULL | 세션 ID |
| store_id | UUID | FK(Store), NOT NULL | 매장 |
| status | String(20) | NOT NULL | 최종 상태 |
| total_amount | Integer | NOT NULL | 총 금액 |
| items_snapshot | JSON | NOT NULL | 주문 항목 스냅샷 |
| ordered_at | DateTime | NOT NULL | 원본 주문 시각 |
| completed_at | DateTime | NOT NULL, DEFAULT NOW | 이용 완료 처리 시각 |

---

## ER 관계

```
Store 1──* Admin
Store 1──* Table
Store 1──* Category
Store 1──* MenuItem
Table 1──* TableSession
Table 1──* Order
TableSession 1──* Order
Category 1──* MenuItem
Order 1──* OrderItem
MenuItem 1──* OrderItem
```
