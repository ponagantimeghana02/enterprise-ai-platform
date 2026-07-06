import { Box, Paper, Typography } from "@mui/material";
import LoginForm from "../../components/auth/LoginForm";

const Login = () => {
  return (
    <Box
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#f5f5f5",
        padding: 2,
      }}
    >
      <Paper
        elevation={6}
        sx={{
          width: 450,
          padding: 5,
          borderRadius: 3,
        }}
      >
        <Typography
          variant="h4"
          fontWeight="bold"
          textAlign="center"
          gutterBottom
        >
          Enterprise AI Workspace
        </Typography>

        <Typography
          color="text.secondary"
          textAlign="center"
          mb={4}
        >
          Login to continue
        </Typography>

        <LoginForm />
      </Paper>
    </Box>
  );
};

export default Login;