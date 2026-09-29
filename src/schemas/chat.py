from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class MessageCreate(BaseModel):
    content: str
    companion_id: Optional[UUID] = None

class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    id: UUID
    user_id: UUID
    companion_id: UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ChatWithMessages(ChatResponse):
    messages: List[MessageResponse]
