import {
  Dialog,
  DialogTitle,
  DialogContent,
  Typography,
} from "@mui/material";

interface Props {
  open: boolean;
  title: string;
  content: string;
  onClose: () => void;
}

const PreviewDialog = ({
  open,
  title,
  content,
  onClose,
}: Props) => {
  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
    >
      <DialogTitle>{title}</DialogTitle>

      <DialogContent>
        <Typography
          whiteSpace="pre-wrap"
        >
          {content}
        </Typography>
      </DialogContent>
    </Dialog>
  );
};

export default PreviewDialog;