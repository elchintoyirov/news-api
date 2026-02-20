from fastapi import APIRouter

from .register import router as register_router
from .basic import router as basic_auth_router
from .session import router as session_auth_router
from .gwt import router as jwt_auth_router


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(register_router)
router.include_router(basic_auth_router)
router.include_router(session_auth_router)
router.include_router(jwt_auth_router)
