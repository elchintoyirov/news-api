from .bauth import router as bauth_router
from .news import router as news_router
from .users import router as users_router
from .weather import router as weather_router

__all__ = [
    "bauth_router",
    "news_router",
    "users_router",
    "weather_router", 
]