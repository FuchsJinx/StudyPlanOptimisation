const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${path}`);
  }
  return res.json() as Promise<T>;
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
