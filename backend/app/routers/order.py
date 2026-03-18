from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_table, get_current_admin
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import OrderService
from app.models.table import Table

router = APIRouter()


def _enrich(order, db):
    """Add table numbers to gift orders for response."""
    resp = OrderResponse.model_validate(order)
    if order.gift_from_table_id:
        t = db.query(Table).filter(Table.id == order.gift_from_table_id).first()
        resp.gift_from_table_number = t.table_number if t else None
    if order.gift_to_table_id:
        t = db.query(Table).filter(Table.id == order.gift_to_table_id).first()
        resp.gift_to_table_number = t.table_number if t else None
    return resp


@router.post("", response_model=OrderResponse, status_code=201)
async def create_order(body: OrderCreate, db: Session = Depends(get_db), table_info=Depends(get_current_table)):
    order = await OrderService.create(
        db, table_info["store_id"], table_info["table"].id,
        table_info["session_id"], [i.model_dump() for i in body.items],
        gift_to_table=body.gift_to_table, gift_message=body.gift_message,
    )
    return _enrich(order, db)


@router.get("", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db), table_info=Depends(get_current_table)):
    orders = OrderService.get_by_session(db, table_info["session_id"], table_info["table"].id)
    return [_enrich(o, db) for o in orders]


@router.get("/admin", response_model=list[OrderResponse])
def get_orders_admin(table_id: str | None = None, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    if table_id:
        orders = OrderService.get_by_table(db, table_id)
    else:
        orders = OrderService.get_by_store(db, admin.store_id)
    return [_enrich(o, db) for o in orders]


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: str, body: OrderStatusUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    order = await OrderService.update_status(db, admin.store_id, order_id, body.status)
    return _enrich(order, db)


@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    await OrderService.delete(db, admin.store_id, order_id)
