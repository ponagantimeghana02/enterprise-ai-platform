import {
  Box,
  Typography,
} from "@mui/material";

const EmptyState = () => {
  return (
    <Box
      height="100%"
      display="flex"
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
    >
      <Typography variant="h5">
        Welcome 👋
      </Typography>

      <Typography color="text.secondary">
        Start a new AI conversation.
      </Typography>
    </Box>
  );
};

export default EmptyState;