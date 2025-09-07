from pydantic import BaseModel
from decimal import Decimal
from datetime import date
from typing import Optional

class TransactionBase(BaseModel):
    amount: Decimal
    date: date
    description: Optional[str] = None
    is_income: bool
    category_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = None
    date: Optional[date] = None
    description: Optional[str] = None
    is_income: Optional[bool] = None
    category_id: Optional[int] = None

class TransactionResponse(TransactionBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True