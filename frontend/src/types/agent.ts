export interface Agent {
  id: string;
  name: string;
  status: string;
  health: string;
  runningTasks: number;
  toolUsage: number;
  logs: string;
  memory: string;
}