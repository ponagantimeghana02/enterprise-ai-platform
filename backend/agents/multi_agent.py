from backend.rag.hybrid_search import hybrid_search_engine


# -----------------------------
# RESEARCH AGENT
# -----------------------------
class ResearchAgent:
    def run(self, query: str, department: str = "General"):
        print("[ResearchAgent] Searching knowledge base...")

        return hybrid_search_engine.search(
            query=query,
            department=department,
            top_k=5
        )


# -----------------------------
# HR AGENT
# -----------------------------
class HRAgent:
    def run(self, query: str):
        print("[HRAgent] Fetching HR information...")

        return hybrid_search_engine.search(
            query=query,
            department="HR",
            top_k=5
        )


# -----------------------------
# PLANNER AGENT
# -----------------------------
class PlannerAgent:
    def run(self, query: str):
        print("[PlannerAgent] Creating plan...")

        return {
            "steps": [
                "Understand query",
                "Retrieve knowledge",
                "Execute tools",
                "Validate result"
            ],
            "query": query
        }


# -----------------------------
# EXECUTOR AGENT
# -----------------------------
class ExecutorAgent:
    def run(self, plan: dict, research_results: list):
        print("[ExecutorAgent] Executing plan...")

        return {
            "status": "executed",
            "plan": plan,
            "results_used": research_results[:3]
        }


# -----------------------------
# VALIDATOR AGENT
# -----------------------------
class ValidatorAgent:
    def run(self, output: dict):
        print("[ValidatorAgent] Validating...")

        if not output.get("results_used"):
            return {"valid": False, "reason": "No results found"}

        return {
            "valid": True,
            "final_response": output
        }


# -----------------------------
# MULTI AGENT SYSTEM
# -----------------------------
class MultiAgentSystem:
    def __init__(self):
        self.research = ResearchAgent()
        self.hr = HRAgent()
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.validator = ValidatorAgent()

    def run(self, query: str, department: str = "HR"):
        print("\n=== START MULTI-AGENT WORKFLOW ===")

        # 1. Research
        research_results = self.research.run(query, department)

        # 2. Planning
        plan = self.planner.run(query)

        # 3. Execution
        execution = self.executor.run(plan, research_results)

        # 4. Validation
        result = self.validator.run(execution)

        print("=== END WORKFLOW ===\n")

        return result


# -----------------------------
# INSTANCE
# -----------------------------
multi_agent_system = MultiAgentSystem()


# =============================
# 🧪 TESTING (INSIDE SAME FILE)
# =============================
if __name__ == "__main__":

    print("\n🚀 Running Multi-Agent Test...\n")

    test_query = "vacation leave entitlement policy"

    output = multi_agent_system.run(
        query=test_query,
        department="HR"
    )

    print("\n📌 FINAL OUTPUT:")
    print(output)