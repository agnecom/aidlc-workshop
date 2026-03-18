from __future__ import annotations
from sqlalchemy.orm import Session
from app.models.admin import Admin


class AdminRepository:
    @staticmethod
    def get_by_store_and_username(db: Session, store_id: str, username: str) -> Admin | None:
        return db.query(Admin).filter(Admin.store_id == store_id, Admin.username == username).first()
