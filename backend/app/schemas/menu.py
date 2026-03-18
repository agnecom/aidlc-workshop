from __future__ import annotations
from pydantic import BaseModel, Field


class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: int = Field(..., ge=0)
    description: str | None = None
    category_id: str = Field(..., min_length=1)
    display_order: int = Field(default=0)


class MenuItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    price: int | None = Field(None, ge=0)
    description: str | None = None
    category_id: str | None = None
    display_order: int | None = None


class MenuItemResponse(BaseModel):
    id: str
    name: str
    price: int
    description: str | None
    image_url: str | None
    category_id: str
    display_order: int

    model_config = {"from_attributes": True}


class DisplayOrderUpdate(BaseModel):
    display_order: int = Field(..., ge=0)
