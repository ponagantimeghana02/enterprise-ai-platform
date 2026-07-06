import api from "../api/axios";

export const analyticsService = {
  getAnalytics: () => api.get("/analytics"),

  exportCSV: () =>
    api.get("/analytics/export/csv", {
      responseType: "blob",
    }),

  exportPDF: () =>
    api.get("/analytics/export/pdf", {
      responseType: "blob",
    }),
};