from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.user import UserRole
import html

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.buyer

    @field_validator('first_name', 'last_name')
    @classmethod
    def sanitize_string(cls, v):
        return html.escape(v.strip())

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator('first_name', 'last_name')
    @classmethod
    def sanitize_string(cls, v):
        if v:
            return html.escape(v.strip())
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse