from decouple import config

APP_ENV = config("APP_ENV", default="development")
DEBUG = config("DEBUG", default=True, cast=bool)

DATABASE_URL = config("DATABASE_URL")
POSTGRES_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

OPENWEATHER_API_KEY =  config("OPENWEATHER_API_KEY")

LOG_LEVEL = config("LOG_LEVEL", default="INFO")
