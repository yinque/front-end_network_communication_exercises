from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):            # 广播，向所有连接池中的设备发送消息
        for connection in self.active_connections:
            await connection.send_text(message)


cm = ConnectionManager()


@router.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    await cm.connect(websocket)                         # 等待websocket客户端主动连接，追加到cm连接池中
    await cm.broadcast(f"<b>{client_name}</b>已连接")
    try:
        while True:
            data = await websocket.receive_text()
            await cm.broadcast(f"<b>{client_name}</b>说: {data}")
    except WebSocketDisconnect:
        cm.disconnect(websocket)
        await cm.broadcast(f"<b>{client_name}</b>断开连接")

