import type { Role } from "../types";

const TOKEN_KEY = "access_token";
const ROLE_KEY = "user_role";
const NAME_KEY = "user_name";
const LOGIN_KEY = "user_login";
const PERMS_KEY = "user_permissions";
const EMAIL_KEY = "user_email";

export type SessionData = {
  accessToken: string;
  role: Role;
  fullName: string;
  login: string;
  permissions: string[];
  email?: string | null;
};

export function loadSession(): SessionData | null {
  try {
    const accessToken = localStorage.getItem(TOKEN_KEY);
    const role = localStorage.getItem(ROLE_KEY) as Role | null;
    const fullName = localStorage.getItem(NAME_KEY);
    const login = localStorage.getItem(LOGIN_KEY);
    const permissionsRaw = localStorage.getItem(PERMS_KEY);
    const email = localStorage.getItem(EMAIL_KEY);
    if (!accessToken || !role || !fullName || !login) return null;
    let permissions: string[] = [];
    try {
      permissions = permissionsRaw ? (JSON.parse(permissionsRaw) as string[]) : [];
    } catch {
      permissions = [];
    }
    return {
      accessToken,
      role,
      fullName,
      login,
      permissions,
      email: email || null,
    };
  } catch {
    return null;
  }
}

export function saveSession(data: SessionData): void {
  localStorage.setItem(TOKEN_KEY, data.accessToken);
  localStorage.setItem(ROLE_KEY, data.role);
  localStorage.setItem(NAME_KEY, data.fullName);
  localStorage.setItem(LOGIN_KEY, data.login);
  localStorage.setItem(PERMS_KEY, JSON.stringify(data.permissions ?? []));
  if (data.email) localStorage.setItem(EMAIL_KEY, data.email);
  else localStorage.removeItem(EMAIL_KEY);
}

export function clearSession(): void {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(ROLE_KEY);
  localStorage.removeItem(NAME_KEY);
  localStorage.removeItem(LOGIN_KEY);
  localStorage.removeItem(PERMS_KEY);
  localStorage.removeItem(EMAIL_KEY);
}

export function hasStoredSession(): boolean {
  return Boolean(localStorage.getItem(TOKEN_KEY));
}

export function authHeaders(): HeadersInit {
  const token = localStorage.getItem(TOKEN_KEY);
  return token ? { Authorization: `Bearer ${token}` } : {};
}
