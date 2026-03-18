from __future__ import annotations
from app.models.store import Store
from app.models.admin import Admin
from app.models.table import Table, TableSession
from app.models.category import Category
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem
from app.services.auth_service import AuthService
from app.dependencies.auth import create_access_token


class TestTableRouter:
    def _seed(self, db):
        store = Store(name="Test", store_identifier="test001")
        db.add(store)
        db.flush()
        admin = Admin(store_id=store.id, username="admin", password_hash=AuthService.hash_password("pw"))
        db.add(admin)
        db.commit()
        token = create_access_token({"sub": admin.id, "store_id": store.id, "role": "admin"})
        return store, admin, token

    def test_create_table(self, client, db):
        store, admin, token = self._seed(db)
        resp = client.post("/api/tables", json={"table_number": 1, "password": "1234"},
                           headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 201
        assert resp.json()["table_number"] == 1

    def test_duplicate_table_number(self, client, db):
        store, admin, token = self._seed(db)
        client.post("/api/tables", json={"table_number": 1, "password": "1234"},
                     headers={"Authorization": f"Bearer {token}"})
        resp = client.post("/api/tables", json={"table_number": 1, "password": "5678"},
                           headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 409

    def test_get_tables(self, client, db):
        store, admin, token = self._seed(db)
        client.post("/api/tables", json={"table_number": 1, "password": "1234"},
                     headers={"Authorization": f"Bearer {token}"})
        resp = client.get("/api/tables", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_complete_table(self, client, db):
        store, admin, token = self._seed(db)
        create_resp = client.post("/api/tables", json={"table_number": 1, "password": "1234"},
                                  headers={"Authorization": f"Bearer {token}"})
        table_id = create_resp.json()["id"]
        resp = client.post(f"/api/tables/{table_id}/complete",
                           headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 204

    def test_update_table_password(self, client, db):
        store, admin, token = self._seed(db)
        create_resp = client.post("/api/tables", json={"table_number": 1, "password": "1234"},
                                  headers={"Authorization": f"Bearer {token}"})
        table_id = create_resp.json()["id"]
        resp = client.put(f"/api/tables/{table_id}", json={"password": "newpass"},
                          headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200

    def test_get_history_empty(self, client, db):
        store, admin, token = self._seed(db)
        create_resp = client.post("/api/tables", json={"table_number": 1, "password": "1234"},
                                  headers={"Authorization": f"Bearer {token}"})
        table_id = create_resp.json()["id"]
        resp = client.get(f"/api/tables/{table_id}/history",
                          headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json() == []
