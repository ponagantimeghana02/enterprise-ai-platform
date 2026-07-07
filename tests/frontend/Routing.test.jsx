import { MemoryRouter } from "react-router-dom";
import { render } from "@testing-library/react";
import App from "../../frontend/src/App";

test("routing works", () => {
  render(
    <MemoryRouter>
      <App />
    </MemoryRouter>
  );
});