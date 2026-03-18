from __future__ import annotations
from pydantic import BaseModel, Field


class CategoryResponse(BaseModel):
    id: str
    name: str
    display_order: int

    model_config = {"from_attributes": True}
