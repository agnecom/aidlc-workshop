from __future__ import annotations
from sqlalchemy.orm import Session
from app.models.menu_item import MenuItem


class MenuRepository:
    @staticmethod
    def get_by_id(db: Session, menu_id: str, store_id: str) -> MenuItem | None:
        return db.query(MenuItem).filter(MenuItem.id == menu_id, MenuItem.store_id == store_id).first()
