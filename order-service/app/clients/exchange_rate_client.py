import httpx
from decimal import Decimal
from app.config import settings

async def get_prices_in_currencies(amount_rsd: Decimal) -> dict:
    """
    Konvertuje cenu iz RSD u EUR i USD koristeći Frankfurter API.
    Vraća fallback (1:1) ako API nije dostupan — štiti tok kupovine.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.EXCHANGE_RATE_API_URL}/latest",
                params={"from": "RSD", "to": "EUR,USD"}
            )
            response.raise_for_status()
            data = response.json()
            rates = data["rates"]
            return {
                "RSD": amount_rsd,
                "EUR": round(amount_rsd * Decimal(str(rates["EUR"])), 2),
                "USD": round(amount_rsd * Decimal(str(rates["USD"])), 2)
            }
    except (httpx.HTTPError, KeyError):
        return {"RSD": amount_rsd, "EUR": amount_rsd, "USD": amount_rsd}