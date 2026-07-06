import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";

import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Stack,
  TextField,
} from "@mui/material";

import { authService } from "../../services/authService";

interface ForgotPasswordData {
  email: string;
}

const ForgotPasswordForm = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [success, setSuccess] = useState("");

  const [error, setError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordData>();

  const onSubmit = async (data: ForgotPasswordData) => {
    try {
      setLoading(true);
      setError("");
      setSuccess("");

      const response = await authService.forgotPassword(data);

      setSuccess(
        response.data?.message ||
          "Password reset link has been sent to your email."
      );
    } catch (err: any) {
      setError(
        err.response?.data?.message ||
          "Unable to process your request."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>

      <Stack spacing={3}>

        {success && (
          <Alert severity="success">
            {success}
          </Alert>
        )}

        {error && (
          <Alert severity="error">
            {error}
          </Alert>
        )}

        <TextField
          label="Email Address"
          fullWidth
          autoComplete="email"
          {...register("email", {
            required: "Email is required",

            pattern: {
              value:
                /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,

              message: "Enter a valid email address",
            },
          })}
          error={!!errors.email}
          helperText={errors.email?.message}
        />

        <Button
          type="submit"
          variant="contained"
          size="large"
          disabled={loading}
        >
          {loading ? (
            <CircularProgress
              size={24}
              color="inherit"
            />
          ) : (
            "Send Reset Link"
          )}
        </Button>

        <Box textAlign="center">

          <Button
            variant="text"
            onClick={() => navigate("/login")}
          >
            Back to Login
          </Button>

        </Box>

      </Stack>

    </form>
  );
};

export default ForgotPasswordForm;