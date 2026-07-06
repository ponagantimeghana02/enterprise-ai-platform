import { CircularProgress, Box } from "@mui/material";

const Loader = () => (
  <Box
    display="flex"
    justifyContent="center"
    mt={5}
  >
    <CircularProgress />
  </Box>
);

export default Loader;