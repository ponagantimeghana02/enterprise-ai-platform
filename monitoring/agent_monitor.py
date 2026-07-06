import time
import uuid
from collections import defaultdict


# =========================
# AGENT MONITOR SYSTEM
# =========================
class AgentMonitor:
    def __init__(self):
        self.active_agents = set()
        self.task_count = 0

        self.tool_usage = defaultdict(int)
        self.failed_executions = 0
        self.success_executions = 0

        self.execution_times = []
        self.tool_latencies = defaultdict(list)

        self.agent_cost = defaultdict(float)
        self.workflow_runs = 0

    # -------------------------
    # AGENT TRACKING
    # -------------------------
    def start_agent(self, name: str):
        self.active_agents.add(name)
        print(f"[MONITOR] Agent started: {name}")

    def stop_agent(self, name: str):
        self.active_agents.discard(name)
        print(f"[MONITOR] Agent stopped: {name}")

    # -------------------------
    # TASK TRACKING
    # -------------------------
    def start_task(self):
        self.task_count += 1
        task_id = str(uuid.uuid4())
        print(f"[MONITOR] Task started: {task_id}")
        return task_id

    # -------------------------
    # TOOL USAGE
    # -------------------------
    def log_tool_usage(self, tool_name: str):
        self.tool_usage[tool_name] += 1
        print(f"[MONITOR] Tool used: {tool_name}")

    # -------------------------
    # EXECUTION SUCCESS
    # -------------------------
    def log_success(self, execution_time: float):
        self.success_executions += 1
        self.workflow_runs += 1
        self.execution_times.append(execution_time)
        print(f"[MONITOR] Success | Time: {execution_time:.3f}s")

    def log_failure(self):
        self.failed_executions += 1
        self.workflow_runs += 1
        print("[MONITOR] Execution Failed")

    # -------------------------
    # TOOL LATENCY
    # -------------------------
    def log_tool_latency(self, tool_name: str, latency: float):
        self.tool_latencies[tool_name].append(latency)

    # -------------------------
    # COST TRACKING
    # -------------------------
    def log_cost(self, agent: str, cost: float):
        self.agent_cost[agent] += cost

    # -------------------------
    # ANALYTICS
    # -------------------------
    def get_success_rate(self):
        if self.workflow_runs == 0:
            return 0
        return self.success_executions / self.workflow_runs

    def get_avg_execution_time(self):
        if not self.execution_times:
            return 0
        return sum(self.execution_times) / len(self.execution_times)

    def get_tool_latency(self):
        return {
            tool: sum(times) / len(times)
            for tool, times in self.tool_latencies.items()
        }

    # -------------------------
    # DASHBOARD
    # -------------------------
    def dashboard(self):
        return {
            "active_agents": list(self.active_agents),
            "running_tasks": self.task_count,
            "tool_usage": dict(self.tool_usage),
            "workflow_success_rate": self.get_success_rate(),
            "failed_executions": self.failed_executions,
            "avg_execution_time": self.get_avg_execution_time(),
            "tool_latency": self.get_tool_latency(),
            "agent_cost": dict(self.agent_cost),
        }


# =========================
# SINGLETON INSTANCE
# =========================
agent_monitor = AgentMonitor()


# =========================
# DEMO / TEST (SAME FILE)
# =========================
if __name__ == "__main__":

    print("\n🚀 STARTING AGENT MONITOR DEMO\n")

    # Start agents
    agent_monitor.start_agent("ResearchAgent")
    agent_monitor.start_agent("PlannerAgent")

    # Start task
    task_id = agent_monitor.start_task()

    # Tool usage simulation
    agent_monitor.log_tool_usage("hybrid_search")
    agent_monitor.log_tool_usage("bm25_search")

    # Simulate execution time
    start = time.time()
    time.sleep(0.3)
    end = time.time()

    agent_monitor.log_success(end - start)

    # Cost tracking
    agent_monitor.log_cost("ResearchAgent", 0.003)
    agent_monitor.log_cost("PlannerAgent", 0.002)

    # Tool latency simulation
    agent_monitor.log_tool_latency("hybrid_search", 0.12)
    agent_monitor.log_tool_latency("bm25_search", 0.08)

    # Stop agents
    agent_monitor.stop_agent("ResearchAgent")
    agent_monitor.stop_agent("PlannerAgent")

    # FINAL DASHBOARD
    print("\n📊 FINAL DASHBOARD:\n")
    import pprint
    pprint.pprint(agent_monitor.dashboard())