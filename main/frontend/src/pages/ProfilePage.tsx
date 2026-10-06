import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { authHeaders } from "../auth/session";
import { roleLabel } from "../auth/roles";
import { PageHeader } from "../components/PageHeader";
import { formatApiDetail } from "../lib/loginValidation";

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

type MeResponse = {
  id: number;
  login: string;
  full_name: string;
  role: string;
  email?: string | null;
  is_active: boolean;
};

function initials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
}

export function ProfilePage() {
  const navigate = useNavigate();
  const { session, logout, refreshProfile } = useAuth();
  const [me, setMe] = useState<MeResponse | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [pwdError, setPwdError] = useState<string | null>(null);
  const [pwdOk, setPwdOk] = useState<string | null>(null);
  const [pwdLoading, setPwdLoading] = useState(false);

  useEffect(() => {
    let cancelled = false;
    fetch(`${API_BASE}/auth/me`, { headers: { ...authHeaders() } })
      .then(async (res) => {
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(formatApiDetail(data.detail) || `Ошибка ${res.status}`);
        return data as MeResponse;
      })
      .then((data) => {
        if (cancelled) return;
        setMe(data);
        refreshProfile({
          fullName: data.full_name,
          email: data.email ?? null,
          login: data.login,
        });
      })
      .catch((err: Error) => {
        if (!cancelled) setLoadError(err.message);
      });
    return () => {
      cancelled = true;
    };
  }, [refreshProfile]);

  async function onChangePassword(e: FormEvent) {
    e.preventDefault();
    setPwdError(null);
    setPwdOk(null);
    if (newPassword.length < 6) {
      setPwdError("Новый пароль не короче 6 символов");
      return;
    }
    if (newPassword !== confirmPassword) {
      setPwdError("Пароли не совпадают");
      return;
    }
    setPwdLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/change-password`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeaders(),
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(formatApiDetail(data.detail) || `Ошибка ${res.status}`);
      }
      setPwdOk("Пароль обновлён. Выполните вход снова.");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      window.setTimeout(() => {
        logout();
        navigate("/login", { replace: true });
      }, 1200);
    } catch (err) {
      setPwdError(err instanceof Error ? err.message : "Не удалось сменить пароль");
    } finally {
      setPwdLoading(false);
    }
  }

  const name = me?.full_name || session?.fullName || "—";
  const role = (me?.role || session?.role || "methodist") as "admin" | "methodist" | "dispatcher";
  const login = me?.login || session?.login || "—";
  const email = me?.email || session?.email || "не указан";

  return (
    <section className="profile-page">
      <PageHeader title="Профиль" subtitle="Личные данные и безопасность учётной записи" />

      {loadError ? <div className="form-alert">{loadError}</div> : null}

      <div className="profile-hero card">
        <div className="profile-avatar-lg">{initials(name)}</div>
        <div>
          <h2 style={{ marginBottom: 4 }}>{name}</h2>
          <p className="muted">{roleLabel(role)}</p>
        </div>
      </div>

      <div className="grid-2" style={{ marginTop: 16 }}>
        <div className="card">
          <h2>Учётная запись</h2>
          <dl className="profile-dl">
            <div>
              <dt>Логин</dt>
              <dd>{login}</dd>
            </div>
            <div>
              <dt>ФИО</dt>
              <dd>{name}</dd>
            </div>
            <div>
              <dt>Роль</dt>
              <dd>{roleLabel(role)}</dd>
            </div>
            <div>
              <dt>Email</dt>
              <dd>{email}</dd>
            </div>
            <div>
              <dt>Статус</dt>
              <dd>{me?.is_active === false ? "Отключён" : "Активен"}</dd>
            </div>
          </dl>
        </div>

        <div className="card">
          <h2>Смена пароля</h2>
          <form className="profile-form" onSubmit={onChangePassword}>
            <label className="field">
              <span>Текущий пароль</span>
              <input
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                autoComplete="current-password"
                required
              />
            </label>
            <label className="field">
              <span>Новый пароль</span>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                autoComplete="new-password"
                minLength={6}
                required
              />
            </label>
            <label className="field">
              <span>Подтверждение</span>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                autoComplete="new-password"
                minLength={6}
                required
              />
            </label>
            {pwdError ? <div className="form-alert">{pwdError}</div> : null}
            {pwdOk ? <p className="ok-text">{pwdOk}</p> : null}
            <button type="submit" className="btn primary" disabled={pwdLoading}>
              {pwdLoading ? "Сохранение…" : "Обновить пароль"}
            </button>
          </form>
        </div>
      </div>
    </section>
  );
}
