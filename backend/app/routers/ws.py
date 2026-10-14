from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.connection_manager import manager

router = APIRouter(tags=["websocket"])

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo for testing, in real app handle events
            await manager.send_personal_message(f"Message text was: {data}", user_id)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
