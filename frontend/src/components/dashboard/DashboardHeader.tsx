import {
  Box,
  Typography,
} from "@mui/material";

const DashboardHeader = () => {
  return (
    <Box mb={4}>
      <Typography
        variant="h4"
        fontWeight="bold"
      >
        Enterprise Dashboard
      </Typography>

      <Typography color="text.secondary">
        AI Workspace Overview
      </Typography>
    </Box>
  );
};

export default DashboardHeader;