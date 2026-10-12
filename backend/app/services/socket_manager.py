import json
import logging
from typing import List
from fastapi import WebSocket

logger = logging.getLogger("nids.socket_manager")

class SocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Client connected to live telemetry stream. Total active: %d", len(self.active_connections))

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("Client disconnected from telemetry stream. Remaining: %d", len(self.active_connections))

    async def broadcast(self, data: dict):
        if not self.active_connections:
            return
        
        message_json = json.dumps(data)
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.warning("Error pushing telemetry event to client: %s", str(e))
                disconnected.append(connection)

        for dead_connection in disconnected:
            self.disconnect(dead_connection)

socket_manager = SocketManager()
