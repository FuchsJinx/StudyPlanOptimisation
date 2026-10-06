import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "./AuthContext";
import { hasStoredSession } from "./session";

export function RequireAuth({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  // Учитываем localStorage: сразу после loginSuccess state ещё может не обновиться
  const ok = isAuthenticated || hasStoredSession();
  if (!ok) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }
  return <>{children}</>;
}
