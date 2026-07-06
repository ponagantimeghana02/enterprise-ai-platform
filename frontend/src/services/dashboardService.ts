import api from "../api/axios";

export const dashboardService = {
  async getDashboard(filter: string) {
    const response = await api.get("/dashboard", {
      params: {
        filter,
      },
    });

    return response.data;
  },
};