from .auth.basic import router as basic_router
from .news import router as news_router
from .users import router as users_router
from .weather import router as weather_router
from .auth import auth_router as auth_router


__all__ = [
    "basic_router",
    "news_router",
    "users_router",
    "weather_router",
]
