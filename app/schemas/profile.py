from pydantic import BaseModel

from app.core.currencies import Currency
from app.core.themes import Theme


class ProfileShema(BaseModel):
    user_id: int
    currency: Currency
    subscription: bool
    balance: float
    theme: Theme