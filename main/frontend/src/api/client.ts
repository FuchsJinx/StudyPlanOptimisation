import { authHeaders, clearSession } from "../auth/session";

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

type UnauthorizedHandler = () => void;
let unauthorizedHandler: UnauthorizedHandler | null = null;

export function setUnauthorizedHandler(handler: UnauthorizedHandler | null): void {
  unauthorizedHandler = handler;
}

async function parseError(res: Response, path: string): Promise<never> {
  let detail = `API ${res.status}: ${path}`;
  try {
    const data = await res.json();
    if (typeof data?.detail === "string") detail = data.detail;
    else if (Array.isArray(data?.detail)) {
      detail = data.detail.map((x: { msg?: string }) => x.msg || String(x)).join("; ");
    }
  } catch {
    /* keep default */
  }
  if (res.status === 401) {
    clearSession();
    unauthorizedHandler?.();
  }
  throw new ApiError(res.status, detail);
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { ...authHeaders() },
  });
  if (!res.ok) await parseError(res, path);
  return res.json() as Promise<T>;
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) await parseError(res, path);
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export async function apiPatch<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) await parseError(res, path);
  return res.json() as Promise<T>;
}

export async function apiDelete(path: string): Promise<void> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "DELETE",
    headers: { ...authHeaders() },
  });
  if (!res.ok) await parseError(res, path);
}

export type HealthResponse = {
  status: string;
  app: string;
  version: string;
  env: string;
};

export type Plan = {
  id: number;
  code?: string | null;
  title: string;
  study_year: number;
  education_form: string;
  import_status: string;
};

export type DirectorySummary = {
  groups: number;
  teachers: number;
  classrooms: number;
  subjects: number;
  specialties: number;
  lesson_types: number;
};

export type Specialty = {
  id: number;
  code: string;
  title: string;
  is_active: boolean;
};

export type LessonType = {
  id: number;
  code: string;
  title: string;
  is_active: boolean;
};

export type StudyGroup = {
  id: number;
  code: string;
  size: number | null;
  education_form: string;
  specialty_code: string | null;
  study_year: number | null;
  is_active: boolean;
};

export type Teacher = {
  id: number;
  full_name: string;
  rate: number | null;
  budget_flag: boolean;
  contacts: string | null;
  is_active: boolean;
};

export type Classroom = {
  id: number;
  code: string;
  capacity: number | null;
  building: string | null;
  room_type: string | null;
  is_active: boolean;
};

export type Subject = {
  id: number;
  code: string;
  title: string;
  short_title: string | null;
  cycle: string | null;
  is_active: boolean;
};
