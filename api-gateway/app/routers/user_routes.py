from fastapi import APIRouter, Request, Depends, HTTPException
from app.config import settings
from app.auth import verify_token
from app.circuit_breaker import protected_request
import httpx

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/auth/register")
async def register(request: Request):
    body = await request.json()
    try:
        response = await protected_request(
            "user-service", "post",
            f"{settings.USER_SERVICE_URL}/auth/register",
            json=body
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    try:
        response = await protected_request(
            "user-service", "post",
            f"{settings.USER_SERVICE_URL}/auth/login",
            json=body
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/me")
async def get_profile(current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "user-service", "get",
            f"{settings.USER_SERVICE_URL}/users/me",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.put("/me")
async def update_profile(request: Request, current_user=Depends(verify_token)):
    body = await request.json()
    try:
        response = await protected_request(
            "user-service", "put",
            f"{settings.USER_SERVICE_URL}/users/me",
            json=body,
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/")
async def get_all_users(current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "user-service", "get",
            f"{settings.USER_SERVICE_URL}/users/",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.put("/{user_id}/deactivate")
async def deactivate_user(user_id: str, current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "user-service", "put",
            f"{settings.USER_SERVICE_URL}/users/{user_id}/deactivate",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))