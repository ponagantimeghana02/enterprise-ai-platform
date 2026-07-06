import uuid

class WorkflowEngine:
    def __init__(self):
        self.workflows = {}

    def start_leave_workflow(self, employee_id: str, dates: list[str], leave_type: str) -> dict:
        wf_id = f"WF_{uuid.uuid4().hex[:6].upper()}"
        context = {
            "workflow_id": wf_id,
            "employee_id": employee_id,
            "dates": dates,
            "leave_type": leave_type,
            "status": "Running",
            "current_step": "Check Leave Balance",
            "progress": "20%",
            "history": []
        }
        
        context["history"].append("Check Leave Balance: Success")
        context["current_step"] = "Validate Dates"
        context["progress"] = "40%"
        
        context["history"].append("Validate Dates: Success")
        context["current_step"] = "Manager Approval"
        context["progress"] = "60%"
        
        self.workflows[wf_id] = context
        return context

    def get_workflow_status(self, wf_id: str) -> dict:
        return self.workflows.get(wf_id, {"error": "Workflow not found"})

    def cancel_workflow(self, wf_id: str) -> dict:
        if wf_id in self.workflows:
            self.workflows[wf_id]["status"] = "Cancelled"
            self.workflows[wf_id]["progress"] = "100%"
            return self.workflows[wf_id]
        return {"error": "Workflow not found"}

    def retry_workflow(self, wf_id: str) -> dict:
        if wf_id in self.workflows:
            self.workflows[wf_id]["status"] = "Running"
            self.workflows[wf_id]["current_step"] = "Calendar Update"
            self.workflows[wf_id]["progress"] = "80%"
            return self.workflows[wf_id]
        return {"error": "Workflow not found"}

workflow_engine = WorkflowEngine()
