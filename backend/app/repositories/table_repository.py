from __future__ import annotations
from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload
from app.models.table import Table, TableSession
from app.models.order import Order, OrderHistory


class TableRepository:
    @staticmethod
    def get_by_store_and_number(db: Session, store_id: str, table_number: int) -> Table | None:
        return db.query(Table).filter(Table.store_id == store_id, Table.table_number == table_number).first()

    @staticmethod
    def get_by_id(db: Session, table_id: str, store_id: str) -> Table | None:
        return db.query(Table).filter(Table.id == table_id, Table.store_id == store_id).first()

    @staticmethod
    def get_all(db: Session, store_id: str) -> list[Table]:
        return db.query(Table).filter(Table.store_id == store_id).order_by(Table.table_number).all()

    @staticmethod
    def create(db: Session, table: Table) -> Table:
        db.add(table)
        db.commit()
        db.refresh(table)
        return table


class TableSessionRepository:
    @staticmethod
    def get_active_session(db: Session, table_id: str) -> TableSession | None:
        return db.query(TableSession).filter(
            TableSession.table_id == table_id, TableSession.is_active == True
        ).first()

    @staticmethod
    def close_session(db: Session, session: TableSession):
        session.is_active = False
        session.ended_at = datetime.now(timezone.utc)

    @staticmethod
    def create_session(db: Session, table_id: str) -> TableSession:
        s = TableSession(table_id=table_id)
        db.add(s)
        return s


class OrderHistoryRepository:
    @staticmethod
    def bulk_create(db: Session, histories: list[OrderHistory]):
        db.add_all(histories)

    @staticmethod
    def get_by_table(db: Session, table_id: str, date_from: datetime | None = None, date_to: datetime | None = None) -> list[OrderHistory]:
        q = db.query(OrderHistory).filter(OrderHistory.table_id == table_id)
        if date_from:
            q = q.filter(OrderHistory.ordered_at >= date_from)
        if date_to:
            q = q.filter(OrderHistory.ordered_at <= date_to)
        return q.order_by(OrderHistory.ordered_at.desc()).all()
