import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";

import {
  IconButton,
  ListItem,
  ListItemButton,
  ListItemText,
  Stack,
} from "@mui/material";

import { Conversation } from "../../types/conversation";

interface Props {
  conversation: Conversation;
  active: boolean;
  onSelect: () => void;
  onRename: () => void;
  onDelete: () => void;
}

const ConversationItem = ({
  conversation,
  active,
  onSelect,
  onRename,
  onDelete,
}: Props) => {
  return (
    <ListItem
      disablePadding
      secondaryAction={
        <Stack direction="row">
          <IconButton
            size="small"
            onClick={onRename}
          >
            <EditIcon fontSize="small" />
          </IconButton>

          <IconButton
            size="small"
            onClick={onDelete}
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        </Stack>
      }
    >
      <ListItemButton
        selected={active}
        onClick={onSelect}
      >
        <ListItemText
          primary={conversation.title}
          secondary={new Date(
            conversation.updatedAt
          ).toLocaleString()}
        />
      </ListItemButton>
    </ListItem>
  );
};

export default ConversationItem;