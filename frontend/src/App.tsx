import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/auth/Login";

import ProtectedRoute from "./utils/ProtectedRoute";
import ForgotPassword from "./pages/auth/ForgotPassword";
import ResetPassword from "./pages/auth/ResetPassword";
import MFAVerification from "./pages/auth/MFAVerification";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
        <Route
        path="/forgot-password"
        element={<ForgotPassword />}
    />

<Route
  path="/reset-password"
  element={<ResetPassword />}
/>

<Route
  path="/mfa"
  element={<MFAVerification />}
/>

          <Route
            path="/dashboard"
            element={<h1>Dashboard</h1>}
          />

        </Route>

      </Routes>

    </BrowserRouter>
  );
}

export default App;