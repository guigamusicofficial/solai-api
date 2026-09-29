from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class PlanResponse(BaseModel):
    id: UUID
    name: str
    type: str
    price: float
    messages_per_month: int
    companions_available: int
    features: dict
    description: Optional[str]
    
    class Config:
        from_attributes = True

class SubscriptionResponse(BaseModel):
    id: UUID
    user_id: UUID
    plan_id: UUID
    status: str
    started_at: datetime
    expires_at: Optional[datetime]
    
    class Config:
        from_attributes = True
