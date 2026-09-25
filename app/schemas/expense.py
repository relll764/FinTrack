from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    currency: str
    description: Optional[str] = None
    date: date
    category_id: Optional[int] = None


class ExpenseOut(BaseModel):
    id: int
    user_id: int
    category_id: int
    created_at: datetime
    amount: float
    currency: str
    description: Optional[str]
    date: date

    model_config = {"from_attributes": True}

class ExpenseUpdate(BaseModel):
    amount: float
    currency: str
    description: Optional[str] = None
    date: date
    category_id: Optional[int] = None
    auto_categorize: bool = False