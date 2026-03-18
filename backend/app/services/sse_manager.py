from __future__ import annotations
import asyncio
import json
from collections import defaultdict


class SSEManager:
    def __init__(self):
        self._connections: dict[str, list[asyncio.Queue]] = defaultdict(list)

    def connect(self, key: str) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._connections[key].append(queue)
        try:
            from app.telemetry import sse_connections
            sse_connections.add(1, {"key_type": key.split(":")[0]})
        except Exception:
            pass
        return queue

    def disconnect(self, key: str, queue: asyncio.Queue):
        if key in self._connections:
            self._connections[key] = [q for q in self._connections[key] if q is not queue]
            if not self._connections[key]:
                del self._connections[key]
        try:
            from app.telemetry import sse_connections
            sse_connections.add(-1, {"key_type": key.split(":")[0]})
        except Exception:
            pass

    async def broadcast(self, event_type: str, data: dict, store_id: str, table_id: str | None = None):
        message = f"event: {event_type}\ndata: {json.dumps(data, default=str)}\n\n"
        for queue in self._connections.get(f"admin:{store_id}", []):
            await queue.put(message)
        if table_id:
            for queue in self._connections.get(f"table:{table_id}", []):
                await queue.put(message)


sse_manager = SSEManager()
