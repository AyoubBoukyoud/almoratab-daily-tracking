from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserOut(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "user"
