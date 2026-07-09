from sqlalchemy import Column, String, Numeric, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
import enum
from datetime import datetime

class OrderStatus(str, enum.Enum):
    pending = "pending"
    payment_processing = "payment_processing"
    confirmed = "confirmed"
    failed = "failed"
    refunded = "refunded"

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    buyer_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    seller_id = Column(UUID(as_uuid=True), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.pending)
    payment_reference = Column(String(255), nullable=True)
    download_token = Column(String(500), nullable=True)
    token_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)