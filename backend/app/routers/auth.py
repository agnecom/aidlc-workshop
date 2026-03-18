from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import AdminLoginRequest, TableLoginRequest, TokenResponse, TableTokenResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/admin/login", response_model=TokenResponse)
def admin_login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    return AuthService.admin_login(db, request.store_identifier, request.username, request.password)


@router.post("/table/login", response_model=TableTokenResponse)
def table_login(request: TableLoginRequest, db: Session = Depends(get_db)):
    return AuthService.table_login(db, request.store_id, request.table_number, request.password)
