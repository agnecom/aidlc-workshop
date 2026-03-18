from __future__ import annotations
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_table, get_current_admin
from app.schemas.menu import MenuItemResponse, DisplayOrderUpdate
from app.services.menu_service import MenuService

router = APIRouter()


@router.get("", response_model=list[MenuItemResponse])
def get_menus(category_id: str | None = None, db: Session = Depends(get_db), table_info=Depends(get_current_table)):
    return MenuService.get_all(db, table_info["store_id"], category_id)


@router.get("/admin", response_model=list[MenuItemResponse])
def get_menus_admin(category_id: str | None = None, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return MenuService.get_all(db, admin.store_id, category_id)


@router.post("", response_model=MenuItemResponse, status_code=201)
async def create_menu(
    name: str = Form(...), price: int = Form(..., ge=0),
    description: str | None = Form(None), category_id: str = Form(...),
    display_order: int = Form(0), image: UploadFile | None = File(None),
    db: Session = Depends(get_db), admin=Depends(get_current_admin),
):
    return await MenuService.create(db, admin.store_id, name, price, description, category_id, display_order, image)


@router.put("/{menu_id}", response_model=MenuItemResponse)
async def update_menu(
    menu_id: str, name: str | None = Form(None), price: int | None = Form(None, ge=0),
    description: str | None = Form(None), category_id: str | None = Form(None),
    display_order: int | None = Form(None), image: UploadFile | None = File(None),
    db: Session = Depends(get_db), admin=Depends(get_current_admin),
):
    return await MenuService.update(db, admin.store_id, menu_id, name, price, description, category_id, display_order, image)


@router.delete("/{menu_id}", status_code=204)
def delete_menu(menu_id: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    MenuService.delete(db, admin.store_id, menu_id)


@router.patch("/{menu_id}/order", response_model=MenuItemResponse)
def update_menu_order(menu_id: str, body: DisplayOrderUpdate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return MenuService.update_order(db, admin.store_id, menu_id, body.display_order)
