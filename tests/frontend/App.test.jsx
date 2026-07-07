import { render, screen } from "@testing-library/react";
import App from "../../frontend/src/App";

test("renders app", () => {
  render(<App />);
  expect(screen.getByText(/app/i)).toBeInTheDocument();
});