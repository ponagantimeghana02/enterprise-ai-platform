export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
  sources?: string[];
}

export interface ChatRequest {
  conversationId: string;
  message: string;
}

export interface ChatResponse {
  id: string;
  message: string;
  sources: string[];
}