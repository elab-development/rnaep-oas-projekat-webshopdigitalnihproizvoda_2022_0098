import httpx
from decimal import Decimal
from app.config import settings

async def get_prices_in_currencies(amount_rsd: Decimal) -> dict:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                f"{settings.EXCHANGE_RATE_API_URL}/latest",
                params={"from": "RSD", "to": "EUR,USD"}
            )
            response.raise_for_status()
            data = response.json()
            print(f"Frankfurter API response: {data}")
            rates = data.get("rates", {})
            eur_rate = rates.get("EUR")
            usd_rate = rates.get("USD")

            if not eur_rate or not usd_rate:
                raise ValueError("Missing rates in response")

            return {
                "RSD": float(round(amount_rsd, 2)),
                "EUR": float(round(amount_rsd * Decimal(str(eur_rate)), 2)),
                "USD": float(round(amount_rsd * Decimal(str(usd_rate)), 2))
            }
    except Exception as e:
        print(f"Exchange rate error: {e}")
        return {
            "RSD": float(amount_rsd),
            "EUR": float(round(amount_rsd * Decimal("0.0085"), 2)),
            "USD": float(round(amount_rsd * Decimal("0.0093"), 2))
        }