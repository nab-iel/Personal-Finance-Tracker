from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from app.dependencies import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """Get all transactions for the current user"""
    result = await db.execute(
        select(Transaction)
        .where(Transaction.owner_id == current_user.id)
        .options(selectinload(Transaction.category))
        .order_by(Transaction.date.desc())
    )
    transactions = result.scalars().all()
    return transactions

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
        transaction_data: TransactionCreate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """Create a new transaction for the current user"""
    new_transaction = Transaction(
        **transaction_data.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
        transaction_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """Get a specific transaction by ID (only if owned by current user)"""
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id, Transaction.owner_id == current_user.id)
        .options(selectinload(Transaction.category))
    )
    transaction = result.scalar_one_or_none()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    return transaction

@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
        transaction_id: int,
        transaction_data: TransactionUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """Update a transaction (only if owned by current user)"""
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id, Transaction.owner_id == current_user.id)
    )
    transaction = result.scalar_one_or_none()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    update_data = transaction_data.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)

    await db.commit()
    await db.refresh(transaction)
    return transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
        transaction_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """Delete a transaction (only if owned by current user)"""
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id, Transaction.owner_id == current_user.id)
    )
    transaction = result.scalar_one_or_none()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    await db.delete(transaction)
    await db.commit()
    return None