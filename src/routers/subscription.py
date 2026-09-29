from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.subscription import Plan, Subscription
from src.models.user import User
from src.auth.dependencies import get_current_user
from src.services.payment import StripeService

router = APIRouter(prefix="/api/subscription", tags=["subscription"])

payment_service = StripeService()

@router.get("/plans")
async def list_plans(db: Session = Depends(get_db)):
    plans = db.query(Plan).filter(Plan.is_active == True).all()
    return plans

@router.post("/checkout")
async def create_checkout(
    plan_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    
    # Create Stripe session
    session = await payment_service.create_checkout_session(
        user=current_user,
        plan=plan
    )
    
    return {"checkout_url": session.url}

@router.get("/current")
async def get_current_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        return {"plan": "free"}
    
    return subscription
