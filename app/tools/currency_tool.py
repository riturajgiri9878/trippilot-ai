import httpx

from app.config import settings


FRANKFURTER_BASE_URL = "https://api.frankfurter.dev/v2"


def get_exchange_rate(
    base_currency: str,
    quote_currency: str,
) -> dict:
    base = base_currency.strip().upper()
    quote = quote_currency.strip().upper()

    if len(base) != 3:
        raise ValueError(
            "Base currency must be a 3-letter code."
        )

    if len(quote) != 3:
        raise ValueError(
            "Quote currency must be a 3-letter code."
        )

    if base == quote:
        return {
            "date": None,
            "base": base,
            "quote": quote,
            "rate": 1.0,
            "provider": "frankfurter",
            "source_type": "live",
        }

    url = (
        f"{FRANKFURTER_BASE_URL}"
        f"/rate/{base}/{quote}"
    )

    response = httpx.get(
        url,
        timeout=settings.request_timeout,
    )

    response.raise_for_status()

    data = response.json()

    rate = data.get("rate")

    if rate is None:
        raise ValueError(
            f"Exchange rate unavailable "
            f"for {base} to {quote}."
        )

    return {
        "date": data.get("date"),
        "base": data.get("base", base),
        "quote": data.get("quote", quote),
        "rate": float(rate),
        "provider": "frankfurter",
        "source_type": "live",
    }


def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
) -> dict:
    if amount < 0:
        raise ValueError(
            "Amount cannot be negative."
        )

    exchange = get_exchange_rate(
        from_currency,
        to_currency,
    )

    converted_amount = (
        amount * exchange["rate"]
    )

    return {
        "original_amount": round(amount, 2),
        "original_currency": (
            exchange["base"]
        ),
        "converted_amount": round(
            converted_amount,
            2,
        ),
        "converted_currency": (
            exchange["quote"]
        ),
        "rate": exchange["rate"],
        "rate_date": exchange["date"],
        "provider": exchange["provider"],
        "source_type": exchange[
            "source_type"
        ],
    }