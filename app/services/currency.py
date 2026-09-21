import json

import httpx
import redis

from app.core.config import get_settings

settings = get_settings()

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

EXCHANGE_API_URL = "https://api.frankfurter.dev/v1/latest"
CACHE_TTL_SECONDS = 3600  # 1 час


def _get_rates(base_currency: str) -> dict:
    cache_key = f"rates:{base_currency}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    response = httpx.get(EXCHANGE_API_URL, params={"base": base_currency})
    response.raise_for_status()
    data = response.json()
    rates = data["rates"]

    redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(rates))

    return rates


def convert(amount: float, from_currency: str, to_currency: str) -> float:
    if from_currency == to_currency:
        return amount

    rates = _get_rates(from_currency)
    rate = rates.get(to_currency)

    if rate is None:
        raise ValueError(f"No exchange rate found for {to_currency}")

    return round(amount * rate, 2)
