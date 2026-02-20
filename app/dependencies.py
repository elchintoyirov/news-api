from typing import Annotated
from datetime import datetime, timezone, timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.session import get_db as db_dep
from app.models import User, UserSessionToken
from app.services.utils import verify_password, decode_jwt_token
from app.config import settings


basic = HTTPBasic()
basic_auth_dep = Annotated[HTTPBasicCredentials, Depends(basic)]

jwt_security = HTTPBearer(auto_error=False)


def get_current_user(session: db_dep, credentials: basic_auth_dep):
    stmt = (
        select(User)
        .where(User.email == credentials.username)
        .options(joinedload(User.profession))
    )
    user = session.execute(stmt).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user


current_user_basic_dep = Annotated[User, Depends(get_current_user)]


def get_current_user_session(session: db_dep, request: Request):
    sessionId = request.cookies.get("session_id")
    if not sessionId:
        raise HTTPException(status_code=401, detail="Not authenticated")

    stmt = select(UserSessionToken).where(UserSessionToken.token == sessionId)
    session_obj = (session.execute(stmt)).scalars().first()

    if not session_obj:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if session_obj.expires_at < datetime.now(tz=timezone.utc):
        session.delete(session_obj)
        session.commit()
        raise HTTPException(status_code=401, detail="Not authenticated")

    stmt = (
        select(User)
        .where(User.id == session_obj.user_id)
        .options(joinedload(User.profession))
    )
    user = session.execute(stmt).scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return user


session_auth_dep = Annotated[User, Depends(get_current_user_session)]


def get_current_user_jwt(
    session: db_dep, credentials: HTTPAuthorizationCredentials = Depends(jwt_security)
):
    if not credentials:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print(credentials.credentials)

    decoded = decode_jwt_token(credentials.credentials)
    user_id = decoded["sub"]
    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)

    if exp < datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ):
        raise HTTPException(status_code=401, detail="Token expired.")

    stmt = select(User).where(User.id == user_id).options(joinedload(User.profession))
    user = session.execute(stmt).scalars().first()

    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")

    return user


current_user_jwt_dep = Annotated[User, Depends(get_current_user_jwt)]
