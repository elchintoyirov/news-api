from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.users import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.utils import hash_password
from app.dependencies import current_user_jwt_dep

router = APIRouter()


@router.post("/create", response_model=UserResponse)
async def user_create(
    user_in: UserCreate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    new_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        bio=user_in.bio,
        profession_id=user_in.profession_id,
        is_active=user_in.is_active,
        is_staff=user_in.is_staff,
        is_superuser=user_in.is_superuser,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/list", response_model=list[UserResponse])
async def users_list(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}/", response_model=UserResponse)
async def user_detail(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return JSONResponse(
            {"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return user


@router.put("/{user_id}/", response_model=UserResponse)
async def user_update(
    user_id: int,
    user_in: UserUpdate,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return JSONResponse(
            {"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    user.first_name = user_in.first_name
    user.last_name = user_in.last_name
    user.email = user_in.email
    user.bio = user_in.bio
    user.is_active = user_in.is_active
    user.is_staff = user_in.is_staff
    user.is_superuser = user_in.is_superuser

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}")
async def user_delete(
    user_id: int,
    current_user: current_user_jwt_dep,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return JSONResponse(
            {"error": "User not found"}, status_code=status.HTTP_404_NOT_FOUND
        )

    await db.delete(user)
    await db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
