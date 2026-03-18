from __future__ import annotations
from app.models.store import Store
from app.models.admin import Admin
from app.services.auth_service import AuthService


class TestAdminLogin:
    def _seed(self, db):
        store = Store(name="Test Store", store_identifier="test001")
        db.add(store)
        db.flush()
        admin = Admin(store_id=store.id, username="admin", password_hash=AuthService.hash_password("pass1234"))
        db.add(admin)
        db.commit()
        return store

    def test_admin_login_success(self, client, db):
        self._seed(db)
        resp = client.post("/api/auth/admin/login", json={
            "store_identifier": "test001", "username": "admin", "password": "pass1234"
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_admin_login_wrong_password(self, client, db):
        self._seed(db)
        resp = client.post("/api/auth/admin/login", json={
            "store_identifier": "test001", "username": "admin", "password": "wrong"
        })
        assert resp.status_code == 401

    def test_admin_login_invalid_store(self, client, db):
        self._seed(db)
        resp = client.post("/api/auth/admin/login", json={
            "store_identifier": "invalid", "username": "admin", "password": "pass1234"
        })
        assert resp.status_code == 401


class TestTableLogin:
    def _seed(self, db):
        store = Store(name="Test Store", store_identifier="test001")
        db.add(store)
        db.flush()
        from app.models.table import Table
        table = Table(store_id=store.id, table_number=1, password_hash=AuthService.hash_password("table123"))
        db.add(table)
        db.commit()
        return store

    def test_table_login_success(self, client, db):
        store = self._seed(db)
        resp = client.post("/api/auth/table/login", json={
            "store_id": store.id, "table_number": 1, "password": "table123"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "session_id" in data

    def test_table_login_wrong_password(self, client, db):
        store = self._seed(db)
        resp = client.post("/api/auth/table/login", json={
            "store_id": store.id, "table_number": 1, "password": "wrong"
        })
        assert resp.status_code == 401
