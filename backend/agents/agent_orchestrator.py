from backend.agents.function_router import function_router

class AgentOrchestrator:
    def __init__(self):
        self.agents = [
            "HR Agent",
            "Payroll Agent",
            "Knowledge Agent",
            "Project Management Agent",
            "Analytics Agent",
            "Customer Support Agent"
        ]

    def route_query(self, query: str) -> str:
        q = query.lower()
        if "leave" in q or "vacation" in q or "onboarding" in q:
            return "HR Agent"
        elif "payroll" in q or "salary" in q or "payslip" in q:
            return "Payroll Agent"
        elif "project" in q or "milestone" in q or "task" in q:
            return "Project Management Agent"
        elif "analytics" in q or "metric" in q or "cost" in q:
            return "Analytics Agent"
        elif "support" in q or "ticket" in q or "help" in q:
            return "Customer Support Agent"
        else:
            return "Knowledge Agent"

    def execute_agent_task(self, query: str) -> dict:
        agent = self.route_query(query)
        result = {}
        
        try:
            if agent == "HR Agent":
                result = function_router.execute("get_employee", {"employee_id": "EMP_001"})
            elif agent == "Payroll Agent":
                result = function_router.execute("generate_payroll", {"employee_id": "EMP_001", "month": "July"})
            elif agent == "Project Management Agent":
                result = function_router.execute("get_project_status", {"project_id": "PRJ_44"})
            elif agent == "Knowledge Agent":
                result = function_router.execute("search_documents", {"query": query, "department": "HR"})
            else:
                result = {"result": f"Completed general request via {agent}", "status": "Success"}
        except Exception as e:
            result = {"error": str(e), "status": "Failed", "recovery": "Routing fallback to knowledge base"}
            
        return {
            "routed_agent": agent,
            "execution_status": result.get("status", "Failed"),
            "data": result.get("result", result.get("error"))
        }

agent_orchestrator = AgentOrchestrator()
