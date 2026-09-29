from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.config import settings
from src.database import Base, engine
from src.routers import auth, chat, companions, subscription
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sol AI API",
    description="API for Sol AI - Virtual Dating Companion",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(companions.router)
app.include_router(subscription.router)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "Sol AI API",
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    return {
        "message": "Welcome to Sol AI API",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
