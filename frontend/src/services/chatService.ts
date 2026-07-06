import api from "../api/axios";
import { ChatRequest, ChatResponse } from "../types/chat";

export const chatService = {
  async sendMessage(
    payload: ChatRequest
  ): Promise<ChatResponse> {
    const response = await api.post(
      "/chat",
      payload
    );

    return response.data;
  },
};