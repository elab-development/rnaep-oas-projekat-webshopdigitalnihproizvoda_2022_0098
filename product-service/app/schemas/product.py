from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime
import html

class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    category_id: Optional[UUID] = None
    file_path: str

    @field_validator('name', 'description')
    @classmethod
    def sanitize_string(cls, v):
        return html.escape(v.strip())

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than 0')
        return v

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category_id: Optional[UUID] = None
    is_active: Optional[bool] = None

    @field_validator('name', 'description')
    @classmethod
    def sanitize_string(cls, v):
        if v:
            return html.escape(v.strip())
        return v

class ProductResponse(BaseModel):
    id: UUID
    seller_id: UUID
    category_id: Optional[UUID]
    name: str
    description: str
    price: Decimal
    thumbnail_url: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}