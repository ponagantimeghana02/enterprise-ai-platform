export interface Analytics {
  aiRequests: number;
  cost: number;
  agentPerformance: number;
  ragAccuracy: number;
  hallucinationRate: number;
  responseTime: number;
  topKnowledgeSource: string;
  userSatisfaction: number;
}