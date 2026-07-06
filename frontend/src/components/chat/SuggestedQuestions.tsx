import {
  Button,
  Stack,
} from "@mui/material";

const questions = [
  "Summarize today's reports",
  "Explain company leave policy",
  "Generate project status",
  "Find payroll document",
];

interface Props {
  onSelect: (
    question: string
  ) => void;
}

const SuggestedQuestions = ({
  onSelect,
}: Props) => {
  return (
    <Stack
      spacing={2}
      mt={3}
    >
      {questions.map((q) => (
        <Button
          key={q}
          variant="outlined"
          onClick={() =>
            onSelect(q)
          }
        >
          {q}
        </Button>
      ))}
    </Stack>
  );
};

export default SuggestedQuestions;