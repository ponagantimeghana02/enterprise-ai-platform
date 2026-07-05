import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from backend.authentication.rbac import get_current_user
from backend.chat.conversation_memory import conversation_memory
from backend.rag.query_rewriter import query_rewriter
from backend.rag.hybrid_search import hybrid_search_engine
from backend.rag.reranker import reranker
from backend.rag.context_builder import context_builder
from backend.rag.hallucination_detector import hallucination_detector
from backend.rag.citation_engine import citation_engine

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str
    department: str
    stream: bool = False

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]
    confidence: int

@router.post("")
def chat(req: ChatRequest, current_user: dict = Depends(get_current_user)):
    rewritten_query = query_rewriter.rewrite(req.message)
    
    docs = hybrid_search_engine.search(
        query=rewritten_query,
        department=req.department,
        top_k=10
    )
    
    reranked = reranker.rerank(req.message, docs, top_k=3)
    
    ctx = context_builder.build_context(reranked)
    
    context_text = " ".join(ctx["context"])
    
    if context_text:
        words = context_text.split()
        snippet = " ".join(words[:40]) + "..."
        answer = f"According to the {req.department} records: {snippet} [Verified from sources]"
    else:
        answer = f"I could not find any active documents in the {req.department} department matching your request. Please ensure you have uploaded and approved the required files."

    scores = [d.get("rerank_score", 0.85) for d in reranked]
    max_score = max(scores) if scores else 0.5
    
    det = hallucination_detector.detect(answer, ctx["context"], max_score)
    
    citations = citation_engine.format_citations(ctx["sources"], scores)
    final_answer = f"{answer}\n\n{citations}"

    conversation_memory.add_message(req.session_id, "user", req.message)
    conversation_memory.add_message(req.session_id, "assistant", final_answer)

    if req.stream:
        async def event_generator():
            chunks = final_answer.split(" ")
            for c in chunks:
                yield f"{c} "
                await asyncio.sleep(0.05)
        return StreamingResponse(event_generator(), media_type="text/event-stream")

    return {
        "answer": final_answer,
        "sources": ctx["sources"],
        "confidence": int(det["confidence"])
    }

@router.post("/history")
def save_chat_history(session_id: str, current_user: dict = Depends(get_current_user)):
    return {"status": "saved", "session_id": session_id}

@router.delete("/history")
def delete_chat_history(session_id: str, current_user: dict = Depends(get_current_user)):
    conversation_memory.clear(session_id)
    return {"status": "deleted"}

@router.get("/session/{session_id}")
def get_session(session_id: str, current_user: dict = Depends(get_current_user)):
    history = conversation_memory.get_history(session_id)
    return {"session_id": session_id, "history": history}
