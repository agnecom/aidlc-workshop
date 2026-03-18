from __future__ import annotations
from app.models.store import Store
from app.models.admin import Admin
from app.models.table import Table, TableSession
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.services.auth_service import AuthService
from app.dependencies.auth import create_access_token


class TestOrderRouter:
    def _seed(self, db):
        store = Store(name="Test", store_identifier="test001")
        db.add(store)
        db.flush()
        admin = Admin(store_id=store.id, username="admin", password_hash=AuthService.hash_password("pw"))
        db.add(admin)
        table = Table(store_id=store.id, table_number=1, password_hash=AuthService.hash_password("pw"))
        db.add(table)
        db.flush()
        session = TableSession(table_id=table.id)
        db.add(session)
        cat = Category(store_id=store.id, name="Main", display_order=0)
        db.add(cat)
        db.flush()
        menu = MenuItem(store_id=store.id, category_id=cat.id, name="Burger", price=10000, display_order=0)
        db.add(menu)
        db.commit()
        admin_token = create_access_token({"sub": admin.id, "store_id": store.id, "role": "admin"})
        table_token = create_access_token({"sub": table.id, "table_id": table.id, "session_id": session.id, "store_id": store.id, "role": "table"})
        return store, admin, table, session, menu, admin_token, table_token

    def test_create_order(self, client, db):
        store, admin, table, session, menu, admin_token, table_token = self._seed(db)
        resp = client.post("/api/orders", json={"items": [{"menu_item_id": menu.id, "quantity": 2}]},
                           headers={"Authorization": f"Bearer {table_token}"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["total_amount"] == 20000
        assert data["order_number"] == 1
        assert len(data["items"]) == 1

    def test_get_orders_by_session(self, client, db):
        store, admin, table, session, menu, admin_token, table_token = self._seed(db)
        client.post("/api/orders", json={"items": [{"menu_item_id": menu.id, "quantity": 1}]},
                    headers={"Authorization": f"Bearer {table_token}"})
        resp = client.get("/api/orders", headers={"Authorization": f"Bearer {table_token}"})
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_update_order_status(self, client, db):
        store, admin, table, session, menu, admin_token, table_token = self._seed(db)
        create_resp = client.post("/api/orders", json={"items": [{"menu_item_id": menu.id, "quantity": 1}]},
                                  headers={"Authorization": f"Bearer {table_token}"})
        order_id = create_resp.json()["id"]
        resp = client.patch(f"/api/orders/{order_id}/status", json={"status": "preparing"},
                            headers={"Authorization": f"Bearer {admin_token}"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "preparing"

    def test_invalid_status_transition(self, client, db):
        store, admin, table, session, menu, admin_token, table_token = self._seed(db)
        create_resp = client.post("/api/orders", json={"items": [{"menu_item_id": menu.id, "quantity": 1}]},
                                  headers={"Authorization": f"Bearer {table_token}"})
        order_id = create_resp.json()["id"]
        resp = client.patch(f"/api/orders/{order_id}/status", json={"status": "completed"},
                            headers={"Authorization": f"Bearer {admin_token}"})
        assert resp.status_code == 400

    def test_delete_order(self, client, db):
        store, admin, table, session, menu, admin_token, table_token = self._seed(db)
        create_resp = client.post("/api/orders", json={"items": [{"menu_item_id": menu.id, "quantity": 1}]},
                                  headers={"Authorization": f"Bearer {table_token}"})
        order_id = create_resp.json()["id"]
        resp = client.delete(f"/api/orders/{order_id}", headers={"Authorization": f"Bearer {admin_token}"})
        assert resp.status_code == 204

    def test_empty_cart_rejected(self, client, db):
        store, admin, table, session, menu, admin_token, table_token = self._seed(db)
        resp = client.post("/api/orders", json={"items": []},
                           headers={"Authorization": f"Bearer {table_token}"})
        assert resp.status_code == 422
