from fastapi import APIRouter, Depends, HTTPException
from app.config import settings
from app.auth import verify_token
from app.circuit_breaker import protected_request
import httpx

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])

@router.get("/")
async def get_notifications(current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "notification-service", "get",
            f"{settings.NOTIFICATION_SERVICE_URL}/notifications/",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/unread-count")
async def get_unread_count(current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "notification-service", "get",
            f"{settings.NOTIFICATION_SERVICE_URL}/notifications/unread-count",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: str, current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "notification-service", "put",
            f"{settings.NOTIFICATION_SERVICE_URL}/notifications/{notification_id}/read",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.put("/read-all")
async def mark_all_as_read(current_user=Depends(verify_token)):
    try:
        response = await protected_request(
            "notification-service", "put",
            f"{settings.NOTIFICATION_SERVICE_URL}/notifications/read-all",
            headers={"Authorization": f"Bearer {current_user['token']}"}
        )
        return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=str(e))