from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.database.db import User
from backend.authentication.auth import get_current_user

router = APIRouter(prefix="/settings", tags=["Settings"])

class SettingsResponse(BaseModel):
    vector_db_url: str
    llm_api_key_configured: bool

@router.get("/", response_model=SettingsResponse)
def get_settings(current_user: User = Depends(get_current_user)):
    # This route is protected by RBAC middleware anyway, but we double-check here too
    if current_user.role.name != "Admin":
        raise HTTPException(status_code=403, detail="Admin role required")
        
    from backend.settings.config import settings
    return SettingsResponse(
        vector_db_url=settings.VECTOR_DB_URL,
        llm_api_key_configured=bool(settings.LLM_API_KEY)
    )
