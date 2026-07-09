from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from backend.database import db

# Authentication
from backend.authentication.auth_api import router as auth_router

# Chat
from backend.chat.chat_api import router as chat_router

# Knowledge Base
from backend.rag.knowledge_api import router as knowledge_router
from backend.rag.retriever import router as retriever_router
from backend.rag.document_upload import router as document_router
from backend.admin.document_admin import router as doc_admin_router
from backend.multitenancy.tenant_middleware import TenantMiddleware
from backend.multitenancy.tenant_kb import get_documents
from backend.multitenancy.tenant_audit import log_action

# Vector Store
from backend.rag.vector_store import vector_store

# Monitoring
from monitoring.tracing import tracing_middleware
from monitoring.metrics import (
    router as metrics_router,
    metrics_middleware
)

app = FastAPI(
    title="BlackRoth Enterprise AI Platform Gateway",
    description="Unified entry point for Authentication, Chat, Knowledge Base, Document Upload and Retrieval.",
    version="1.0.0"
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --------------------------------------------------
# Middleware
# --------------------------------------------------

app.middleware("http")(tracing_middleware)
app.middleware("http")(metrics_middleware)

# --------------------------------------------------
# Routers
# --------------------------------------------------
app.add_middleware(TenantMiddleware)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["AI Chat"]
)

app.include_router(
    knowledge_router,
    prefix="/documents",
    tags=["Knowledge Base"]
)

app.include_router(
    retriever_router,
    prefix="/retrieve",
    tags=["Retriever"]
)

app.include_router(
    document_router,
    prefix="/upload",
    tags=["Document Upload"]
)

app.include_router(
    doc_admin_router,
    prefix="/admin/documents",
    tags=["Document Admin"]
)

app.include_router(metrics_router)

# --------------------------------------------------
# Root API
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "running",
        "application": "BlackRoth Enterprise AI Platform"
    }

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "database": "connected" if db.is_connected() else "disconnected",
        "vector_db": "connected" if vector_store.client else "disconnected",
        "llm": "connected",
        "status": "healthy"
    }
@app.get("/documents")

def documents(request: Request):

    tenant_id = request.headers["X-Tenant-ID"]

    docs = get_documents(
        tenant_id
    )

    log_action(
        tenant_id,
        "john",
        "Viewed Documents"
    )

    return {

        "tenant": tenant_id,

        "documents": docs
    }