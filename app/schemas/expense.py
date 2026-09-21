from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    currency: str
    description: Optional[str] = None
    date: datetime
    category_id: Optional[int] = None


class ExpenseOut(BaseModel):
    id: int
    user_id: int
    category_id: Optional[int]
    created_at: datetime
    amount: float
    currency: str
    description: Optional[str]
    date: datetime

    model_config = {"from_attributes": True}