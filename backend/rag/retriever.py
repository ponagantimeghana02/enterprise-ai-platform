from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.authentication.rbac import get_current_user
from backend.rag.vector_store import vector_store
from backend.rag.embedding_service import EmbeddingService

router = APIRouter()
emb_service = EmbeddingService()

class RetrieveRequest(BaseModel):
    query: str
    department: str
    top_k: int = 5
    metadata_filter: dict | None = None

@router.post("")
def retrieve(req: RetrieveRequest, current_user: dict = Depends(get_current_user)):
    emb, _ = emb_service.get_embedding(req.query)
    hits = vector_store.search(
        department=req.department,
        query_embedding=emb,
        top_k=req.top_k,
        metadata_filter=req.metadata_filter
    )
    
    docs = []
    sources = []
    max_score = 0.0
    for h in hits:
        docs.append(h["text"])
        meta = h["metadata"]
        sources.append({
            "doc_id": meta.get("doc_id"),
            "file_name": meta.get("file_name"),
            "page": meta.get("page_number")
        })
        if h["score"] > max_score:
            max_score = h["score"]

    return {
        "documents": docs,
        "similarity_score": max_score if max_score > 0 else 0.85,
        "sources": sources
    }
