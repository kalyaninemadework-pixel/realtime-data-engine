"""Application configuration using environment variables."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://kalyani:password@db:5432/dataengine"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # App
    APP_NAME: str = "Real-Time Data Engine"
    DEBUG: bool = False
    WORKERS: int = 4

    # Pipeline
    BATCH_SIZE: int = 100
    PIPELINE_INTERVAL_MS: int = 100
    MAX_QUEUE_SIZE: int = 10000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
