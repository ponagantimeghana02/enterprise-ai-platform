import time
import uuid
from backend.database import db

class ApprovalEngine:
    def __init__(self):
        self.approvals = {}

    def create_approval(self, app_type: str, details: str, requested_by: str) -> dict:
        app_id = f"APP_{uuid.uuid4().hex[:6].upper()}"
        approval = {
            "id": app_id,
            "type": app_type,
            "details": details,
            "requested_by": requested_by,
            "status": "Pending",
            "created_at": time.time(),
            "approved_by": None,
            "approval_date": None,
            "comments": ""
        }
        self.approvals[app_id] = approval
        return approval

    def approve(self, app_id: str, user_email: str, comments: str = "") -> dict:
        if app_id in self.approvals:
            app = self.approvals[app_id]
            app["status"] = "Approved"
            app["approved_by"] = user_email
            app["approval_date"] = time.time()
            app["comments"] = comments
            
            db.execute(
                "INSERT INTO audit_logs (user_id, action, endpoint, ip_address, status_code) VALUES (%s, %s, %s, %s, %s)",
                (None, f"Approve: {app_id}", f"/approvals/{app_id}/approve", "system", 200)
            )
            return app
        return {"error": "Approval request not found"}

    def reject(self, app_id: str, user_email: str, comments: str = "") -> dict:
        if app_id in self.approvals:
            app = self.approvals[app_id]
            app["status"] = "Rejected"
            app["approved_by"] = user_email
            app["approval_date"] = time.time()
            app["comments"] = comments
            
            db.execute(
                "INSERT INTO audit_logs (user_id, action, endpoint, ip_address, status_code) VALUES (%s, %s, %s, %s, %s)",
                (None, f"Reject: {app_id}", f"/approvals/{app_id}/reject", "system", 200)
            )
            return app
        return {"error": "Approval request not found"}

    def get_pending(self) -> list[dict]:
        return [v for v in self.approvals.values() if v["status"] == "Pending"]

    def get_history(self) -> list[dict]:
        return [v for v in self.approvals.values() if v["status"] != "Pending"]

approval_engine = ApprovalEngine()
