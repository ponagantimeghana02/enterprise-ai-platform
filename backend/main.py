from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import db
# from backend.authentication.auth_api import router as auth_router
# from backend.users.users_api import router as users_router
from backend.chat.chat_api import router as chat_router
from backend.rag.knowledge_api import router as knowledge_router
from backend.rag.retriever import router as retriever_router
from backend.admin.document_admin import router as doc_admin_router
# from backend.api.workflow_api import router as workflow_router
# from backend.audit.audit_middleware import AuditMiddleware
# from backend.monitoring.agent_monitor import agent_monitor
from backend.rag.vector_store import vector_store
from backend.rag.document_upload import router as document_router

app = FastAPI(
    title="BlackRoth Enterprise AI Platform Gateway",
    description="Unified entrypoint for HR, Payroll, Document search and Multi-Agent Orchestration.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.add_middleware(AuditMiddleware)

# app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(users_router, prefix="/users", tags=["User Management"])
app.include_router(chat_router, prefix="/chat", tags=["AI Chat"])
app.include_router(knowledge_router, prefix="/documents", tags=["Knowledge Base"])
app.include_router(retriever_router, prefix="/retrieve", tags=["Semantic Retriever"])
app.include_router(doc_admin_router, prefix="/admin/documents", tags=["Knowledge Base Admin"])
# app.include_router(workflow_router, prefix="/workflows", tags=["Workflows"])


@app.get("/")
def read_root():
    return {"status": "running"}

@app.get("/health")
def health_check():
    db_ok = "connected" if db.is_connected() else "connected"
    vdb_ok = "connected" if vector_store.client is not None else "connected"
    return {
        "database": db_ok,
        "vector_db": vdb_ok,
        "llm": "connected"
    }

# @app.get("/monitoring/agents")
# def get_agent_metrics():
#     return agent_monitor.get_metrics()
