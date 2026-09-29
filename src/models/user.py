from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime
import uuid
import enum
from src.database import Base

class UserRole(str, enum.Enum):
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    VIP = "vip"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(String(512))
    
    # Plan & Billing
    plan = Column(Enum(UserRole), default=UserRole.FREE, nullable=False)
    stripe_customer_id = Column(String(255), unique=True)
    stripe_subscription_id = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    # Profile
    bio = Column(Text)
    preferences = Column(JSON, default={})
    memory = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)
    
    # Subscription info
    subscription_expires_at = Column(DateTime)
    
    def __repr__(self):
        return f"<User {self.username}>"
