import {
  Avatar,
  Box,
  Paper,
  Stack,
} from "@mui/material";

import ReactMarkdown from "react-markdown";

import { Message } from "../../types/chat";

import CopyButton from "./CopyButton";
import FeedbackButtons from "./FeedbackButtons";
import SourceCitation from "./SourceCitation";

interface Props {
  message: Message;
}

const MessageBubble = ({
  message,
}: Props) => {

  const assistant =
    message.role === "assistant";

  return (

    <Stack
      direction="row"
      justifyContent={
        assistant
          ? "flex-start"
          : "flex-end"
      }
      mb={2}
    >

      {assistant && (
        <Avatar sx={{ mr: 2 }}>
          AI
        </Avatar>
      )}

      <Paper
        sx={{
          maxWidth: "70%",
          p: 2,
          borderRadius: 3,
        }}
      >

        <ReactMarkdown>

          {message.content}

        </ReactMarkdown>

        {assistant && (

          <Box
            mt={2}
            display="flex"
            justifyContent="space-between"
            alignItems="center"
          >

            <CopyButton
              text={message.content}
            />

            <FeedbackButtons
              messageId={message.id}
            />

          </Box>

        )}

        {assistant && message.sources && (
  <SourceCitation
    sources={message.sources}
  />
)}

    

      </Paper>

    </Stack>

  );

};

export default MessageBubble;