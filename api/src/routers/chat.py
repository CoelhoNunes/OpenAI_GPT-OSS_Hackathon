"""
Chat router - handles GPT-OSS coach conversations
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.db import get_db
from src.core.schemas import ChatMessageCreate, ChatMessageResponse, Problem
from src.services.gpt_coach import GPTCoachService

router = APIRouter()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[uuid.UUID, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, problem_id: uuid.UUID):
        await websocket.accept()
        self.active_connections[problem_id] = websocket
    
    def disconnect(self, problem_id: uuid.UUID):
        if problem_id in self.active_connections:
            del self.active_connections[problem_id]
    
    async def send_personal_message(self, message: str, problem_id: uuid.UUID):
        if problem_id in self.active_connections:
            websocket = self.active_connections[problem_id]
            await websocket.send_text(message)

manager = ConnectionManager()


@router.post("/", response_model=ChatMessageResponse)
async def send_message(
    message: ChatMessageCreate,
    db: AsyncSession = Depends(get_db)
) -> ChatMessageResponse:
    """Send a message to the GPT-OSS coach."""
    
    # Validate problem exists
    result = await db.execute(
        select(Problem).where(Problem.problem_id == message.problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Get coach response
    coach_service = GPTCoachService()
    try:
        coach_response = await coach_service.get_coach_response(
            problem_context=f"{problem.title}: {problem.prompt}",
            user_message=message.user_message,
            code_snippet=message.code_snippet
        )
    except Exception as e:
        # Let the coach service handle its own fallback responses
        coach_response = coach_service._get_fallback_response(f"{problem.title}: {problem.prompt}\n\nUser question: {message.user_message}")
    finally:
        await coach_service.close()
    
    # Save chat message
    from src.core.schemas import ChatMessage
    chat_message = ChatMessage(
        problem_id=message.problem_id,
        user_message=message.user_message,
        coach_response=coach_response,
        code_snippet=message.code_snippet
    )
    
    db.add(chat_message)
    await db.commit()
    await db.refresh(chat_message)
    
    return ChatMessageResponse.model_validate(chat_message)


@router.websocket("/ws/{problem_id}")
async def websocket_endpoint(websocket: WebSocket, problem_id: uuid.UUID):
    """WebSocket endpoint for real-time chat."""
    await manager.connect(websocket, problem_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Parse message (assuming JSON format)
            import json
            try:
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                code_snippet = message_data.get("code_snippet")
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "error": "Invalid JSON format"
                }))
                continue
            
            # Get coach response
            coach_service = GPTCoachService()
            try:
                # Get problem context (you might want to cache this)
                from src.core.db import AsyncSessionLocal
                async with AsyncSessionLocal() as db:
                    result = await db.execute(
                        select(Problem).where(Problem.problem_id == problem_id)
                    )
                    problem = result.scalar_one_or_none()
                    
                    if not problem:
                        await websocket.send_text(json.dumps({
                            "error": "Problem not found"
                        }))
                        continue
                    
                    coach_response = await coach_service.get_coach_response(
                        problem_context=f"{problem.title}: {problem.prompt}",
                        user_message=user_message,
                        code_snippet=code_snippet
                    )
                    
                    # Save chat message
                    from src.core.schemas import ChatMessage
                    chat_message = ChatMessage(
                        problem_id=problem_id,
                        user_message=user_message,
                        coach_response=coach_response,
                        code_snippet=code_snippet
                    )
                    
                    db.add(chat_message)
                    await db.commit()
                    
            except Exception as e:
                coach_response = "I'm having trouble processing your request. Please try again."
            finally:
                await coach_service.close()
            
            # Send response back to client
            await websocket.send_text(json.dumps({
                "response": coach_response,
                "timestamp": chat_message.created_at.isoformat()
            }))
            
    except WebSocketDisconnect:
        manager.disconnect(problem_id)


@router.get("/{problem_id}/history", response_model=list[ChatMessageResponse])
async def get_chat_history(
    problem_id: uuid.UUID,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
) -> list[ChatMessageResponse]:
    """Get chat history for a problem."""
    
    from src.core.schemas import ChatMessage
    
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.problem_id == problem_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )
    
    messages = result.scalars().all()
    return [ChatMessageResponse.model_validate(msg) for msg in reversed(messages)]
