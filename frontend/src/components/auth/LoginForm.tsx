import {
  Button,
  Checkbox,
  CircularProgress,
  FormControlLabel,
  IconButton,
  InputAdornment,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import {
  Visibility,
  VisibilityOff,
} from "@mui/icons-material";

import { useForm } from "react-hook-form";

import { useState, useEffect } from "react";

import { useNavigate } from "react-router-dom";

import { useAppDispatch, useAuth } from "../../hooks/useAuth";

import { loginUser, clearError } from "../../store/authSlice";

interface LoginData {
  email: string;
  password: string;
}

const LoginForm = () => {
  const dispatch = useAppDispatch();

  const navigate = useNavigate();

  const auth = useAuth();

  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginData>();

  useEffect(() => {
    if (auth.authenticated) {
      navigate("/dashboard");
    }
  }, [auth.authenticated]);

  useEffect(() => {
    return () => {
      dispatch(clearError());
    };
  }, []);

  const onSubmit = (data: LoginData) => {
    dispatch(loginUser(data));
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>

      <Stack spacing={3}>

        <TextField
          label="Email"
          fullWidth
          {...register("email", {
            required: "Email is required",
            pattern: {
              value:
                /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: "Invalid Email",
            },
          })}
          error={!!errors.email}
          helperText={errors.email?.message}
        />

        <TextField
          type={showPassword ? "text" : "password"}
          label="Password"
          fullWidth
          {...register("password", {
            required: "Password is required",
            minLength: {
              value: 6,
              message: "Minimum 6 characters",
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

        <FormControlLabel
          control={<Checkbox />}
          label="Remember Me"
        />

        {auth.error && (
          <Typography color="error">
            {auth.error}
          </Typography>
        )}

        <Button
          type="submit"
          variant="contained"
          size="large"
          disabled={auth.loading}
        >
          {auth.loading ? (
            <CircularProgress size={25} color="inherit" />
          ) : (
            "Login"
          )}
        </Button>

        <Button
          onClick={() =>
            navigate("/forgot-password")
          }
        >
          Forgot Password?
        </Button>

      </Stack>

    </form>
  );
};

export default LoginForm;