import { Box, Paper, Typography } from "@mui/material";
import MFAForm from "../../components/auth/MFAForm";

const MFAVerification = () => {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        bgcolor: "#f5f5f5",
        px: 2,
      }}
    >
      <Paper
        elevation={6}
        sx={{
          width: 500,
          p: 5,
          borderRadius: 3,
        }}
      >
        <Typography
          variant="h4"
          fontWeight="bold"
          textAlign="center"
          gutterBottom
        >
          Multi-Factor Authentication
        </Typography>

        <Typography
          textAlign="center"
          color="text.secondary"
          mb={4}
        >
          Enter the 6-digit verification code sent to your registered device.
        </Typography>

        <MFAForm />
      </Paper>
    </Box>
  );
};

export default MFAVerification;