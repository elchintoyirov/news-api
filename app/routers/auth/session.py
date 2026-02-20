import secrets
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select, delete

from app.db.session import get_db as db_dep
from app.models import User, UserSessionToken
from app.dependencies import session_auth_dep
from app.schemas.auth import UserLoginRequest, UserProfileResponse
from app.services.utils import verify_password
from app.config import settings


router = APIRouter(prefix="/session", tags=["Auth"])


@router.post("/login/", status_code=200)
async def login(db: db_dep, login_data: UserLoginRequest, response: Response):
    stmt = select(User).where(User.email == login_data.email)
    res = db.execute(stmt)
    user = res.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    sessionId = secrets.token_urlsafe(32)

    stmt = delete(UserSessionToken).where(UserSessionToken.user_id == user.id)
    db.execute(stmt)
    db.flush()

    new_session = UserSessionToken(
        token=sessionId,
        user_id=user.id,
        expires_at=datetime.now(tz=timezone.utc)
        + timedelta(days=settings.SESSION_ID_EXPIRE_DAYS),
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    response.set_cookie(
        key="session_id",
        value=sessionId,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.SESSION_ID_EXPIRE_DAYS * 24 * 60 * 60,
    )


@router.get("/profile/", response_model=UserProfileResponse)
async def user_profile(db: db_dep, current_user: session_auth_dep):
    return current_user
