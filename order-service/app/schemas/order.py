from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from app.models.order import OrderStatus

class OrderCreate(BaseModel):
    product_id: UUID

class OrderResponse(BaseModel):
    id: UUID
    buyer_id: UUID
    product_id: UUID
    seller_id: UUID
    amount: Decimal
    status: OrderStatus
    download_token: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}

class SalesStatsResponse(BaseModel):
    product_id: UUID
    total_sales: int
    total_revenue: Decimal

class PricesInCurrencies(BaseModel):
    RSD: Decimal
    EUR: Decimal
    USD: Decimal