import AddIcon from "@mui/icons-material/Add";

import {
  Button,
} from "@mui/material";

interface Props {
  onClick: () => void;
}

const NewConversationButton = ({
  onClick,
}: Props) => (
  <Button
    fullWidth
    variant="contained"
    startIcon={<AddIcon />}
    onClick={onClick}
  >
    New Chat
  </Button>
);

export default NewConversationButton;