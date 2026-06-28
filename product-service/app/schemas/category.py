from pydantic import BaseModel, field_validator
from typing import Optional
from uuid import UUID
import html

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator('name', 'description')
    @classmethod
    def sanitize_string(cls, v):
        if v:
            return html.escape(v.strip())
        return v

class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]

    model_config = {"from_attributes": True}