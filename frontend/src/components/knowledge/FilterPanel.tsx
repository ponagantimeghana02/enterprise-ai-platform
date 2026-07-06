import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from "@mui/material";

interface Props {
  status: string;
  onChange: (value: string) => void;
}

const FilterPanel = ({ status, onChange }: Props) => {
  return (
    <FormControl fullWidth>
      <InputLabel>Status</InputLabel>

      <Select
        value={status}
        label="Status"
        onChange={(e) => onChange(e.target.value)}
      >
        <MenuItem value="">All</MenuItem>
        <MenuItem value="Pending">Pending</MenuItem>
        <MenuItem value="Approved">Approved</MenuItem>
        <MenuItem value="Rejected">Rejected</MenuItem>
      </Select>
    </FormControl>
  );
};

export default FilterPanel;