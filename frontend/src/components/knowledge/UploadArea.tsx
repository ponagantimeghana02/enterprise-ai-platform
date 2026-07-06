import { Paper, Typography } from "@mui/material";

interface Props {
  onUpload: (file: File) => void;
}

const UploadArea = ({ onUpload }: Props) => {
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();

    const file = e.dataTransfer.files[0];

    if (file) {
      onUpload(file);
    }
  };

  return (
    <Paper
      sx={{
        p: 4,
        textAlign: "center",
        border: "2px dashed gray",
        cursor: "pointer",
      }}
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      <Typography variant="h6">
        Drag & Drop File Here
      </Typography>

      <Typography>
        or Click Upload Button
      </Typography>

      <input
        type="file"
        onChange={(e) => {
          const file = e.target.files?.[0];

          if (file) onUpload(file);
        }}
      />
    </Paper>
  );
};

export default UploadArea;