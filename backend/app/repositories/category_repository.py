from __future__ import annotations
from sqlalchemy.orm import Session
from app.models.category import Category


class CategoryRepository:
    @staticmethod
    def get_all(db: Session, store_id: str) -> list[Category]:
        return db.query(Category).filter(Category.store_id == store_id).order_by(Category.display_order).all()
