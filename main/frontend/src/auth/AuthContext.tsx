import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useNavigate } from "react-router-dom";
import { setUnauthorizedHandler } from "../api/client";
import type { Role } from "../types";
import { permissionsForRole } from "./roles";
import {
  authHeaders,
  clearSession,
  hasStoredSession,
  loadSession,
  saveSession,
  type SessionData,
} from "./session";

type LoginPayload = {
  access_token: string;
  role: string;
  full_name: string;
  login: string;
  permissions?: string[];
  email?: string | null;
};

type AuthContextValue = {
  session: SessionData | null;
  isAuthenticated: boolean;
  permissions: string[];
  loginSuccess: (data: LoginPayload) => void;
  logout: () => void;
  refreshProfile: (patch: Partial<SessionData>) => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);
const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

export function AuthProvider({ children }: { children: ReactNode }) {
  const navigate = useNavigate();
  const [session, setSession] = useState<SessionData | null>(() => loadSession());

  const loginSuccess = useCallback((data: LoginPayload) => {
    const role = data.role as Role;
    const next: SessionData = {
      accessToken: data.access_token,
      role,
      fullName: data.full_name,
      login: data.login,
      permissions: permissionsForRole(role, data.permissions),
      email: data.email ?? null,
    };
    saveSession(next);
    setSession(next);
  }, []);

  const logout = useCallback(() => {
    const headers = { ...authHeaders() };
    clearSession();
    setSession(null);
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), 2500);
    void fetch(`${API_BASE}/auth/logout`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...headers,
      },
      signal: controller.signal,
    }).catch(() => undefined).finally(() => window.clearTimeout(timer));
  }, []);

  const refreshProfile = useCallback((patch: Partial<SessionData>) => {
    setSession((prev) => {
      if (!prev) return prev;
      const next = { ...prev, ...patch };
      saveSession(next);
      return next;
    });
  }, []);

  useEffect(() => {
    setUnauthorizedHandler(() => {
      clearSession();
      setSession(null);
      navigate("/session-expired", { replace: true });
    });
    return () => setUnauthorizedHandler(null);
  }, [navigate]);

  // Подтягиваем актуальные права с сервера (после обновления ролей)
  useEffect(() => {
    if (!hasStoredSession()) return;
    let cancelled = false;
    void fetch(`${API_BASE}/auth/session`, { headers: { ...authHeaders() } })
      .then(async (res) => {
        if (res.status === 401) {
          clearSession();
          if (!cancelled) {
            setSession(null);
            navigate("/session-expired", { replace: true });
          }
          return null;
        }
        if (!res.ok) return null;
        return res.json() as Promise<{
          role?: string;
          full_name?: string;
          login?: string;
          permissions?: string[];
        }>;
      })
      .then((data) => {
        if (cancelled || !data) return;
        setSession((prev) => {
          const base = prev ?? loadSession();
          if (!base) return prev;
          const role = (data.role as Role) || base.role;
          const next: SessionData = {
            ...base,
            role,
            fullName: data.full_name || base.fullName,
            login: data.login || base.login,
            permissions: permissionsForRole(role, data.permissions),
          };
          saveSession(next);
          return next;
        });
      })
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [navigate]);

  const value = useMemo<AuthContextValue>(() => {
    const effective = session ?? (hasStoredSession() ? loadSession() : null);
    return {
      session: effective,
      isAuthenticated: Boolean(effective?.accessToken),
      permissions: effective
        ? permissionsForRole(effective.role, effective.permissions)
        : [],
      loginSuccess,
      logout,
      refreshProfile,
    };
  }, [session, loginSuccess, logout, refreshProfile]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth должен использоваться внутри AuthProvider");
  return ctx;
}
