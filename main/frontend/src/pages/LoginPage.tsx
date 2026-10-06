import { FormEvent, useMemo, useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { IconBook, IconGrid, IconInfo } from "../components/Icons";
import {
  formatApiDetail,
  hasLoginErrors,
  validateLoginFields,
  type LoginFieldErrors,
} from "../lib/loginValidation";
import type { Role } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

type Touched = { login: boolean; password: boolean };

const ROLE_OPTIONS: { value: Role; label: string }[] = [
  { value: "methodist", label: "Методист" },
  { value: "dispatcher", label: "Диспетчер" },
  { value: "admin", label: "Администратор" },
];

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, loginSuccess } = useAuth();
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<Role>("methodist");
  const [touched, setTouched] = useState<Touched>({ login: false, password: false });
  const [submitAttempted, setSubmitAttempted] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fieldErrors: LoginFieldErrors = useMemo(
    () => validateLoginFields({ login, password }),
    [login, password],
  );

  const showLoginError = (touched.login || submitAttempted) && fieldErrors.login;
  const showPasswordError = (touched.password || submitAttempted) && fieldErrors.password;
  const from = (location.state as { from?: string } | null)?.from || "/";

  if (isAuthenticated) {
    return <Navigate to={from} replace />;
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setSubmitAttempted(true);
    setFormError(null);

    const errors = validateLoginFields({ login, password });
    if (hasLoginErrors(errors)) {
      setFormError("Исправьте ошибки в форме");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ login: login.trim(), password }),
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(formatApiDetail(data.detail) || `Ошибка входа (${res.status})`);
      }

      if (data.role && data.role !== role) {
        setFormError(
          `Учётка имеет роль «${ROLE_OPTIONS.find((r) => r.value === data.role)?.label || data.role}». Выберите её в поле роли.`,
        );
        return;
      }

      loginSuccess(data);
      navigate(from, { replace: true });
    } catch (err) {
      const message =
        err instanceof TypeError
          ? "Сервер недоступен. Запустите backend на порту 8000."
          : err instanceof Error
            ? err.message
            : "Не удалось войти";
      setFormError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-screen">
      <div className="login-brand-top">
        <span className="login-logo-mark">
          <IconGrid size={22} />
        </span>
        <h1 className="login-brand-name">Учебный контур</h1>
        <p className="login-brand-tag">Информационная система планирования</p>
      </div>

      <form className="login-card" onSubmit={onSubmit} noValidate>
        <div className="login-card-icon">
          <IconBook size={22} />
        </div>
        <h1>Вход в систему</h1>
        <p className="login-card-lead">Используйте учётную запись образовательной организации</p>

        <div className={`field ${showLoginError ? "field-invalid" : ""}`}>
          <label htmlFor="login">Логин</label>
          <input
            id="login"
            name="login"
            value={login}
            onChange={(e) => {
              setLogin(e.target.value);
              setFormError(null);
            }}
            onBlur={() => setTouched((t) => ({ ...t, login: true }))}
            autoComplete="username"
            autoFocus
            required
            minLength={3}
            maxLength={50}
            placeholder="a.voronova"
          />
          {showLoginError ? (
            <span className="field-error" role="alert">
              {fieldErrors.login}
            </span>
          ) : null}
        </div>

        <div className={`field ${showPasswordError ? "field-invalid" : ""}`}>
          <label htmlFor="password">Пароль</label>
          <div className="password-wrap">
            <input
              id="password"
              name="password"
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setFormError(null);
              }}
              onBlur={() => setTouched((t) => ({ ...t, password: true }))}
              autoComplete="current-password"
              required
              minLength={6}
              maxLength={128}
              placeholder="••••••••"
            />
            <button
              type="button"
              className="password-info"
              title="Демо: Admin123!, Method123!, Dispatch123!"
              aria-label="Подсказка по паролю"
            >
              <IconInfo size={16} />
            </button>
          </div>
          {showPasswordError ? (
            <span className="field-error" role="alert">
              {fieldErrors.password}
            </span>
          ) : null}
        </div>

        <div className="field">
          <label htmlFor="role">Роль пользователя</label>
          <select
            id="role"
            value={role}
            onChange={(e) => {
              setRole(e.target.value as Role);
              setFormError(null);
            }}
          >
            {ROLE_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        {formError ? (
          <div className="form-alert" role="alert">
            {formError}
          </div>
        ) : null}

        <button type="submit" className="btn primary login-submit" disabled={loading}>
          {loading ? "Вход…" : "Войти"}
        </button>

        <p className="login-switch">
          Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
        </p>

        <button
          type="button"
          className="login-recover"
          onClick={() =>
            setFormError(
              "Восстановление пароля администратора: обратитесь в службу ИТ или используйте демо-учётку admin / Admin123!",
            )
          }
        >
          Восстановить пароль администратора
        </button>

        <p className="login-demo">
          Демо: <code>admin</code>, <code>methodist</code>, <code>dispatcher</code>
        </p>
      </form>

      <p className="login-footer">ГБПОУ «Технологический колледж № 1» · Версия 2.4.1</p>
    </div>
  );
}
