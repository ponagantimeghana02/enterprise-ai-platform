import { Box } from "@mui/material";
import { useEffect, useState } from "react";

import ChatHeader from "../../components/chat/ChatHeader";
import ChatSidebar from "../../components/chat/ChatSidebar";
import ChatWindow from "../../components/chat/ChatWindow";
import MessageInput from "../../components/chat/MessageInput";
import { chatService } from "../../services/chatService";

import { Message } from "../../types/chat";
import { Conversation } from "../../types/conversation";

import { conversationService } from "../../services/conversationService";

const Chat = () => {
  // Chat Messages
  const [messages, setMessages] = useState<Message[]>([]);

  // Sidebar State
  const [search, setSearch] = useState("");

  const [selectedConversation, setSelectedConversation] =
    useState("");

  const [conversations, setConversations] =
    useState<Conversation[]>([]);
    const [loading, setLoading] =
  useState(false);

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      const history =
        await conversationService.getHistory();

      setConversations(history.conversations);

      if (history.conversations.length > 0) {
        setSelectedConversation(
          history.conversations[0].id
        );
      }
    } catch (error) {
      console.error(
        "Failed to load conversations",
        error
      );
    }
  }

  async function sendMessage(
  text: string
) {

  if (!selectedConversation)
    return;

  const userMessage: Message = {

    id: crypto.randomUUID(),

    role: "user",

    content: text,

    createdAt:
      new Date().toISOString(),

  };

  setMessages((prev) => [
    ...prev,
    userMessage,
  ]);

  try {

    setLoading(true);

    const response =
      await chatService.sendMessage({

        conversationId:
          selectedConversation,

        message: text,

      });

    const aiMessage: Message = {

      id: response.id,

      role: "assistant",

      content:
        response.message,

      createdAt:
        new Date().toISOString(),

      sources:
        response.sources,

    };

    setMessages((prev) => [
      ...prev,
      aiMessage,
    ]);

  } catch {

    const errorMessage: Message = {

      id: crypto.randomUUID(),

      role: "assistant",

      content:
        "Something went wrong while contacting the AI service.",

      createdAt:
        new Date().toISOString(),

    };

    setMessages((prev) => [
      ...prev,
      errorMessage,
    ]);

  } finally {

    setLoading(false);

  }

}
  function handleNewConversation() {
    const newConversation: Conversation = {
      id: crypto.randomUUID(),
      title: "New Conversation",
      updatedAt: new Date().toISOString(),
    };

    setConversations((prev) => [
      newConversation,
      ...prev,
    ]);

    setSelectedConversation(newConversation.id);

    setMessages([]);
  }

  function handleRenameConversation(id: string) {
    const title = window.prompt(
      "Enter new conversation name"
    );

    if (!title) return;

    setConversations((prev) =>
      prev.map((conversation) =>
        conversation.id === id
          ? {
              ...conversation,
              title,
            }
          : conversation
      )
    );
  }

  function handleDeleteConversation(id: string) {
    if (
      !window.confirm(
        "Delete this conversation?"
      )
    )
      return;

    setConversations((prev) =>
      prev.filter(
        (conversation) =>
          conversation.id !== id
      )
    );

    if (selectedConversation === id) {
      setSelectedConversation("");
      setMessages([]);
    }
  }

  return (
    <Box display="flex" height="100vh">
      <ChatSidebar
        conversations={conversations}
        selectedId={selectedConversation}
        search={search}
        onSearch={setSearch}
        onSelect={setSelectedConversation}
        onNew={handleNewConversation}
        onRename={handleRenameConversation}
        onDelete={handleDeleteConversation}
      />

      <Box
        flex={1}
        display="flex"
        flexDirection="column"
      >
        <ChatHeader />

        <Box
          flex={1}
          p={3}
          sx={{
            overflowY: "auto",
          }}
        >
          <ChatWindow messages={messages} />
        </Box>

        <Box
          p={2}
          borderTop="1px solid #e0e0e0"
        >
          <MessageInput
            onSend={sendMessage}
          />
        </Box>
      </Box>
    </Box>
  );
};


export default Chat;


