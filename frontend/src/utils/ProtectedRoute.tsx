import { Navigate, Outlet } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

const ProtectedRoute = () => {
  const auth = useAuth();

  if (!auth.authenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;