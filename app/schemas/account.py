from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.core.currencies import Currency


class AccountCreate(BaseModel):
    name: str
    balance: float
    currency: Currency
    description: Optional[str] = None

class AccountOut(BaseModel):
    id: int
    user_id: int
    name: str
    balance: float
    currency: Currency
    description: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}