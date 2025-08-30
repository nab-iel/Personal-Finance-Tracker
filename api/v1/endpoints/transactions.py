from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from api.v1.endpoints.auth import get_current_user
from models.user import User

router = APIRouter()

@router.get("/")
async def get_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Implementation for getting user transactions
    return {"message": "Get user transactions"}