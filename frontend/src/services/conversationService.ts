import api from "../api/axios";
import { ConversationHistoryResponse } from "../types/conversation";

export const conversationService = {
  async getHistory(): Promise<ConversationHistoryResponse> {
    const response = await api.get("/chat/history");
    return response.data;
  },

  async renameConversation(id: string, title: string) {
    return api.put(`/chat/${id}`, {
      title,
    });
  },

  async deleteConversation(id: string) {
    return api.delete(`/chat/${id}`);
  },
};