from __future__ import annotations

from typing import Any

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self._connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self._connections:
            self._connections.remove(websocket)

    async def broadcast(self, payload: dict[str, Any]) -> None:
        for websocket in list(self._connections):
            try:
                await websocket.send_json(payload)
            except Exception:
                self.disconnect(websocket)


websocket_manager = WebSocketManager()
