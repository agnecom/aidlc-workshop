from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    menu_item_id: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=99)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(..., min_length=1)
    gift_to_table: int | None = None
    gift_message: str | None = Field(None, max_length=200)


class OrderItemResponse(BaseModel):
    id: str
    menu_item_id: str
    menu_name: str
    quantity: int
    unit_price: int

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: str
    order_number: int
    table_id: str
    session_id: str
    status: str
    total_amount: int
    created_at: datetime
    is_gift: bool = False
    gift_from_table_id: str | None = None
    gift_to_table_id: str | None = None
    gift_message: str | None = None
    gift_from_table_number: int | None = None
    gift_to_table_number: int | None = None
    items: list[OrderItemResponse] = []

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(preparing|completed)$")
