import {
  Button,
  Stack,
  TextField,
} from "@mui/material";

import {
  useState,
} from "react";

interface Props {
  onSend: (
    message: string
  ) => void;
}

const MessageInput = ({
  onSend,
}: Props) => {

  const [message, setMessage] =
    useState("");

  function send() {

    if (!message.trim()) return;

    onSend(message);

    setMessage("");

  }

  return (

    <Stack
      direction="row"
      spacing={2}
    >

      {/* <TextField
        fullWidth
        placeholder="Ask AI anything..."
        value={message}
        onChange={(e) =>
          setMessage(
            e.target.value
          )
        }
      /> */}
      <TextField
  fullWidth
  multiline
  maxRows={6}
  placeholder="Ask AI anything..."
  value={message}
  onChange={(e) =>
    setMessage(e.target.value)
  }
  onKeyDown={(e) => {
    if (
      e.key === "Enter" &&
      !e.shiftKey
    ) {
      e.preventDefault();
      send();
    }
  }}
/>

      <Button
        variant="contained"
        onClick={send}
      >
        Send
      </Button>

    </Stack>

  );

};

export default MessageInput;