from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.models.chat import ChatSession, Message, MessageRole, Companion
from src.schemas.chat import MessageCreate, MessageResponse, ChatResponse, ChatWithMessages
from src.auth.dependencies import get_current_user
from src.services.llm import LLMService
from uuid import uuid4

router = APIRouter(prefix="/api/chat", tags=["chat"])

llm_service = LLMService()

@router.post("/message")
async def send_message(
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get or create chat session
    if not message.companion_id:
        # Default to first companion
        companion = db.query(Companion).filter(Companion.is_active == 1).first()
        if not companion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No companions available"
            )
        message.companion_id = companion.id
    
    # Check companion exists
    companion = db.query(Companion).filter(
        Companion.id == message.companion_id,
        Companion.is_active == 1
    ).first()
    
    if not companion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Companion not found"
        )
    
    # Get or create session (get active session)
    session = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.companion_id == message.companion_id,
        ChatSession.is_active == 1
    ).first()
    
    if not session:
        session = ChatSession(
            id=uuid4(),
            user_id=current_user.id,
            companion_id=message.companion_id,
            title=f"Chat with {companion.name}"
        )
        db.add(session)
        db.commit()
    
    # Save user message
    user_msg = Message(
        id=uuid4(),
        session_id=session.id,
        user_id=current_user.id,
        companion_id=message.companion_id,
        role=MessageRole.USER,
        content=message.content
    )
    db.add(user_msg)
    db.commit()
    
    # Get chat history
    history = db.query(Message).filter(
        Message.session_id == session.id
    ).order_by(Message.created_at).all()
    
    # Generate response
    response_text = await llm_service.generate_response(
        companion=companion,
        user=current_user,
        history=history,
        user_message=message.content
    )
    
    # Save assistant response
    assistant_msg = Message(
        id=uuid4(),
        session_id=session.id,
        user_id=current_user.id,
        companion_id=message.companion_id,
        role=MessageRole.ASSISTANT,
        content=response_text
    )
    db.add(assistant_msg)
    db.commit()
    
    return {
        "message": response_text,
        "session_id": str(session.id),
        "companion_id": str(message.companion_id)
    }

@router.get("/sessions")
async def get_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).all()
    return sessions

@router.get("/session/{session_id}", response_model=ChatWithMessages)
async def get_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    messages = db.query(Message).filter(
        Message.session_id == session.id
    ).order_by(Message.created_at).all()
    
    return {
        **ChatResponse.from_orm(session).dict(),
        "messages": [MessageResponse.from_orm(m).dict() for m in messages]
    }
