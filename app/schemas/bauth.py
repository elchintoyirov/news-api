from pydantic import BaseModel, EmailStr

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    
    id: int
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None