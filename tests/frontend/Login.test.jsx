import { render, screen } from "@testing-library/react";
import Login from "../../frontend/src/pages/auth/Login";

test("login page loads", () => {
  render(<Login />);
  expect(screen.getByText(/login/i)).toBeInTheDocument();
});