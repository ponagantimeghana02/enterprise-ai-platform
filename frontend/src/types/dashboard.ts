export interface DashboardStats {
  activeAISessions: number;
  activeUsers: number;
  runningAgents: number;
  knowledgeBaseSize: number;
  todayQueries: number;
  averageResponseTime: number;
  tokenUsage: number;
  workflowStatus: string;
}

export interface DashboardResponse {
  stats: DashboardStats;
}