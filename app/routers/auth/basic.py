from fastapi import APIRouter
from app.db.session import get_db as db_dep
from app.dependencies import current_user_basic_dep
from app.schemas.auth import (
    UserProfileResponse,
    UserProfileUpdateRequest,
)


router = APIRouter(prefix="/basic", tags=["Auth"])


@router.get("/profile/", response_model=UserProfileResponse)
async def user_profile(db: db_dep, current_user: current_user_basic_dep):
    return current_user


@router.put("/profile/", response_model=UserProfileResponse)
async def user_profile_update(
    db: db_dep,
    current_user: current_user_basic_dep,
    update_data: UserProfileUpdateRequest,
):
    for attr, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, attr, value)

    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete("/profile/", status_code=204)
async def profile_delete(db: db_dep, current_user: current_user_basic_dep):
    current_user.is_active = False
    current_user.is_deleted = True
    current_user.deleted_email = current_user.email
    current_user.email = None

    db.commit()
