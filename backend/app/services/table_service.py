from __future__ import annotations
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.table import Table, TableSession
from app.models.order import Order, OrderHistory
from app.repositories.table_repository import TableRepository, TableSessionRepository, OrderHistoryRepository
from app.services.auth_service import AuthService
from app.services.sse_manager import sse_manager


class TableService:
    @staticmethod
    def create(db: Session, store_id: str, table_number: int, password: str) -> Table:
        if TableRepository.get_by_store_and_number(db, store_id, table_number):
            raise HTTPException(status_code=409, detail="Table number already exists")
        table = Table(store_id=store_id, table_number=table_number, password_hash=AuthService.hash_password(password))
        table = TableRepository.create(db, table)
        session = TableSession(table_id=table.id)
        db.add(session)
        db.commit()
        return table

    @staticmethod
    def get_all(db: Session, store_id: str) -> list[dict]:
        tables = TableRepository.get_all(db, store_id)
        result = []
        for t in tables:
            active_session = TableSessionRepository.get_active_session(db, t.id)
            orders = []
            if active_session:
                orders = db.query(Order).filter(Order.session_id == active_session.id).all()
            result.append({
                "id": t.id, "table_number": t.table_number,
                "order_count": len(orders),
                "total_amount": sum(o.total_amount for o in orders),
            })
        return result

    @staticmethod
    def get_detail(db: Session, store_id: str, table_id: str) -> dict:
        table = TableRepository.get_by_id(db, table_id, store_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        active_session = TableSessionRepository.get_active_session(db, table.id)
        orders = []
        if active_session:
            orders = db.query(Order).options(joinedload(Order.items)).filter(Order.session_id == active_session.id).all()
        return {"id": table.id, "table_number": table.table_number, "orders": orders}

    @staticmethod
    async def complete(db: Session, store_id: str, table_id: str):
        table = TableRepository.get_by_id(db, table_id, store_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        active_session = TableSessionRepository.get_active_session(db, table.id)
        if not active_session:
            raise HTTPException(status_code=400, detail="No active session")

        orders = db.query(Order).options(joinedload(Order.items)).filter(Order.session_id == active_session.id).all()
        histories = []
        for o in orders:
            histories.append(OrderHistory(
                original_order_id=o.id, order_number=o.order_number, table_id=o.table_id,
                session_id=o.session_id, store_id=o.store_id,
                status=o.status.value if hasattr(o.status, 'value') else o.status,
                total_amount=o.total_amount,
                items_snapshot=[{"menu_name": i.menu_name, "quantity": i.quantity, "unit_price": i.unit_price} for i in o.items],
                ordered_at=o.created_at,
            ))
        OrderHistoryRepository.bulk_create(db, histories)
        for o in orders:
            db.delete(o)
        TableSessionRepository.close_session(db, active_session)
        TableSessionRepository.create_session(db, table.id)
        db.commit()
        await sse_manager.broadcast("session_completed", {"table_id": table_id}, store_id, table_id)

    @staticmethod
    def update(db: Session, store_id: str, table_id: str, password: str | None) -> Table:
        table = TableRepository.get_by_id(db, table_id, store_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        if password:
            table.password_hash = AuthService.hash_password(password)
        db.commit()
        db.refresh(table)
        return table

    @staticmethod
    def get_history(db: Session, store_id: str, table_id: str, date_from: datetime | None, date_to: datetime | None) -> list[OrderHistory]:
        table = TableRepository.get_by_id(db, table_id, store_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found")
        return OrderHistoryRepository.get_by_table(db, table_id, date_from, date_to)
