from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_table, get_current_admin
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryResponse

router = APIRouter()


@router.get("", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db), _=Depends(get_current_table)):
    table_info = _
    return CategoryRepository.get_all(db, table_info["store_id"])


@router.get("/admin", response_model=list[CategoryResponse])
def get_categories_admin(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return CategoryRepository.get_all(db, admin.store_id)
