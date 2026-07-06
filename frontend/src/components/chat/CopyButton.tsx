import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import { IconButton, Tooltip } from "@mui/material";
import toast from "react-hot-toast";

interface Props {
  text: string;
}

const CopyButton = ({ text }: Props) => {
  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    toast.success("Copied to clipboard");
  };

  return (
    <Tooltip title="Copy">
      <IconButton size="small" onClick={handleCopy}>
        <ContentCopyIcon fontSize="small" />
      </IconButton>
    </Tooltip>
  );
};

export default CopyButton;