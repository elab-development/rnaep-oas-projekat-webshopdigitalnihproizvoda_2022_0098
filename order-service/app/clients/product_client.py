import httpx
import os

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8000")

async def get_product_details(product_id: str, token: str):
    """Pribavlja podatke o proizvodu sa Product Service-a."""
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}", headers=headers)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()