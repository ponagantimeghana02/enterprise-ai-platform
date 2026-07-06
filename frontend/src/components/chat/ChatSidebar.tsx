import {
  Box,
  Divider,
  List,
} from "@mui/material";

import { Conversation } from "../../types/conversation";

import ConversationSearch from "./ConversationSearch";
import ConversationItem from "./ConversationItem";
import NewConversationButton from "./NewConversationButton";

interface Props {
  conversations: Conversation[];
  selectedId: string;
  search: string;
  onSearch: (value: string) => void;
  onSelect: (id: string) => void;
  onNew: () => void;
  onRename: (id: string) => void;
  onDelete: (id: string) => void;
}

const ChatSidebar = ({
  conversations,
  selectedId,
  search,
  onSearch,
  onSelect,
  onNew,
  onRename,
  onDelete,
}: Props) => {
  const filtered = conversations.filter((c) =>
    c.title
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <Box
      width={320}
      borderRight="1px solid #ddd"
      p={2}
      display="flex"
      flexDirection="column"
      gap={2}
    >
      <NewConversationButton onClick={onNew} />

      <ConversationSearch
        value={search}
        onChange={onSearch}
      />

      <Divider />

      <List>
        {filtered.map((conversation) => (
          <ConversationItem
            key={conversation.id}
            conversation={conversation}
            active={
              conversation.id === selectedId
            }
            onSelect={() =>
              onSelect(conversation.id)
            }
            onRename={() =>
              onRename(conversation.id)
            }
            onDelete={() =>
              onDelete(conversation.id)
            }
          />
        ))}
      </List>
    </Box>
  );
};

export default ChatSidebar;