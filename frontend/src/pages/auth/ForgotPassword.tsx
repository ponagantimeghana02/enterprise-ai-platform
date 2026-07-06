import { Box, Paper, Typography } from "@mui/material";
import ForgotPasswordForm from "../../components/auth/ForgotPasswordForm";

const ForgotPassword = () => {
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
          width: 450,
          p: 5,
          borderRadius: 3,
        }}
      >
        <Typography
          variant="h4"
          textAlign="center"
          fontWeight="bold"
          gutterBottom
        >
          Forgot Password
        </Typography>

        <Typography
          textAlign="center"
          color="text.secondary"
          mb={4}
        >
          Enter your registered email address. We'll send you a password reset
          link.
        </Typography>

        <ForgotPasswordForm />
      </Paper>
    </Box>
  );
};

export default ForgotPassword;