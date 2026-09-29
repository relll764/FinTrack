from fastapi import APIRouter

from app.core.currencies import Currency
from app.services.currency import get_all_currency_rates

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("/")
def get_available_currencies(base: str = "USD"):
    rates = get_all_currency_rates(base)
    return [{"code": code, "rate": rate} for code, rate in rates.items()]