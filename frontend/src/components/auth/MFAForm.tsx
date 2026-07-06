import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "../../services/authService";

const OTP_LENGTH = 6;

const MFAForm = () => {
  const navigate = useNavigate();

  const [otp, setOtp] = useState(Array(OTP_LENGTH).fill(""));
  const [loading, setLoading] = useState(false);
  const [seconds, setSeconds] = useState(60);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const inputs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    if (seconds <= 0) return;

    const timer = setInterval(() => {
      setSeconds((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [seconds]);

  const handleChange = (
    value: string,
    index: number
  ) => {
    if (!/^\d?$/.test(value)) return;

    const copy = [...otp];
    copy[index] = value;
    setOtp(copy);

    if (value && index < OTP_LENGTH - 1) {
      inputs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (
    e: React.KeyboardEvent<HTMLInputElement>,
    index: number
  ) => {
    if (
      e.key === "Backspace" &&
      !otp[index] &&
      index > 0
    ) {
      inputs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (
    e: React.ClipboardEvent<HTMLInputElement>
  ) => {
    e.preventDefault();

    const pasted = e.clipboardData
      .getData("text")
      .replace(/\D/g, "")
      .slice(0, OTP_LENGTH);

    if (!pasted) return;

    const values = pasted.split("");

    const updated = [...otp];

    values.forEach((digit, idx) => {
      updated[idx] = digit;
    });

    setOtp(updated);

    inputs.current[
      Math.min(values.length, OTP_LENGTH) - 1
    ]?.focus();
  };

  const verifyOTP = async () => {
    const code = otp.join("");

    if (code.length !== OTP_LENGTH) {
      setError("Please enter all six digits.");
      return;
    }

    try {
      setLoading(true);
      setError("");
      setSuccess("");

      const response = await authService.verifyMFA({
        code,
      });

      setSuccess(
        response.data?.message ||
          "Verification successful."
      );

      setTimeout(() => {
        navigate("/dashboard");
      }, 1500);

    } catch (err: any) {
      setError(
        err.response?.data?.message ||
          "Invalid verification code."
      );
    } finally {
      setLoading(false);
    }
  };

  const resendCode = async () => {
    // Replace with your resend endpoint when available
    setSeconds(60);
    setOtp(Array(OTP_LENGTH).fill(""));
    inputs.current[0]?.focus();
  };

  return (
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

      <Box
        display="flex"
        justifyContent="space-between"
        gap={1}
      >
        {otp.map((digit, index) => (
          <TextField
            key={index}
            value={digit}
            inputRef={(el) => {
              inputs.current[index] = el;
            }}
            onChange={(e) =>
              handleChange(e.target.value, index)
            }
            onKeyDown={(e) =>
              handleKeyDown(e, index)
            }
            onPaste={handlePaste}
            inputProps={{
              maxLength: 1,
              style: {
                textAlign: "center",
                fontSize: "24px",
                fontWeight: "bold",
              },
            }}
            sx={{ width: 55 }}
          />
        ))}
      </Box>

      <Button
        variant="contained"
        size="large"
        onClick={verifyOTP}
        disabled={loading}
      >
        {loading ? (
          <CircularProgress
            size={24}
            color="inherit"
          />
        ) : (
          "Verify"
        )}
      </Button>

      <Typography textAlign="center">
        {seconds > 0
          ? `Resend code in ${seconds}s`
          : "Didn't receive the code?"}
      </Typography>

      <Button
        disabled={seconds > 0}
        onClick={resendCode}
      >
        Resend Code
      </Button>

    </Stack>
  );
};

export default MFAForm;