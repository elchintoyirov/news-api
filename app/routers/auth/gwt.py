from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db as db_dep
from app.dependencies import current_user_jwt_dep
from app.schemas.auth import UserLoginRequest, RefreshTokenRequest, UserProfileResponse
from app.models import User
from app.services.utils import verify_password, generate_jwt_tokens, decode_jwt_token


router = APIRouter(prefix="/jwt", tags=["Auth"])


@router.post("/login/")
async def login(
    login_data: UserLoginRequest, db: AsyncSession = Depends(db_dep)
):

    stmt = select(User).where(User.email == login_data.email)
    user = (await db.execute(stmt)).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token, refresh_token = generate_jwt_tokens(user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/refresh/")
async def refresh(
    data: RefreshTokenRequest, db: AsyncSession = Depends(db_dep)
):
    decoded_data = decode_jwt_token(data.refresh_token)

    exp_time = datetime.fromtimestamp(decoded_data["exp"], tz=timezone.utc)
    if exp_time < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401, detail="Refresh token expired. Please log in."
        )

    user_id = decoded_data["sub"]
    access_token = generate_jwt_tokens(user_id, is_access_only=True)

    return {
        "access_token": access_token,
    }


@router.get("/me/", response_model=UserProfileResponse)
async def me(current_user: current_user_jwt_dep):
    return current_user
