from unittest.mock import patch, MagicMock

from app.services.currency import convert


def test_convert_usd_to_rub_uses_cbr():
    mock_response = MagicMock()
    mock_response.content = (
        '<ValCurs><Valute><CharCode>USD</CharCode>'
        '<Nominal>1</Nominal><Value>92,50</Value></Valute></ValCurs>'
    ).encode("windows-1251")
    mock_response.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_response), \
         patch("app.services.currency.redis_client") as mock_redis:
        mock_redis.get.return_value = None
        result = convert(100, "USD", "RUB")
        assert result == 9250.0


def test_convert_rub_to_usd_inverse():
    mock_response = MagicMock()
    mock_response.content = (
        '<ValCurs><Valute><CharCode>USD</CharCode>'
        '<Nominal>1</Nominal><Value>100,00</Value></Valute></ValCurs>'
    ).encode("windows-1251")
    mock_response.raise_for_status.return_value = None

    with patch("httpx.get", return_value=mock_response), \
         patch("app.services.currency.redis_client") as mock_redis:
        mock_redis.get.return_value = None
        result = convert(1000, "RUB", "USD")
        assert result == 10.0