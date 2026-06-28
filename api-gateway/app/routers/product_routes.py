from fastapi import APIRouter, Request, Depends, HTTPException, Query
from typing import Optional
from app.config import settings
from app.auth import verify_token
from app.circuit_breaker import protected_request
import httpx

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/")
async def get_products(
    search: Optional[str] = Query(None),
    category_id: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None)
):
    params = {}
    if search: params["search"] = search
    if category_id: params["category_id"] = category_id
    if min_price: params["min_price"] = min_price
    if max_price: params["max_price"] = max_price
    try:
        response = await protected_request(
            "product-service", "get",
            f"{settings.PRODUCT_SERVICE_URL}/products/",
            params=params
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/categories")
async def get_categories():
    try:
        response = await protected_request(
            "product-service", "get",
            f"{settings.PRODUCT_SERVICE_URL}/categories/"
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/{product_id}")
async def get_product(product_id: str):
    try:
        response = await protected_request(
            "product-service", "get",
            f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}"
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.post("/")
async def create_product(request: Request, current_user=Depends(verify_token)):
    body = await request.json()
    try:
        response = await protected_request(
            "product-service", "post",
            f"{settings.PRODUCT_SERVICE_URL}/products/",
            json=body,
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.put("/{product_id}")
async def update_product(product_id: str, request: Request, current_user=Depends(verify_token)):
    body = await request.json()
    try:
        response = await protected_request(
            "product-service", "put",
            f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}",
            json=body,
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.delete("/{product_id}")
async def delete_product(product_id: str, current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "product-service", "delete",
            f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return {"message": "Product deleted"}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/seller/my-products")
async def get_my_products(current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "product-service", "get",
            f"{settings.PRODUCT_SERVICE_URL}/products/seller/my-products",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.post("/categories")
async def create_category(request: Request, current_user=Depends(verify_token)):
    body = await request.json()
    try:
        response = await protected_request(
            "product-service", "post",
            f"{settings.PRODUCT_SERVICE_URL}/categories/",
            json=body,
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.delete("/categories/{category_id}")
async def delete_category(category_id: str, current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "product-service", "delete",
            f"{settings.PRODUCT_SERVICE_URL}/categories/{category_id}",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return {"message": "Category deleted"}
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))