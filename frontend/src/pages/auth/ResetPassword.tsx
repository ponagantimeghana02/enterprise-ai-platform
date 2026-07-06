import { Box, Paper, Typography } from "@mui/material";
import ResetPasswordForm from "../../components/auth/ResetPasswordForm";

const ResetPassword = () => {
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
          textAlign="center"
          fontWeight="bold"
          gutterBottom
        >
          Reset Password
        </Typography>

        <Typography
          textAlign="center"
          color="text.secondary"
          mb={4}
        >
          Create a new password for your account.
        </Typography>

        <ResetPasswordForm />
      </Paper>
    </Box>
  );
};

export default ResetPassword;