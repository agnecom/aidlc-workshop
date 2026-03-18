from __future__ import annotations
from app.models.store import Store
from app.models.admin import Admin
from app.models.table import Table, TableSession
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.services.auth_service import AuthService


class TestModels:
    def test_store_creation(self, db):
        store = Store(name="Test", store_identifier="t001")
        db.add(store)
        db.commit()
        assert store.id is not None

    def test_admin_creation(self, db):
        store = Store(name="Test", store_identifier="t002")
        db.add(store)
        db.flush()
        admin = Admin(store_id=store.id, username="admin", password_hash=AuthService.hash_password("pw"))
        db.add(admin)
        db.commit()
        assert admin.id is not None
        assert admin.store_id == store.id

    def test_table_and_session(self, db):
        store = Store(name="Test", store_identifier="t003")
        db.add(store)
        db.flush()
        table = Table(store_id=store.id, table_number=1, password_hash="hash")
        db.add(table)
        db.flush()
        session = TableSession(table_id=table.id)
        db.add(session)
        db.commit()
        assert session.is_active is True

    def test_category_and_menu_item(self, db):
        store = Store(name="Test", store_identifier="t004")
        db.add(store)
        db.flush()
        cat = Category(store_id=store.id, name="Main")
        db.add(cat)
        db.flush()
        item = MenuItem(category_id=cat.id, store_id=store.id, name="Burger", price=10000)
        db.add(item)
        db.commit()
        assert item.id is not None
