from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from pages.base.router import templates
from pages.chat.models import Message
from src.auth.base_config import current_user
from src.database import async_session_maker, get_async_session

router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, save_to_database: bool):
        if save_to_database:
            await self.save_message_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def save_message_to_database(message: str):
        async with async_session_maker() as session:
            statement = insert(Message).values(
                message=message
            )
            await session.execute(statement)
            await session.commit()


manager = ConnectionManager()


@router.get('/last_messages')
async def get_last_messages(session: AsyncSession = Depends(get_async_session)):
    query = select(Message).order_by(Message.id.desc()).limit(5)
    messages = await session.execute(query)
    messages = messages.all()
    messages_list = [msg[0].as_dict() for msg in messages]
    return messages_list


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}", save_to_database=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", save_to_database=False)


@router.get('')
def get_chat_page(request: Request, current_user=Depends(current_user)):
    return templates.TemplateResponse(
        'chat.html',
        {'request': request, 'current_user': current_user}
    )
