from __future__ import annotations
import asyncio

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from app.dependencies.auth import get_current_admin, get_current_table
from app.services.sse_manager import sse_manager

router = APIRouter()


async def _event_stream(queue: asyncio.Queue, key: str, request: Request):
    try:
        while True:
            if await request.is_disconnected():
                break
            try:
                message = await asyncio.wait_for(queue.get(), timeout=30)
                yield message
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"
    finally:
        sse_manager.disconnect(key, queue)


@router.get("/table")
def sse_table(request: Request, table_info=Depends(get_current_table)):
    key = f"table:{table_info['table'].id}"
    queue = sse_manager.connect(key)
    return StreamingResponse(_event_stream(queue, key, request), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.get("/admin")
def sse_admin(request: Request, admin=Depends(get_current_admin)):
    key = f"admin:{admin.store_id}"
    queue = sse_manager.connect(key)
    return StreamingResponse(_event_stream(queue, key, request), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
