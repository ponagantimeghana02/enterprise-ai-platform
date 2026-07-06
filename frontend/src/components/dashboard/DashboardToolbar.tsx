import {
  Box,
  Button,
  MenuItem,
  Select,
  Typography,
} from "@mui/material";

interface Props {
  filter: string;
  loading: boolean;
  lastUpdated: string;
  onFilterChange: (value: string) => void;
  onRefresh: () => void;
}

const DashboardToolbar = ({
  filter,
  loading,
  lastUpdated,
  onFilterChange,
  onRefresh,
}: Props) => {
  return (
    <Box
      display="flex"
      justifyContent="space-between"
      alignItems="center"
      mb={3}
      flexWrap="wrap"
      gap={2}
    >
      <Box>
        <Typography variant="body2" color="text.secondary">
          Last Updated
        </Typography>

        <Typography fontWeight="bold">
          {lastUpdated}
        </Typography>
      </Box>

      <Box display="flex" gap={2}>
        <Select
          size="small"
          value={filter}
          onChange={(e) =>
            onFilterChange(e.target.value)
          }
        >
          <MenuItem value="today">Today</MenuItem>
          <MenuItem value="week">This Week</MenuItem>
          <MenuItem value="month">This Month</MenuItem>
        </Select>

        <Button
          variant="contained"
          onClick={onRefresh}
          disabled={loading}
        >
          Refresh
        </Button>
      </Box>
    </Box>
  );
};

export default DashboardToolbar;