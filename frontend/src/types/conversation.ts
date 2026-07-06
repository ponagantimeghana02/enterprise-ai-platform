export interface Conversation {
  id: string;
  title: string;
  updatedAt: string;
}

export interface ConversationHistoryResponse {
  conversations: Conversation[];
}