import os
import hashlib
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from pypdf import PdfReader
from docx import Document as DocxDocument
from backend.authentication.rbac import get_current_user
from backend.database import db
from backend.settings.config import settings

router = APIRouter()

def hash_file(file_content: bytes) -> str:
    return hashlib.md5(file_content).hexdigest()

def extract_text(file_content: bytes, file_name: str) -> str:
    ext = os.path.splitext(file_name)[1].lower()
    if ext == ".pdf":
        from io import BytesIO
        pdf = PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text
    elif ext == ".docx":
        from io import BytesIO
        doc = DocxDocument(BytesIO(file_content))
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    elif ext in [".txt", ".md", ".markdown"]:
        return file_content.decode("utf-8", errors="ignore")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    department: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    content = await file.read()
    size = len(content)
    if size > settings.max_file_size_bytes:
        raise HTTPException(status_code=400, detail="File too large")
        
    mime_type = file.content_type
    if mime_type not in settings.allowed_mime_types:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".pdf", ".docx", ".txt", ".md"]:
            raise HTTPException(status_code=400, detail="Unsupported MIME type")

    file_hash = hash_file(content)
    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = os.path.join(settings.upload_dir, file.filename)
    
    existing = db.execute(
        "SELECT id FROM documents WHERE file_name = %s",
        (file.filename,),
        fetch=True
    )
    if existing:
        raise HTTPException(status_code=400, detail="Duplicate file name detected")

    with open(file_path, "wb") as f:
        f.write(content)

    try:
        text = extract_text(content, file.filename)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Failed to extract text: {str(e)}")

    db.execute(
        "INSERT INTO documents (title, file_name, document_type, department, owner, version, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (file.filename, file.filename, file.content_type or "text/plain", department, current_user["email"], "1.0", "Pending")
    )
    
    doc = db.execute(
        "SELECT id FROM documents WHERE file_name = %s",
        (file.filename,),
        fetch=True
    )
    doc_id = doc[0][0]
    
    db.execute(
        "INSERT INTO document_versions (document_id, version, uploaded_by) VALUES (%s, %s, %s)",
        (doc_id, "1.0", current_user["email"])
    )

    return {
        "document_id": doc_id,
        "filename": file.filename,
        "size": size,
        "extracted_length": len(text),
        "status": "Pending"
    }
