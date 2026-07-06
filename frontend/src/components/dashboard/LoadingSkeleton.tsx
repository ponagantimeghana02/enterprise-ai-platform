import {
  Grid,
  Skeleton,
} from "@mui/material";

const LoadingSkeleton = () => {
  return (
    <Grid container spacing={3}>
      {Array.from({ length: 8 }).map((_, index) => (
        <Grid
          item
          xs={12}
          md={3}
          key={index}
        >
          <Skeleton
            variant="rounded"
            height={120}
          />
        </Grid>
      ))}
    </Grid>
  );
};

export default LoadingSkeleton;