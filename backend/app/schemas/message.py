from __future__ import annotations
from pydantic import BaseModel, Field
from datetime import datetime


class MessageSend(BaseModel):
    to_table_number: int = Field(..., ge=1)
    message: str = Field(..., min_length=1, max_length=300)


class MessageResponse(BaseModel):
    id: str
    from_table_number: int
    to_table_number: int
    message: str
    created_at: datetime
    is_mine: bool = False

    model_config = {"from_attributes": True}
