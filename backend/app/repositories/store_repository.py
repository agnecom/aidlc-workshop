from __future__ import annotations
from sqlalchemy.orm import Session
from app.models.store import Store


class StoreRepository:
    @staticmethod
    def get_by_identifier(db: Session, store_identifier: str) -> Store | None:
        return db.query(Store).filter(Store.store_identifier == store_identifier).first()
