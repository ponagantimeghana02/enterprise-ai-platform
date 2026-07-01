from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.database.db import User
from backend.authentication.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    # Standard Chat functionality placeholder
    return ChatResponse(
        response=f"Hello {current_user.name}, you said: '{request.message}'. This is a response from the Chat Module."
    )
