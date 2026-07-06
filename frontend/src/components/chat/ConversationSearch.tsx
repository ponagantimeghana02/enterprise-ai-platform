import {
  TextField,
} from "@mui/material";

interface Props {
  value: string;
  onChange: (value: string) => void;
}

const ConversationSearch = ({
  value,
  onChange,
}: Props) => {
  return (
    <TextField
      fullWidth
      size="small"
      placeholder="Search conversations..."
      value={value}
      onChange={(e) =>
        onChange(e.target.value)
      }
    />
  );
};

export default ConversationSearch;