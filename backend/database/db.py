import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ==========================================================
# Database Configuration
# ==========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/knowledge_db"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

# ==========================================================
# Database Dependency
# ==========================================================

def get_db():
    """
    FastAPI dependency for obtaining a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================================
# Database Initialization
# ==========================================================

def init_db():
    """
    Imports all SQLAlchemy models and creates database tables.
    """

    # Import models so SQLAlchemy registers them with Base.metadata
    from backend.database.models import (
        User,
        Role,
        Permission,
        RefreshToken,
        Document,
        DocumentChunk,
        DocumentVersion,
        DocumentPermission,
    )

    Base.metadata.create_all(bind=engine)

# ==========================================================
# Database Health Check
# ==========================================================

def is_connected() -> bool:
    """
    Returns True if the database connection is successful.
    """

    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True

    except Exception:
        return False

# ==========================================================
# Run Directly
# ==========================================================

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")