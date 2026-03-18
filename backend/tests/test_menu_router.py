from __future__ import annotations
from app.models.store import Store
from app.models.admin import Admin
from app.models.category import Category
from app.services.auth_service import AuthService
from app.dependencies.auth import create_access_token


class TestMenuRouter:
    def _seed(self, db):
        store = Store(name="Test", store_identifier="test001")
        db.add(store)
        db.flush()
        admin = Admin(store_id=store.id, username="admin", password_hash=AuthService.hash_password("pw"))
        db.add(admin)
        cat = Category(store_id=store.id, name="Main", display_order=0)
        db.add(cat)
        db.commit()
        token = create_access_token({"sub": admin.id, "store_id": store.id, "role": "admin"})
        return store, admin, cat, token

    def test_create_menu(self, client, db):
        store, admin, cat, token = self._seed(db)
        resp = client.post("/api/menus", data={
            "name": "Burger", "price": "10000", "category_id": cat.id, "description": "Tasty"
        }, headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 201
        assert resp.json()["name"] == "Burger"

    def test_get_menus_admin(self, client, db):
        store, admin, cat, token = self._seed(db)
        client.post("/api/menus", data={"name": "A", "price": "1000", "category_id": cat.id},
                     headers={"Authorization": f"Bearer {token}"})
        resp = client.get("/api/menus/admin", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_delete_menu(self, client, db):
        store, admin, cat, token = self._seed(db)
        create_resp = client.post("/api/menus", data={"name": "A", "price": "1000", "category_id": cat.id},
                                  headers={"Authorization": f"Bearer {token}"})
        menu_id = create_resp.json()["id"]
        resp = client.delete(f"/api/menus/{menu_id}", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 204

    def test_update_menu_order(self, client, db):
        store, admin, cat, token = self._seed(db)
        create_resp = client.post("/api/menus", data={"name": "A", "price": "1000", "category_id": cat.id},
                                  headers={"Authorization": f"Bearer {token}"})
        menu_id = create_resp.json()["id"]
        resp = client.patch(f"/api/menus/{menu_id}/order", json={"display_order": 5},
                            headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["display_order"] == 5
