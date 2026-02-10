from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    slug: str
    body: str
    category_id: int
    is_active: bool = True

class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    category_id: int
    user_id: int
    views_count: int
    comments_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
    
class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    body: str
    category_id: int
    user_id: int
    is_active: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

class PostResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    views_count: int
    comments_count: int
    is_active: bool
    category_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    user_id: int

class CommentResponse(CommentBase):
    id: int
    user_id: int
    post_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommentUpdate(BaseModel):
    text: str


class TagCreateRequest(BaseModel):
    name: str
    slug: str


class TagUpdateRequest(BaseModel):
    name: str | None = None


class TagListResponse(BaseModel):
    id: int
    name: str
    slug: str


class CategoryListResonse(BaseModel):
    id: int | None = None
    name: str | None = None


class CategoryCreateRequest(BaseModel):
    name: str | None = None


class ProfessionCreateRequest(BaseModel):
    name: str


class ProfessionListResponse(BaseModel):
    id: int
    name: str


class ProfessionUpdateRequest(BaseModel):
    name: str