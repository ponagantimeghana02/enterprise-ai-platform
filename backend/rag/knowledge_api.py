from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from backend.authentication.rbac import get_current_user
from backend.database import db
from backend.rag.vector_store import vector_store
from backend.rag.embedding_service import EmbeddingService

router = APIRouter()
emb_service = EmbeddingService()

class SearchRequest(BaseModel):
    query: str
    department: str
    limit: int = 5

@router.get("")
def list_documents(
    department: str | None = None,
    status: str | None = None,
    owner: str | None = None,
    limit: int = 20,
    offset: int = 0,
    sort_by: str = "created_at",
    current_user: dict = Depends(get_current_user)
):
    query = "SELECT id, title, file_name, document_type, department, owner, version, status, created_at FROM documents WHERE 1=1"
    params = []
    if department:
        query += " AND department = %s"
        params.append(department)
    if status:
        query += " AND status = %s"
        params.append(status)
    if owner:
        query += " AND owner = %s"
        params.append(owner)
    
    if sort_by in ["id", "title", "department", "created_at", "status"]:
        query += f" ORDER BY {sort_by} DESC"
    else:
        query += " ORDER BY created_at DESC"
        
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    rows = db.execute(query, tuple(params), fetch=True)
    return [
        {
            "id": r[0],
            "title": r[1],
            "file_name": r[2],
            "document_type": r[3],
            "department": r[4],
            "owner": r[5],
            "version": r[6],
            "status": r[7],
            "created_at": r[8]
        }
        for r in rows
    ]

@router.get("/{doc_id}")
def get_document(doc_id: int, current_user: dict = Depends(get_current_user)):
    rows = db.execute(
        "SELECT id, title, file_name, document_type, department, owner, version, status, created_at FROM documents WHERE id = %s",
        (doc_id,),
        fetch=True
    )
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    r = rows[0]
    return {
        "id": r[0],
        "title": r[1],
        "file_name": r[2],
        "document_type": r[3],
        "department": r[4],
        "owner": r[5],
        "version": r[6],
        "status": r[7],
        "created_at": r[8]
    }

@router.put("/{doc_id}")
def update_document(doc_id: int, status: str, current_user: dict = Depends(get_current_user)):
    rows = db.execute("SELECT id FROM documents WHERE id = %s", (doc_id,), fetch=True)
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.execute(
        "UPDATE documents SET status = %s WHERE id = %s",
        (status, doc_id)
    )
    return {"id": doc_id, "status": status}

@router.delete("/{doc_id}")
def delete_document(doc_id: int, current_user: dict = Depends(get_current_user)):
    rows = db.execute("SELECT id, department FROM documents WHERE id = %s", (doc_id,), fetch=True)
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    
    dept = rows[0][1]
    vector_store.delete(dept, str(doc_id))
    db.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
    return {"status": "deleted"}

@router.post("/search")
def search_documents(req: SearchRequest, current_user: dict = Depends(get_current_user)):
    emb, _ = emb_service.get_embedding(req.query)
    results = vector_store.search(
        department=req.department,
        query_embedding=emb,
        top_k=req.limit
    )
    return {"results": results}
