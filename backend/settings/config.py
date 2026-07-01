import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    JWT_SECRET_KEY: str = "949f2b84cf63a6dc92d847bb06427d14d84ff0d046f4b3dfbbfa410940dc4113"
    JWT_REFRESH_SECRET_KEY: str = "e83a3d2e1c9e83a81283d81b83d5a23c4a2a1949f2b84cf63a6dc92d847bb0642"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    VECTOR_DB_URL: str = "http://localhost:6333"
    LLM_API_KEY: str = "mock_llm_key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Load settings instance
settings = Settings()
