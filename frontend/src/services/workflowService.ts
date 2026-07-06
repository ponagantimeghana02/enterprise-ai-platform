import api from "../api/axios";

export const workflowService = {
  getWorkflows: () =>
    api.get("/workflow/history"),

  retryWorkflow: (id: string) =>
    api.post(`/workflow/retry/${id}`),
};