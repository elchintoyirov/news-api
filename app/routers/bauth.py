# Basic auth
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import User
from app.schemas.user import (UserRegisterResponse, UserRegisterRequest)
from sqlalchemy import select
from services.utils import hash_password # fix import module

router = APIRouter()
security = HTTPBasic()

@router.get("/user")
async def auth_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {"username": credentials.username, "password": credentials.password}


@router.get("/register", response_model=UserRegisterResponse)
async def register_user(data: UserRegisterRequest, session: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == data.email)
    res = (session.execute(stmt))

    if res:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(email=data.email, password_hash=hash_password(data.password))

    stmt = select(User)
    existing_user = session.execute(stmt).scalars().first()

    if not existing_user:
        user.is_staff = True
        user.is_superuser = True

    session.add(user)
    session.commit()
    session.refresh(user)

    return user