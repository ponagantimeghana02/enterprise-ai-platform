import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    JWT_SECRET_KEY: str ="secret_key "
    JWT_REFRESH_SECRET_KEY: str = "refresh_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    VECTOR_DB_URL: str = "http://localhost:6333"
    LLM_API_KEY: str = "mock_llm_key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Load settings instance
settings = Settings()
