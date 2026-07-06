import VisibilityIcon from "@mui/icons-material/Visibility";
import DownloadIcon from "@mui/icons-material/Download";
import DeleteIcon from "@mui/icons-material/Delete";

import {
  IconButton,
  Stack,
  Tooltip,
} from "@mui/material";

interface Props {
  onPreview: () => void;
  onDownload: () => void;
  onDelete: () => void;
}

const DocumentActions = ({
  onPreview,
  onDownload,
  onDelete,
}: Props) => {
  return (
    <Stack direction="row" spacing={1}>
      <Tooltip title="Preview">
        <IconButton onClick={onPreview}>
          <VisibilityIcon />
        </IconButton>
      </Tooltip>

      <Tooltip title="Download">
        <IconButton onClick={onDownload}>
          <DownloadIcon />
        </IconButton>
      </Tooltip>

      <Tooltip title="Delete">
        <IconButton
          color="error"
          onClick={onDelete}
        >
          <DeleteIcon />
        </IconButton>
      </Tooltip>
    </Stack>
  );
};

export default DocumentActions;