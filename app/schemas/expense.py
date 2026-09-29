from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from app.core.currencies import Currency


class ExpenseCreate(BaseModel):
    amount: float
    currency: Currency
    description: Optional[str] = None
    date: date
    category_id: Optional[int] = None
    account_id: Optional[int] = None


class ExpenseOut(BaseModel):
    id: int
    user_id: int
    category_id: int
    created_at: datetime
    amount: float
    currency: Currency
    description: Optional[str]
    date: date
    account_id: Optional[int]
    account_amount: Optional[float]

    model_config = {"from_attributes": True}

class ExpenseUpdate(BaseModel):
    amount: float
    currency: Currency
    description: Optional[str] = None
    date: date
    category_id: Optional[int] = None
    auto_categorize: bool = False
    account_id: Optional[int] = None