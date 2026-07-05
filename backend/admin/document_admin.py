from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.authentication.rbac import RBACChecker
from backend.database import db
from backend.rag.vector_store import vector_store

router = APIRouter(dependencies=[Depends(RBACChecker(["Admin", "HR", "Manager"]))])

class BulkDeleteRequest(BaseModel):
    document_ids: list[int]

class RestoreVersionRequest(BaseModel):
    version: str

@router.post("/{doc_id}/approve")
def approve_document(doc_id: int):
    rows = db.execute("SELECT id FROM documents WHERE id = %s", (doc_id,), fetch=True)
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    db.execute("UPDATE documents SET status = 'Approved' WHERE id = %s", (doc_id,))
    return {"status": "Approved"}

@router.post("/{doc_id}/reject")
def reject_document(doc_id: int):
    rows = db.execute("SELECT id FROM documents WHERE id = %s", (doc_id,), fetch=True)
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    db.execute("UPDATE documents SET status = 'Rejected' WHERE id = %s", (doc_id,))
    return {"status": "Rejected"}

@router.post("/{doc_id}/archive")
def archive_document(doc_id: int):
    rows = db.execute("SELECT id FROM documents WHERE id = %s", (doc_id,), fetch=True)
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    db.execute("UPDATE documents SET status = 'Archived' WHERE id = %s", (doc_id,))
    return {"status": "Archived"}

@router.get("/{doc_id}/versions")
def get_versions(doc_id: int):
    rows = db.execute(
        "SELECT version, uploaded_by, approved_by, approval_date FROM document_versions WHERE document_id = %s",
        (doc_id,),
        fetch=True
    )
    return [
        {
            "version": r[0],
            "uploaded_by": r[1],
            "approved_by": r[2],
            "approval_date": r[3]
        }
        for r in rows
    ]

@router.post("/{doc_id}/restore-version")
def restore_version(doc_id: int, req: RestoreVersionRequest):
    rows = db.execute("SELECT id FROM documents WHERE id = %s", (doc_id,), fetch=True)
    if not rows:
        raise HTTPException(status_code=404, detail="Document not found")
    
    ver_rows = db.execute(
        "SELECT id FROM document_versions WHERE document_id = %s AND version = %s",
        (doc_id, req.version),
        fetch=True
    )
    if not ver_rows:
        raise HTTPException(status_code=404, detail="Version not found")
        
    db.execute(
        "UPDATE documents SET version = %s WHERE id = %s",
        (req.version, doc_id)
    )
    return {"status": "restored", "version": req.version}

@router.post("/bulk-delete")
def bulk_delete(req: BulkDeleteRequest):
    for doc_id in req.document_ids:
        rows = db.execute("SELECT id, department FROM documents WHERE id = %s", (doc_id,), fetch=True)
        if rows:
            dept = rows[0][1]
            vector_store.delete(dept, str(doc_id))
            db.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
    return {"status": "bulk_deleted", "count": len(req.document_ids)}

@router.get("/audit-logs")
def get_document_audit_logs():
    rows = db.execute(
        "SELECT id, user_id, action, endpoint, ip_address, status_code, timestamp FROM audit_logs WHERE endpoint LIKE '%document%' OR endpoint LIKE '%knowledge%' ORDER BY timestamp DESC LIMIT 100",
        fetch=True
    )
    return [
        {
            "id": r[0],
            "user_id": r[1],
            "action": r[2],
            "endpoint": r[3],
            "ip_address": r[4],
            "status_code": r[5],
            "timestamp": r[6]
        }
        for r in rows
    ]
