from __future__ import annotations
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem, OrderStatus
from app.models.menu_item import MenuItem
from app.models.table import Table
from app.repositories.order_repository import OrderRepository
from app.services.sse_manager import sse_manager

VALID_TRANSITIONS = {
    OrderStatus.PENDING: OrderStatus.PREPARING,
    OrderStatus.PREPARING: OrderStatus.COMPLETED,
}


class OrderService:
    @staticmethod
    async def create(db: Session, store_id: str, table_id: str, session_id: str,
                     items_data: list[dict], gift_to_table: int | None = None,
                     gift_message: str | None = None) -> Order:
        total = 0
        order_items = []
        for item in items_data:
            menu = db.query(MenuItem).filter(MenuItem.id == item["menu_item_id"], MenuItem.store_id == store_id).first()
            if not menu:
                raise HTTPException(status_code=404, detail=f"Menu item not found: {item['menu_item_id']}")
            subtotal = menu.price * item["quantity"]
            total += subtotal
            order_items.append(OrderItem(
                menu_item_id=menu.id, menu_name=menu.name,
                quantity=item["quantity"], unit_price=menu.price,
            ))

        # Gift handling
        gift_to_table_id = None
        if gift_to_table is not None:
            target = db.query(Table).filter(Table.store_id == store_id, Table.table_number == gift_to_table).first()
            if not target:
                raise HTTPException(status_code=404, detail=f"테이블 {gift_to_table}번을 찾을 수 없습니다")
            if target.id == table_id:
                raise HTTPException(status_code=400, detail="자신의 테이블에는 선물할 수 없습니다")
            gift_to_table_id = target.id

        order_number = OrderRepository.get_next_order_number(db, store_id)
        order = Order(
            order_number=order_number, table_id=table_id, session_id=session_id,
            store_id=store_id, total_amount=total, items=order_items,
            is_gift=gift_to_table_id is not None,
            gift_from_table_id=table_id if gift_to_table_id else None,
            gift_to_table_id=gift_to_table_id,
            gift_message=gift_message,
        )
        order = OrderRepository.create(db, order)

        # Record custom metric
        try:
            from app.telemetry import orders_created
            orders_created.add(1, {"gift": str(gift_to_table_id is not None)})
        except Exception:
            pass
        await sse_manager.broadcast("new_order", _order_dict(db, order), store_id, table_id)
        # Also notify the gift recipient table
        if gift_to_table_id:
            await sse_manager.broadcast("gift_received", _order_dict(db, order), store_id, gift_to_table_id)
            # Auto-send chat message with gift details
            from app.models.message import TableMessage
            from_table = db.query(Table).filter(Table.id == table_id).first()
            to_table = db.query(Table).filter(Table.id == gift_to_table_id).first()
            items_text = ", ".join(f"{i.menu_name}({i.unit_price:,}원)x{i.quantity}" for i in order.items)
            chat_msg = f"🎁 선물을 보냈습니다!\n{items_text}\n총 {order.total_amount:,}원"
            if gift_message:
                chat_msg += f'\n💌 "{gift_message}"'
            msg = TableMessage(
                store_id=store_id,
                from_table_id=table_id, to_table_id=gift_to_table_id,
                from_table_number=from_table.table_number, to_table_number=to_table.table_number,
                message=chat_msg,
            )
            db.add(msg)
            db.commit()
            db.refresh(msg)
            msg_data = {
                "id": msg.id, "from_table_number": msg.from_table_number,
                "to_table_number": msg.to_table_number, "message": msg.message,
                "created_at": str(msg.created_at),
            }
            await sse_manager.broadcast("new_message", msg_data, store_id, gift_to_table_id)
            await sse_manager.broadcast("new_message", msg_data, store_id, table_id)

        return order

    @staticmethod
    async def update_status(db: Session, store_id: str, order_id: str, new_status: str) -> Order:
        order = OrderRepository.get_by_id(db, order_id, store_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        current = OrderStatus(order.status)
        target = OrderStatus(new_status)
        if VALID_TRANSITIONS.get(current) != target:
            raise HTTPException(status_code=400, detail=f"Invalid transition: {current.value} → {target.value}")
        order.status = target
        db.commit()
        db.refresh(order)
        await sse_manager.broadcast("order_updated", _order_dict(db, order), store_id, order.table_id)
        if order.gift_to_table_id:
            await sse_manager.broadcast("order_updated", _order_dict(db, order), store_id, order.gift_to_table_id)

        # 주문 완료 시 AI 메뉴 추천
        if target == OrderStatus.COMPLETED:
            from app.services.recommendation_service import RecommendationService
            exclude = [i.menu_item_id for i in order.items]
            target_table = order.gift_to_table_id or order.table_id
            recs = RecommendationService.recommend(db, store_id, exclude, limit=3)
            if recs:
                await sse_manager.broadcast("menu_recommendation", {
                    "order_id": order.id, "order_number": order.order_number, "recommendations": recs,
                }, store_id, target_table)
                try:
                    from app.telemetry import recommendations_generated
                    recommendations_generated.add(1)
                except Exception:
                    pass

        return order

    @staticmethod
    async def delete(db: Session, store_id: str, order_id: str):
        order = OrderRepository.get_by_id(db, order_id, store_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        table_id = order.table_id
        gift_to = order.gift_to_table_id
        OrderRepository.delete(db, order)
        await sse_manager.broadcast("order_deleted", {"order_id": order_id, "table_id": table_id}, store_id, table_id)
        if gift_to:
            await sse_manager.broadcast("order_deleted", {"order_id": order_id, "table_id": gift_to}, store_id, gift_to)

    @staticmethod
    def get_by_session(db: Session, session_id: str, table_id: str | None = None) -> list[Order]:
        orders = OrderRepository.get_by_session(db, session_id)
        if table_id:
            # Also include gifts received by this table
            gifts = db.query(Order).filter(Order.gift_to_table_id == table_id, Order.store_id == orders[0].store_id if orders else "").all() if table_id else []
            if not gifts and table_id:
                gifts = db.query(Order).filter(Order.gift_to_table_id == table_id).all()
            seen = {o.id for o in orders}
            for g in gifts:
                if g.id not in seen:
                    orders.append(g)
        return orders

    @staticmethod
    def get_by_store(db: Session, store_id: str) -> list[Order]:
        return OrderRepository.get_by_store(db, store_id)

    @staticmethod
    def get_by_table(db: Session, table_id: str) -> list[Order]:
        return OrderRepository.get_by_table(db, table_id)


def _order_dict(db: Session, order: Order) -> dict:
    from_num = None
    to_num = None
    if order.gift_from_table_id:
        t = db.query(Table).filter(Table.id == order.gift_from_table_id).first()
        from_num = t.table_number if t else None
    if order.gift_to_table_id:
        t = db.query(Table).filter(Table.id == order.gift_to_table_id).first()
        to_num = t.table_number if t else None
    return {
        "id": order.id, "order_number": order.order_number, "table_id": order.table_id,
        "session_id": order.session_id, "status": order.status.value if hasattr(order.status, 'value') else order.status,
        "total_amount": order.total_amount, "created_at": str(order.created_at),
        "is_gift": order.is_gift, "gift_from_table_id": order.gift_from_table_id,
        "gift_to_table_id": order.gift_to_table_id, "gift_message": order.gift_message,
        "gift_from_table_number": from_num, "gift_to_table_number": to_num,
        "items": [{"id": i.id, "menu_item_id": i.menu_item_id, "menu_name": i.menu_name,
                    "quantity": i.quantity, "unit_price": i.unit_price} for i in order.items],
    }
