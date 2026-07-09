from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    order_confirmed = "order_confirmed"
    payment_failed = "payment_failed"
    download_unlocked = "download_unlocked"
    product_created = "product_created"
    new_sale = "new_sale"

class Notification(BaseModel):
    user_id: str
    type: NotificationType
    title: str
    message: str
    is_read: bool = False
    metadata: Optional[dict] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None