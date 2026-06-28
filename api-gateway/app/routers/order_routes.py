from fastapi import APIRouter, Request, Depends, HTTPException
from app.config import settings
from app.auth import verify_token
from app.circuit_breaker import protected_request
import httpx

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.post("/")
async def create_order(request: Request, current_user=Depends(verify_token)):
    body = await request.json()
    try:
        response = await protected_request(
            "order-service", "post",
            f"{settings.ORDER_SERVICE_URL}/orders/",
            json=body,
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/my-purchases")
async def get_my_purchases(current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "order-service", "get",
            f"{settings.ORDER_SERVICE_URL}/orders/my-purchases",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/seller/stats")
async def get_sales_stats(current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "order-service", "get",
            f"{settings.ORDER_SERVICE_URL}/orders/seller/stats",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/{order_id}")
async def get_order(order_id: str, current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "order-service", "get",
            f"{settings.ORDER_SERVICE_URL}/orders/{order_id}",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/{order_id}/download")
async def download_product(order_id: str, current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "order-service", "get",
            f"{settings.ORDER_SERVICE_URL}/orders/{order_id}/download",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/exchange/{amount}")
async def get_price_in_currencies(amount: float):
    try:
        response = await protected_request(
            "order-service", "get",
            f"{settings.ORDER_SERVICE_URL}/orders/exchange/{amount}"
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))