from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.chat import Companion
from src.auth.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api/companions", tags=["companions"])

@router.get("/")
async def list_companions(db: Session = Depends(get_db)):
    companions = db.query(Companion).filter(Companion.is_active == 1).all()
    return [
        {
            "id": str(c.id),
            "name": c.name,
            "description": c.description,
            "avatar_url": c.avatar_url,
            "metadata": c.metadata
        }
        for c in companions
    ]

@router.get("/{companion_id}")
async def get_companion(
    companion_id: str,
    db: Session = Depends(get_db)
):
    companion = db.query(Companion).filter(
        Companion.id == companion_id,
        Companion.is_active == 1
    ).first()
    
    if not companion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Companion not found"
        )
    
    return {
        "id": str(companion.id),
        "name": companion.name,
        "description": companion.description,
        "avatar_url": companion.avatar_url,
        "metadata": companion.metadata
    }
