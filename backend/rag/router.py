from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.database.db import User
from backend.authentication.auth import get_current_user

router = APIRouter(prefix="/rag", tags=["RAG"])

class RAGQueryRequest(BaseModel):
    query: str

class RAGQueryResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/query", response_model=RAGQueryResponse)
def query_rag(request: RAGQueryRequest, current_user: User = Depends(get_current_user)):
    return RAGQueryResponse(
        answer=f"Retrieval-Augmented Generation answer for query '{request.query}'. Retrieved 2 documents.",
        sources=["doc_1.txt", "doc_2.pdf"]
    )
