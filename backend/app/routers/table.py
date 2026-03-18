from __future__ import annotations
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_admin, get_current_table
from app.schemas.table import (
    TableCreateRequest, TableUpdateRequest, TableResponse,
    TableSummaryResponse, TableDetailResponse, OrderHistoryResponse,
)
from app.services.table_service import TableService

router = APIRouter()


@router.get("/list/active")
def get_active_tables(db: Session = Depends(get_db), table_info=Depends(get_current_table)):
    """Get active table numbers for gift sending (customer endpoint)."""
    from app.models.table import Table
    tables = db.query(Table).filter(Table.store_id == table_info["store_id"]).order_by(Table.table_number).all()
    return [{"table_number": t.table_number} for t in tables if t.id != table_info["table"].id]


@router.post("", response_model=TableResponse, status_code=201)
def create_table(body: TableCreateRequest, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return TableService.create(db, admin.store_id, body.table_number, body.password)


@router.get("", response_model=list[TableSummaryResponse])
def get_tables(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return TableService.get_all(db, admin.store_id)


@router.get("/{table_id}")
def get_table_detail(table_id: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return TableService.get_detail(db, admin.store_id, table_id)


@router.put("/{table_id}", response_model=TableResponse)
def update_table(table_id: str, body: TableUpdateRequest, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return TableService.update(db, admin.store_id, table_id, body.password)


@router.post("/{table_id}/complete", status_code=204)
async def complete_table(table_id: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    await TableService.complete(db, admin.store_id, table_id)


@router.get("/{table_id}/history", response_model=list[OrderHistoryResponse])
def get_table_history(
    table_id: str,
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    return TableService.get_history(db, admin.store_id, table_id, date_from, date_to)
