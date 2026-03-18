from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.database import get_db
from app.dependencies.auth import get_current_table
from app.models.message import TableMessage
from app.models.table import Table
from app.schemas.message import MessageSend, MessageResponse
from app.services.sse_manager import sse_manager

router = APIRouter()


@router.post("", response_model=MessageResponse, status_code=201)
async def send_message(body: MessageSend, db: Session = Depends(get_db), table_info=Depends(get_current_table)):
    my_table = table_info["table"]
    store_id = table_info["store_id"]

    if body.to_table_number == my_table.table_number:
        raise HTTPException(status_code=400, detail="자신에게 메시지를 보낼 수 없습니다")

    target = db.query(Table).filter(Table.store_id == store_id, Table.table_number == body.to_table_number).first()
    if not target:
        raise HTTPException(status_code=404, detail=f"테이블 {body.to_table_number}번을 찾을 수 없습니다")

    msg = TableMessage(
        store_id=store_id,
        from_table_id=my_table.id, to_table_id=target.id,
        from_table_number=my_table.table_number, to_table_number=target.table_number,
        message=body.message,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    msg_data = {
        "id": msg.id, "from_table_number": msg.from_table_number,
        "to_table_number": msg.to_table_number, "message": msg.message,
        "created_at": str(msg.created_at),
    }
    await sse_manager.broadcast("new_message", msg_data, store_id, target.id)
    await sse_manager.broadcast("new_message", msg_data, store_id, my_table.id)

    resp = MessageResponse.model_validate(msg)
    resp.is_mine = True
    return resp


@router.get("/{table_number}", response_model=list[MessageResponse])
def get_messages(table_number: int, db: Session = Depends(get_db), table_info=Depends(get_current_table)):
    my_table = table_info["table"]
    store_id = table_info["store_id"]

    target = db.query(Table).filter(Table.store_id == store_id, Table.table_number == table_number).first()
    if not target:
        raise HTTPException(status_code=404, detail=f"테이블 {table_number}번을 찾을 수 없습니다")

    messages = db.query(TableMessage).filter(
        TableMessage.store_id == store_id,
        or_(
            and_(TableMessage.from_table_id == my_table.id, TableMessage.to_table_id == target.id),
            and_(TableMessage.from_table_id == target.id, TableMessage.to_table_id == my_table.id),
        )
    ).order_by(TableMessage.created_at).all()

    result = []
    for m in messages:
        resp = MessageResponse.model_validate(m)
        resp.is_mine = (m.from_table_id == my_table.id)
        result.append(resp)
    return result
