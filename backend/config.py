import os


class Settings:
    APP_NAME = "Enterprise AI Platform"
    APP_VERSION = "1.0.0"

    HOST = "0.0.0.0"
    PORT = 8000

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/enterprise_ai"
    )

    VECTOR_DB = os.getenv("VECTOR_DB", "chroma")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")


settings = Settings()