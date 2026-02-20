from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


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


class CommentUpdate(BaseModel):
    text: Optional[str] = None


class CommentResponse(CommentBase):
    id: int
    user_id: int
    post_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagBase(BaseModel):
    name: str
    slug: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    name: Optional[str] = None


class TagResponse(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProfessionBase(BaseModel):
    name: str


class ProfessionCreate(ProfessionBase):
    pass


class ProfessionUpdate(BaseModel):
    name: Optional[str] = None


class ProfessionResponse(ProfessionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DeviceCreate(BaseModel):
    user_agent: str


class DeviceResponse(BaseModel):
    id: int
    user_agent: str
    last_active: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LikeCreate(BaseModel):
    device_id: int


class SearchTrackRequest(BaseModel):
    term: str


class SearchTrackResponse(BaseModel):
    term: str
    count: int


class MediaCreate(BaseModel):
    url: str


class MediaResponse(BaseModel):
    id: int
    url: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
