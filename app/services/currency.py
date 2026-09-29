import json
import httpx
import redis
import xml.etree.ElementTree as ET

from app.core.config import get_settings
from app.core.currencies import Currency

settings = get_settings()

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

EXCHANGE_API_URL = "https://api.frankfurter.dev/v1/latest"
CACHE_TTL_SECONDS = 3600

CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp"

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

    if from_currency == "RUB" or to_currency == "RUB":
        rub_rates = _get_rub_rates()

        if from_currency == "RUB":
            rate = rub_rates.get(to_currency)
            if rate is None:
                raise ValueError(f"No RUB exchange rate found for {to_currency}")
            return round(amount / rate, 2)
        else:
            rate = rub_rates.get(from_currency)
            if rate is None:
                raise ValueError(f"No RUB exchange rate found for {from_currency}")
            return round(amount * rate, 2)

    rates = _get_rates(from_currency)
    rate = rates.get(to_currency)
    if rate is None:
        raise ValueError(f"No exchange rate found for {to_currency}")
    return round(amount * rate, 2)


def _get_rub_rates() -> dict:
    cache_key = "rub_rates"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    response = httpx.get(CBR_URL, timeout=10.0)
    response.raise_for_status()

    root = ET.fromstring(response.content.decode("windows-1251"))

    rates = {}
    for valute in root.findall("Valute"):
        char_code = valute.find("CharCode").text
        nominal = float(valute.find("Nominal").text)
        value = float(valute.find("Value").text.replace(",", "."))
        rates[char_code] = value / nominal

    redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(rates))
    return rates

def get_all_currency_rates(base: str = "USD") -> dict[str, float]:
    rates = {}
    for currency in Currency:
        code = currency.value
        if code == base:
            rates[code] = 1.0
            continue
        try:
            rates[code] = convert(1, base, code)
        except ValueError:
            continue
    return rates
