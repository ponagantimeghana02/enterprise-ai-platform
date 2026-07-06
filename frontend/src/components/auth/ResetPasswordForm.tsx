import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { useForm } from "react-hook-form";

import {
  Alert,
  Box,
  Button,
  CircularProgress,
  IconButton,
  InputAdornment,
  Stack,
  TextField,
} from "@mui/material";

import {
  Visibility,
  VisibilityOff,
} from "@mui/icons-material";

import { authService } from "../../services/authService";

interface ResetPasswordData {
  password: string;
  confirmPassword: string;
}

const ResetPasswordForm = () => {
  const navigate = useNavigate();

  const [params] = useSearchParams();

  const token = params.get("token") || "";

  const [loading, setLoading] = useState(false);

  const [success, setSuccess] = useState("");

  const [error, setError] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ResetPasswordData>();

  const password = watch("password");

  const onSubmit = async (data: ResetPasswordData) => {
    try {
      setLoading(true);
      setSuccess("");
      setError("");

      const response = await authService.resetPassword({
        token,
        password: data.password,
      });

      setSuccess(
        response.data?.message ||
          "Password reset successful."
      );

      setTimeout(() => {
        navigate("/login");
      }, 2000);

    } catch (err: any) {
      setError(
        err.response?.data?.message ||
          "Unable to reset password."
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
          label="New Password"
          type={showPassword ? "text" : "password"}
          fullWidth
          {...register("password", {
            required: "Password is required",

            minLength: {
              value: 8,
              message: "Minimum 8 characters",
            },

            pattern: {
              value:
                /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/,
              message:
                "Must contain uppercase, lowercase and number",
            },
          })}
          error={!!errors.password}
          helperText={errors.password?.message}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                >
                  {showPassword ? (
                    <VisibilityOff />
                  ) : (
                    <Visibility />
                  )}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        <TextField
          label="Confirm Password"
          type={
            showConfirmPassword ? "text" : "password"
          }
          fullWidth
          {...register("confirmPassword", {
            required: "Confirm your password",

            validate: (value) =>
              value === password ||
              "Passwords do not match",
          })}
          error={!!errors.confirmPassword}
          helperText={
            errors.confirmPassword?.message
          }
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={() =>
                    setShowConfirmPassword(
                      !showConfirmPassword
                    )
                  }
                >
                  {showConfirmPassword ? (
                    <VisibilityOff />
                  ) : (
                    <Visibility />
                  )}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        <Button
          variant="contained"
          type="submit"
          size="large"
          disabled={loading}
        >
          {loading ? (
            <CircularProgress
              size={24}
              color="inherit"
            />
          ) : (
            "Reset Password"
          )}
        </Button>

        <Box textAlign="center">
          <Button
            onClick={() => navigate("/login")}
          >
            Back to Login
          </Button>
        </Box>

      </Stack>

    </form>
  );
};

export default ResetPasswordForm;