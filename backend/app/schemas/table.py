from __future__ import annotations
from pydantic import BaseModel, Field


class TableCreateRequest(BaseModel):
    table_number: int = Field(..., ge=1)
    password: str = Field(..., min_length=4, max_length=128)


class TableUpdateRequest(BaseModel):
    password: str | None = Field(None, min_length=4, max_length=128)


class TableResponse(BaseModel):
    id: str
    table_number: int
    store_id: str

    model_config = {"from_attributes": True}


class TableSummaryResponse(BaseModel):
    id: str
    table_number: int
    order_count: int = 0
    total_amount: int = 0

    model_config = {"from_attributes": True}


class TableDetailResponse(BaseModel):
    id: str
    table_number: int
    orders: list = []

    model_config = {"from_attributes": True}


class OrderHistoryResponse(BaseModel):
    id: str
    original_order_id: str
    order_number: int
    status: str
    total_amount: int
    items_snapshot: list | dict
    ordered_at: str
    completed_at: str

    model_config = {"from_attributes": True}
