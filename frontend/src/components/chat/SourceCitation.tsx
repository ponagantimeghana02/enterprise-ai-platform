import {
  Chip,
  Stack,
} from "@mui/material";

interface Props {
  sources: string[];
}

const SourceCitation = ({
  sources,
}: Props) => {

  if (!sources.length) return null;

  return (
    <Stack
      direction="row"
      spacing={1}
      mt={1}
      flexWrap="wrap"
    >
      {sources.map((source) => (
        <Chip
          key={source}
          label={source}
          size="small"
        />
      ))}
    </Stack>
  );
};

export default SourceCitation;