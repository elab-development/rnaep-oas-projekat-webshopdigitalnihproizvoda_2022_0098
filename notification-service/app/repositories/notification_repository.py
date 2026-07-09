from motor.motor_asyncio import AsyncIOMotorCollection
from app.models.notification import Notification
from bson import ObjectId
from datetime import datetime

class NotificationRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def create(self, notification: Notification) -> str:
        result = await self.collection.insert_one(notification.model_dump())
        return str(result.inserted_id)

    async def get_by_user(self, user_id: str) -> list:
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1)
        notifications = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            notifications.append(doc)
        return notifications

    async def get_unread_count(self, user_id: str) -> int:
        return await self.collection.count_documents({"user_id": user_id, "is_read": False})

    async def mark_as_read(self, notification_id: str, user_id: str) -> bool:
        result = await self.collection.update_one(
            {"_id": ObjectId(notification_id), "user_id": user_id},
            {"$set": {"is_read": True, "read_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def mark_all_as_read(self, user_id: str):
        await self.collection.update_many(
            {"user_id": user_id, "is_read": False},
            {"$set": {"is_read": True, "read_at": datetime.utcnow()}}
        )