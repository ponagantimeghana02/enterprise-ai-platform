import api from "../api/axios";

export const adminService = {
  getUsers: () => api.get("/admin/users"),

  createUser: (user: any) =>
    api.post("/admin/users", user),

  updateUser: (id: string, user: any) =>
    api.put(`/admin/users/${id}`, user),

  deleteUser: (id: string) =>
    api.delete(`/admin/users/${id}`),

  getAISettings: () =>
    api.get("/admin/settings"),

  updateAISettings: (settings: any) =>
    api.put("/admin/settings", settings),

  getAuditLogs: () =>
    api.get("/admin/audit-logs"),
};