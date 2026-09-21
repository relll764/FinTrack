from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from app.models import SubscriptionPeriod


class SubscriptionCreate(BaseModel):
    name: str
    amount: float
    currency: str
    period: SubscriptionPeriod
    next_billing_date: date


class SubscriptionOut(BaseModel):
    id: int
    user_id: int
    name: str
    amount: float
    currency: str
    period: SubscriptionPeriod
    next_billing_date: date
    created_at: datetime

    model_config = {"from_attributes": True}