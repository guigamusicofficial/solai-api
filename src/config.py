from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/solai_prod"
    
    # JWT & Auth
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # API Keys - Hugging Face (Primary)
    huggingface_api_key: str = ""
    
    # API Keys - Fallback
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    
    groq_api_key: str = ""
    groq_base_url: str = "https://api.groq.com/openai/v1"
    
    gemini_api_key: str = ""
    
    # Stripe
    stripe_secret_key: str = ""
    stripe_publishable_key: str = ""
    stripe_webhook_secret: str = ""
    
    # Server
    port: int = 8080
    host: str = "0.0.0.0"
    environment: str = "development"
    debug: bool = False
    
    # Frontend & API URLs
    frontend_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8080"
    
    # Redis (optional)
    redis_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
