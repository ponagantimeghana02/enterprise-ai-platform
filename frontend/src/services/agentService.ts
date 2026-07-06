import api from "../api/axios";

export const agentService = {
  getAgents: () => api.get("/agents"),

  startAgent: (id: string) =>
    api.post(`/agents/${id}/start`),

  stopAgent: (id: string) =>
    api.post(`/agents/${id}/stop`),

  restartAgent: (id: string) =>
    api.post(`/agents/${id}/restart`),
};