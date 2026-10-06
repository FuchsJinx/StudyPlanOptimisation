import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import { canAccess } from "./roles";

export function RequirePermission({
  permission,
  children,
}: {
  permission: string;
  children: React.ReactNode;
}) {
  const { permissions } = useAuth();
  if (!canAccess(permissions, permission)) {
    return <Navigate to="/" replace />;
  }
  return <>{children}</>;
}
