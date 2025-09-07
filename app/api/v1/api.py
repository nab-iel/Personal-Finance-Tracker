from fastapi import APIRouter
from app.api.v1.endpoints import categories
from app.api.v1.endpoints import transactions, auth, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])