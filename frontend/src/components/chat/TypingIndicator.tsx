import {
  Box,
  CircularProgress,
  Typography,
} from "@mui/material";

const TypingIndicator = () => (
  <Box
    display="flex"
    alignItems="center"
    gap={2}
    py={2}
  >
    <CircularProgress size={18} />

    <Typography color="text.secondary">
      AI is generating response...
    </Typography>
  </Box>
);

export default TypingIndicator;