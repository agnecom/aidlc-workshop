from __future__ import annotations
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.menu_item import MenuItem
from app.services.file_storage import FileStorage


class MenuService:
    @staticmethod
    def get_all(db: Session, store_id: str, category_id: str | None = None) -> list[MenuItem]:
        q = db.query(MenuItem).filter(MenuItem.store_id == store_id)
        if category_id:
            q = q.filter(MenuItem.category_id == category_id)
        return q.order_by(MenuItem.display_order, MenuItem.created_at).all()

    @staticmethod
    async def create(db: Session, store_id: str, name: str, price: int, description: str | None,
                     category_id: str, display_order: int, image: UploadFile | None) -> MenuItem:
        image_url = None
        if image and image.filename:
            content = await image.read()
            image_url = FileStorage.save(content, image.filename)

        item = MenuItem(store_id=store_id, name=name, price=price, description=description,
                        category_id=category_id, display_order=display_order, image_url=image_url)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    async def update(db: Session, store_id: str, menu_id: str, name: str | None, price: int | None,
                     description: str | None, category_id: str | None, display_order: int | None,
                     image: UploadFile | None) -> MenuItem:
        item = db.query(MenuItem).filter(MenuItem.id == menu_id, MenuItem.store_id == store_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        if name is not None: item.name = name
        if price is not None: item.price = price
        if description is not None: item.description = description
        if category_id is not None: item.category_id = category_id
        if display_order is not None: item.display_order = display_order

        if image and image.filename:
            FileStorage.delete(item.image_url)
            content = await image.read()
            item.image_url = FileStorage.save(content, image.filename)

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, store_id: str, menu_id: str):
        item = db.query(MenuItem).filter(MenuItem.id == menu_id, MenuItem.store_id == store_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        FileStorage.delete(item.image_url)
        db.delete(item)
        db.commit()

    @staticmethod
    def update_order(db: Session, store_id: str, menu_id: str, display_order: int) -> MenuItem:
        item = db.query(MenuItem).filter(MenuItem.id == menu_id, MenuItem.store_id == store_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        item.display_order = display_order
        db.commit()
        db.refresh(item)
        return item
