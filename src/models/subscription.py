from sqlalchemy import Column, String, DateTime, Boolean, Integer, Enum, Float
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime
import uuid
import enum
from src.database import Base

class PlanType(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    VIP = "vip"

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(Enum(PlanType), nullable=False)
    price = Column(Float, nullable=False)
    stripe_price_id = Column(String(255))
    
    # Limits
    messages_per_month = Column(Integer, default=-1)  # -1 = unlimited
    companions_available = Column(Integer, default=1)
    max_memory_kb = Column(Integer, default=1024)  # 1MB
    priority_support = Column(Boolean, default=False)
    
    features = Column(JSON, default={})
    description = Column(String(512))
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    plan_id = Column(UUID(as_uuid=True), nullable=False)
    
    stripe_subscription_id = Column(String(255), unique=True)
    stripe_customer_id = Column(String(255))
    
    status = Column(String(50), default="active")  # active, canceled, expired
    started_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    canceled_at = Column(DateTime)
    
    auto_renew = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
