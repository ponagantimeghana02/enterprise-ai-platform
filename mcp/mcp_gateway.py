import time

class MCPGateway:
    def __init__(self):
        self.tools = {}
        self.register_default_tools()

    def register_default_tools(self):
        default_tools = [
            "Employee Service",
            "Payroll Service",
            "Leave Service",
            "Project Service",
            "Knowledge Base",
            "Email Service",
            "Calendar Service",
            "Notification Service"
        ]
        for name in default_tools:
            self.register_tool(name, "1.0")

    def register_tool(self, name: str, version: str):
        self.tools[name] = {
            "version": version,
            "status": "Healthy",
            "last_checked": time.time()
        }

    def get_tools(self) -> dict:
        return self.tools

    def execute_tool(self, tool_name: str, params: dict, retries: int = 3) -> dict:
        if tool_name not in self.tools:
            return {"error": "Tool not found", "status": "Failed"}
            
        attempts = 0
        while attempts < retries:
            try:
                self.tools[tool_name]["last_checked"] = time.time()
                return {"result": f"Executed {tool_name} successfully", "status": "Success"}
            except Exception:
                attempts += 1
                
        self.tools[tool_name]["status"] = "Degraded"
        return {"error": "Execution failed after retries", "status": "Failed"}

    def health_check(self) -> dict:
        for t in self.tools:
            self.tools[t]["status"] = "Healthy"
            self.tools[t]["last_checked"] = time.time()
        return self.tools

mcp_gateway = MCPGateway()
