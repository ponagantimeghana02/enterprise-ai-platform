import {
  Box,
  Typography,
} from "@mui/material";

const EmptyState = () => {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      height={300}
    >
      <Typography color="text.secondary">
        No documents found.
      </Typography>
    </Box>
  );
};

export default EmptyState;