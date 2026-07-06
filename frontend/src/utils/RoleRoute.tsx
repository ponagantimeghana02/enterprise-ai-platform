import {
  Navigate,
  Outlet,
} from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

interface Props {
  roles: string[];
}

const RoleRoute = ({
  roles,
}: Props) => {
  const auth = useAuth();

  if (!auth.authenticated)
    return <Navigate to="/login" />;

  if (!roles.includes(auth.user?.role || "")) {
    return <Navigate to="/unauthorized" />;
  }

  return <Outlet />;
};

export default RoleRoute;