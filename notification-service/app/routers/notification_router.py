from fastapi import APIRouter, Depends
from app.database import get_collection
from app.repositories.notification_repository import NotificationRepository
from app.services.auth_dependency import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/")
async def get_my_notifications(current_user=Depends(get_current_user)):
    collection = get_collection()
    repo = NotificationRepository(collection)
    return await repo.get_by_user(current_user["user_id"])

@router.get("/unread-count")
async def get_unread_count(current_user=Depends(get_current_user)):
    collection = get_collection()
    repo = NotificationRepository(collection)
    count = await repo.get_unread_count(current_user["user_id"])
    return {"unread_count": count}

@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: str, current_user=Depends(get_current_user)):
    collection = get_collection()
    repo = NotificationRepository(collection)
    success = await repo.mark_as_read(notification_id, current_user["user_id"])
    return {"success": success}

@router.put("/read-all")
async def mark_all_as_read(current_user=Depends(get_current_user)):
    collection = get_collection()
    repo = NotificationRepository(collection)
    await repo.mark_all_as_read(current_user["user_id"])
    return {"message": "All notifications marked as read"}