import {
  Card,
  CardContent,
  Typography,
} from "@mui/material";

interface Props {
  title: string;
  value: string | number;
  color?: string;
}

const StatsCard = ({
  title,
  value,
  color = "#1976d2",
}: Props) => {
  return (
    <Card elevation={3}>
      <CardContent>
        <Typography
          variant="body2"
          color="text.secondary"
        >
          {title}
        </Typography>

        <Typography
          variant="h4"
          fontWeight="bold"
          sx={{ color }}
        >
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default StatsCard;