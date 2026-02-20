from pydantic import BaseModel, EmailStr


class ProfessionInline(BaseModel):
    id: int
    name: str


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    posts_count: int
    posts_read_count: int
    profession: ProfessionInline | None = None
    is_active: bool
    is_staff: bool
    is_superuser: bool
    is_deleted: bool


class UserProfileUpdateRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    profession_id: int | None = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
