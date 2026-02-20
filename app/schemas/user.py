from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    bio: Optional[str] = None
    profession_id: Optional[int] = None


class UserCreate(UserBase):
    password: str
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    profession_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_staff: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    posts_count: int
    posts_read_count: int
    is_active: bool
    is_staff: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class UserRegisterResponse(BaseModel):
    message: str
