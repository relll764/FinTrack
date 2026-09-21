from datetime import datetime

from pydantic import BaseModel


class BudgetCreate(BaseModel):
    category_id: int
    monthly_limit: float


class BudgetOut(BaseModel):
    id: int
    user_id: int
    category_id: int
    monthly_limit: float
    created_at: datetime

    model_config = {"from_attributes": True}