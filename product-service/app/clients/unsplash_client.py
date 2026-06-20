import httpx
from app.config import settings

UNSPLASH_API_URL = "https://api.unsplash.com/photos/random"

async def get_product_thumbnail(query: str) -> str:
    """Pribavlja nasumičnu sliku sa Unsplash-a na osnovu ključne reči."""
    headers = {"Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"}
    params = {"query": query, "orientation": "landscape"}

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(UNSPLASH_API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data["urls"]["regular"]
    except (httpx.HTTPError, KeyError):
        # Fallback slika ako Unsplash nije dostupan
        return "https://via.placeholder.com/600x400?text=Product+Image"