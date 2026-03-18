"""Initialize seed data: store, admin, tables, categories, menus with images."""
import os
import uuid
import urllib.request

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.store import Store
from app.models.admin import Admin
from app.models.table import Table, TableSession
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.services.auth_service import AuthService

UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/app/uploads")

MENU_DATA = {
    "인기 메뉴": [
        ("양념치킨", 19000, "바삭한 튀김옷에 달콤 매콤한 양념", "all"),
        ("간장치킨", 19000, "짭짤 달콤한 간장 소스의 치킨", "all"),
        ("크림파스타", 14000, "부드러운 크림소스 파스타", "winter"),
        ("로제파스타", 14500, "매콤 크리미한 로제소스", "all"),
    ],
    "메인 요리": [
        ("한우 불고기", 28000, "프리미엄 한우 불고기", "autumn"),
        ("돼지갈비", 22000, "양념 돼지갈비 구이", "all"),
        ("연어 스테이크", 24000, "노르웨이산 연어 스테이크", "spring"),
        ("함박 스테이크", 16000, "수제 함박 스테이크", "winter"),
    ],
    "사이드": [
        ("감자튀김", 7000, "바삭한 감자튀김", "all"),
        ("치즈볼", 6500, "모짜렐라 치즈볼 6개", "winter"),
        ("떡볶이", 8000, "매콤 달콤 떡볶이", "all"),
        ("시저 샐러드", 9000, "신선한 시저 샐러드", "summer"),
    ],
    "음료": [
        ("생맥주 500ml", 5000, "시원한 생맥주", "summer"),
        ("소주", 5000, "참이슬 후레쉬", "all"),
        ("콜라", 2500, "코카콜라 355ml", "summer"),
        ("아메리카노", 4500, "원두 아메리카노", "all"),
    ],
    "디저트": [
        ("티라미수", 8500, "이탈리안 티라미수", "all"),
        ("바닐라 아이스크림", 5500, "프리미엄 바닐라", "summer"),
        ("초코 브라우니", 7000, "진한 초코 브라우니", "winter"),
        ("치즈케이크", 8000, "뉴욕 스타일 치즈케이크", "spring"),
    ],
}

# Unsplash 무료 이미지 (food 키워드, 400x300 크기)
IMAGE_URLS = [
    "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400&h=300&fit=crop",  # 양념치킨
    "https://images.unsplash.com/photo-1569058242567-93de6f36f8eb?w=400&h=300&fit=crop",  # 간장치킨
    "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?w=400&h=300&fit=crop",  # 크림파스타
    "https://images.unsplash.com/photo-1635264685671-739e75e73e0f?w=400&h=300&fit=crop",  # 로제파스타
    "https://images.unsplash.com/photo-1590947132387-155cc02f3212?w=400&h=300&fit=crop",  # 불고기
    "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=300&fit=crop",  # 돼지갈비
    "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400&h=300&fit=crop",  # 연어
    "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop",  # 함박
    "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&h=300&fit=crop",  # 감자튀김
    "https://images.unsplash.com/photo-1531749668029-2db88e4276c7?w=400&h=300&fit=crop",  # 치즈볼
    "https://images.unsplash.com/photo-1635963662853-f0ef27a16506?w=400&h=300&fit=crop",  # 떡볶이
    "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&h=300&fit=crop",  # 샐러드
    "https://images.unsplash.com/photo-1608270586620-248524c67de9?w=400&h=300&fit=crop",  # 맥주
    "https://images.unsplash.com/photo-1517659649778-bae24b8c2e26?w=400&h=300&fit=crop",  # 소주
    "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=400&h=300&fit=crop",  # 콜라
    "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400&h=300&fit=crop",  # 아메리카노
    "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop",  # 티라미수
    "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=400&h=300&fit=crop",  # 아이스크림
    "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=400&h=300&fit=crop",  # 브라우니
    "https://images.unsplash.com/photo-1524351199678-941a58a3df50?w=400&h=300&fit=crop",  # 치즈케이크
]


def download_image(url, filename):
    """Download image and save to uploads directory."""
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        return
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"  Downloaded: {filename}")
    except Exception as e:
        print(f"  Failed to download {filename}: {e}")


def init_seed_data():
    db: Session = SessionLocal()
    try:
        existing = db.query(Store).filter(Store.store_identifier == "store001").first()
        if existing:
            print("Seed data already exists. Skipping.")
            return

        # Store
        store = Store(name="기본 매장", store_identifier="store001")
        db.add(store)
        db.flush()

        # Admin
        admin = Admin(
            store_id=store.id,
            username="admin",
            password_hash=AuthService.hash_password("admin1234"),
        )
        db.add(admin)
        db.flush()

        # Tables 1~3
        for num in range(1, 4):
            table = Table(store_id=store.id, table_number=num, password_hash=AuthService.hash_password("1234"))
            db.add(table)
            db.flush()
            session = TableSession(table_id=table.id)
            db.add(session)
        db.flush()

        # Categories & Menus
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        img_idx = 0
        cat_order = 0
        for cat_name, items in MENU_DATA.items():
            category = Category(store_id=store.id, name=cat_name, display_order=cat_order)
            db.add(category)
            db.flush()
            cat_order += 1

            for menu_order, (name, price, desc, season) in enumerate(items):
                img_filename = f"menu_{img_idx}.jpg"
                download_image(IMAGE_URLS[img_idx], img_filename)
                image_url = f"/uploads/{img_filename}" if os.path.exists(os.path.join(UPLOAD_DIR, img_filename)) else None

                menu = MenuItem(
                    store_id=store.id,
                    category_id=category.id,
                    name=name,
                    price=price,
                    description=desc,
                    image_url=image_url,
                    display_order=menu_order,
                    season_tag=season,
                )
                db.add(menu)
                img_idx += 1

        db.commit()
        print("Seed data created: store=store001, admin=admin/admin1234, tables=1~3 (pw:1234), 5 categories, 20 menus with images")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)
    init_seed_data()
