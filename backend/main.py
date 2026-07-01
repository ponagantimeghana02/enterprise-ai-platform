import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import DB and seeding helper
from backend.database.db import init_db, get_db

# Import Routers
from backend.authentication.router import router as auth_router
from backend.users.router import router as users_router
from backend.chat.router import router as chat_router
from backend.rag.router import router as rag_router
from backend.agents.router import router as agents_router
from backend.settings.router import router as settings_router
from backend.hr_finance_mock_router import router as hr_finance_router

# Import Middleware
from backend.audit.middleware import AuditAndRBACMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and seed roles/permissions/admin
    logger.info("Initializing database...")
    init_db()
    yield
    logger.info("Shutdown completed.")

app = FastAPI(
    title="FastAPI Backend",
    description="A modular backend with JWT Authentication, RBAC, and Audit Logging",
    version="1.0.0",
    lifespan=lifespan
)

# Register Audit & RBAC Middleware
app.add_middleware(AuditAndRBACMiddleware)

# Register Module Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chat_router)
app.include_router(rag_router)
app.include_router(agents_router)
app.include_router(settings_router)
app.include_router(hr_finance_router)

# GET /
@app.get("/", tags=["General"])
def read_root():
    return {"status": "running"}

# GET /health
@app.get("/health", tags=["General"])
def health_check(db: Session = Depends(get_db)):
    # 1. Verify database connection
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "disconnected"
        
    # 2. Verify Vector DB connection (mock status)
    vector_db_status = "connected"
    
    # 3. Verify LLM connection (mock status)
    llm_status = "connected"
    
    return {
        "database": db_status,
        "vector_db": vector_db_status,
        "llm": llm_status
    }
