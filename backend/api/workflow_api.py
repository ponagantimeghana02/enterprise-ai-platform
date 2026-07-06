from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List
import uuid

router = APIRouter(
    prefix="/workflow",
    tags=["Enterprise Workflow APIs"]
)


class WorkflowStartRequest(BaseModel):
    workflow_name: str
    initiated_by: str


class WorkflowCancelRequest(BaseModel):
    workflow_id: str


class WorkflowRetryRequest(BaseModel):
    workflow_id: str


class WorkflowResponse(BaseModel):
    workflow_id: str
    workflow_name: str
    status: str
    current_step: str
    progress: str
    initiated_by: str
    created_at: datetime


workflow_db: Dict[str, dict] = {}


def generate_workflow_id():
    return f"WF{str(uuid.uuid4().hex[:5]).upper()}"


@router.post("/start", response_model=WorkflowResponse)
def start_workflow(request: WorkflowStartRequest):

    workflow_id = generate_workflow_id()

    workflow = {
        "workflow_id": workflow_id,
        "workflow_name": request.workflow_name,
        "status": "Running",
        "current_step": "Manager Approval",
        "progress": "60%",
        "initiated_by": request.initiated_by,
        "created_at": datetime.now()
    }

    workflow_db[workflow_id] = workflow

    return workflow


@router.get("/{workflow_id}")
def get_workflow(workflow_id: str):

    if workflow_id not in workflow_db:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return workflow_db[workflow_id]


@router.post("/cancel")
def cancel_workflow(request: WorkflowCancelRequest):

    workflow = workflow_db.get(request.workflow_id)

    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow["status"] = "Cancelled"
    workflow["current_step"] = "Workflow Cancelled"

    return {
        "message": "Workflow cancelled successfully",
        "workflow": workflow
    }


@router.post("/retry")
def retry_workflow(request: WorkflowRetryRequest):

    workflow = workflow_db.get(request.workflow_id)

    if workflow is None:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow["status"] = "Running"
    workflow["current_step"] = "Manager Approval"
    workflow["progress"] = "60%"

    return {
        "message": "Workflow restarted successfully",
        "workflow": workflow
    }


@router.get("/history")
def workflow_history():

    return {
        "total_workflows": len(workflow_db),
        "history": list(workflow_db.values())
    }