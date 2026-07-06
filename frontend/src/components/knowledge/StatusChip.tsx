import { Chip } from "@mui/material";

interface Props {
  status: "Pending" | "Approved" | "Rejected";
}

const StatusChip = ({ status }: Props) => {
  const color =
    status === "Approved"
      ? "success"
      : status === "Rejected"
      ? "error"
      : "warning";

  return (
    <Chip
      label={status}
      color={color}
      size="small"
    />
  );
};

export default StatusChip;