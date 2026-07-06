import api from "../api/axios";
import { KnowledgeResponse } from "../types/knowledge";

export const knowledgeService = {
  async getDocuments(): Promise<KnowledgeResponse> {
    const response = await api.get("/knowledge");
    return response.data;
  },

  async uploadDocument(file: File) {
    const formData = new FormData();
    formData.append("file", file);

    return api.post("/knowledge/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },

  async deleteDocument(id: string) {
    return api.delete(`/knowledge/${id}`);
  },
  async downloadDocument(id: string) {
  return api.get(`/knowledge/${id}/download`, {
    responseType: "blob",
  });
},

async previewDocument(id: string) {
  return api.get(`/knowledge/${id}/preview`);
},
};
