import uuid
from datetime import datetime, timezone

from typing import Optional

from sqlalchemy import String, Integer, Enum, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

import enum


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)
    table_id: Mapped[str] = mapped_column(String(36), ForeignKey("tables.id"), nullable=False)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("table_sessions.id"), nullable=False)
    store_id: Mapped[str] = mapped_column(String(36), ForeignKey("stores.id"), nullable=False)
    status: Mapped[str] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # Gift fields
    is_gift: Mapped[bool] = mapped_column(Boolean, default=False)
    gift_from_table_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tables.id"), nullable=True)
    gift_to_table_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("tables.id"), nullable=True)
    gift_message: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    table = relationship("Table", back_populates="orders", foreign_keys=[table_id])
    session = relationship("TableSession", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id"), nullable=False)
    menu_item_id: Mapped[str] = mapped_column(String(36), ForeignKey("menu_items.id"), nullable=False)
    menu_name: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")


class OrderHistory(Base):
    __tablename__ = "order_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    original_order_id: Mapped[str] = mapped_column(String(36), nullable=False)
    order_number: Mapped[int] = mapped_column(Integer, nullable=False)
    table_id: Mapped[str] = mapped_column(String(36), ForeignKey("tables.id"), nullable=False)
    session_id: Mapped[str] = mapped_column(String(36), nullable=False)
    store_id: Mapped[str] = mapped_column(String(36), ForeignKey("stores.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    items_snapshot: Mapped[dict] = mapped_column(JSON, nullable=False)
    ordered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
