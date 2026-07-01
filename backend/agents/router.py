from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.database.db import User
from backend.authentication.auth import get_current_user

router = APIRouter(prefix="/agents", tags=["Agents"])

class AgentTaskRequest(BaseModel):
    task: str

class AgentTaskResponse(BaseModel):
    task_id: str
    status: str
    result: str

@router.post("/run", response_model=AgentTaskResponse)
def run_agent_task(request: AgentTaskRequest, current_user: User = Depends(get_current_user)):
    return AgentTaskResponse(
        task_id="task_abc123",
        status="completed",
        result=f"Agent completed task: '{request.task}'."
    )
