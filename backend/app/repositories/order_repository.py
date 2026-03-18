from __future__ import annotations
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderItem


class OrderRepository:
    @staticmethod
    def get_next_order_number(db: Session, store_id: str) -> int:
        result = db.query(func.max(Order.order_number)).filter(Order.store_id == store_id).scalar()
        return (result or 0) + 1

    @staticmethod
    def create(db: Session, order: Order) -> Order:
        db.add(order)
        db.commit()
        db.refresh(order)
        return db.query(Order).options(joinedload(Order.items)).filter(Order.id == order.id).first()

    @staticmethod
    def get_by_id(db: Session, order_id: str, store_id: str) -> Order | None:
        return db.query(Order).options(joinedload(Order.items)).filter(
            Order.id == order_id, Order.store_id == store_id
        ).first()

    @staticmethod
    def get_by_session(db: Session, session_id: str) -> list[Order]:
        return db.query(Order).options(joinedload(Order.items)).filter(
            Order.session_id == session_id
        ).order_by(Order.created_at.desc()).all()

    @staticmethod
    def get_by_table(db: Session, table_id: str) -> list[Order]:
        return db.query(Order).options(joinedload(Order.items)).filter(
            Order.table_id == table_id
        ).order_by(Order.created_at.desc()).all()

    @staticmethod
    def get_by_store(db: Session, store_id: str) -> list[Order]:
        return db.query(Order).options(joinedload(Order.items)).filter(
            Order.store_id == store_id
        ).order_by(Order.created_at.desc()).all()

    @staticmethod
    def delete(db: Session, order: Order):
        db.delete(order)
        db.commit()
