from pydantic import BaseModel
from decimal import Decimal
from datetime import date
from typing import Optional

class BudgetBase(BaseModel):
    amount: Decimal
    start_date: date
    end_date: date
    category_id: int

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    amount: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    category_id: Optional[int] = None

class BudgetResponse(BudgetBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True