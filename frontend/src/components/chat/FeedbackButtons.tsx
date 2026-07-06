import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";

import {
  IconButton,
  Stack,
  Tooltip,
} from "@mui/material";

interface Props {
  messageId: string;
}

const FeedbackButtons = ({ messageId }: Props) => {

  const submitFeedback = (
    feedback: "like" | "dislike"
  ) => {
    console.log(messageId, feedback);

    // Future API:
    // POST /chat/feedback
  };

  return (
    <Stack direction="row">

      <Tooltip title="Helpful">
        <IconButton
          onClick={() =>
            submitFeedback("like")
          }
        >
          <ThumbUpIcon fontSize="small"/>
        </IconButton>
      </Tooltip>

      <Tooltip title="Not Helpful">
        <IconButton
          onClick={() =>
            submitFeedback("dislike")
          }
        >
          <ThumbDownIcon fontSize="small"/>
        </IconButton>
      </Tooltip>

    </Stack>
  );
};

export default FeedbackButtons;