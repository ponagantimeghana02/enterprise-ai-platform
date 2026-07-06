import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

interface Props {
  language: string;
  value: string;
}

const CodeBlock = ({ language, value }: Props) => {
  return (
    <SyntaxHighlighter
      language={language}
      style={oneDark}
      customStyle={{
        borderRadius: 8,
        marginTop: 12,
      }}
    >
      {value}
    </SyntaxHighlighter>
  );
};

export default CodeBlock;