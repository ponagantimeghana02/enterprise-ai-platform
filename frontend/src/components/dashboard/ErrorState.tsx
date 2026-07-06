import {
  Alert,
  Button,
  Stack,
} from "@mui/material";

interface Props {
  retry: () => void;
}

const ErrorState = ({ retry }: Props) => {
  return (
    <Stack spacing={2}>
      <Alert severity="error">
        Failed to load dashboard.
      </Alert>

      <Button
        variant="contained"
        onClick={retry}
      >
        Retry
      </Button>
    </Stack>
  );
};

export default ErrorState;