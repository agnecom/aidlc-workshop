from __future__ import annotations
from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    store_identifier: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


class TableLoginRequest(BaseModel):
    store_id: str = Field(..., min_length=1, max_length=36)
    table_number: int = Field(..., ge=1)
    password: str = Field(..., min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TableTokenResponse(TokenResponse):
    session_id: str
