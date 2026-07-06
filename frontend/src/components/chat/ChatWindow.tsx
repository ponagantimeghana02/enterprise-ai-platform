import {
  Box,
} from "@mui/material";

import {
  useEffect,
  useRef,
} from "react";

import { Message } from "../../types/chat";

import MessageBubble from "./MessageBubble";
import EmptyState from "./EmptyState";
import TypingIndicator from "./TypingIndicator";

interface Props {
  messages: Message[];
  loading: boolean;
}

const ChatWindow = ({
  messages,
  loading,
}: Props) => {

  const bottomRef =
    useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  if (!messages.length && !loading) {
    return <EmptyState />;
  }

  return (
    <Box>

      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
        />
      ))}

      {loading && (
        <TypingIndicator />
      )}

      <div ref={bottomRef} />

    </Box>
  );
};

export default ChatWindow;