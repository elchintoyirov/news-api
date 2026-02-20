from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "News API"
    DEBUG: bool = True
    APP_ENV: str = "development"

    DATABASE_URL: str

    OPENWEATHER_API_KEY: str | None = None

    LOG_LEVEL: str = "INFO"

    SECRET_KEY: str = "secret-key"

    SESSION_ID_EXPIRE_DAYS: int = 1
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    EMAIL_ADDRESS: str
    SMTP_SERVER: str
    SMTP_PORT: int = 587    
    EMAIL_PASSWORD: str | None = None

    REDIS_URL: str

    MEDIA_PATH: str = "media/"
    BASE_URL: str = "https://newsapi.uz"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

POSTGRES_URL = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
