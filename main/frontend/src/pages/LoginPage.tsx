import { FormEvent, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  formatApiDetail,
  hasLoginErrors,
  validateLoginFields,
  type LoginFieldErrors,
} from "../lib/loginValidation";

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

type Touched = { login: boolean; password: boolean };

export function LoginPage() {
  const navigate = useNavigate();
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
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

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user_role", data.role);
      localStorage.setItem("user_name", data.full_name);
      localStorage.setItem("user_login", data.login);
      navigate("/", { replace: true });
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
      <form className="login-card" onSubmit={onSubmit} noValidate>
        <div className="login-brand">
          <span className="brand-mark">УП</span>
          <div>
            <h1>Вход в систему</h1>
            <p className="muted">Учебные планы · нагрузка · расписание</p>
          </div>
        </div>

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
            aria-invalid={Boolean(showLoginError)}
            aria-describedby={showLoginError ? "login-error" : "login-hint"}
            placeholder="например, methodist"
          />
          {showLoginError ? (
            <span id="login-error" className="field-error" role="alert">
              {fieldErrors.login}
            </span>
          ) : (
            <span id="login-hint" className="field-hint">
              Латиница, цифры, . _ - · от 3 до 50 символов
            </span>
          )}
        </div>

        <div className={`field ${showPasswordError ? "field-invalid" : ""}`}>
          <label htmlFor="password">Пароль</label>
          <div className="password-row">
            <input
              id="password"
              name="password"
              type={showPassword ? "text" : "password"}
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
              aria-invalid={Boolean(showPasswordError)}
              aria-describedby={showPasswordError ? "password-error" : "password-hint"}
              placeholder="не менее 6 символов"
            />
            <button
              type="button"
              className="btn ghost password-toggle"
              onClick={() => setShowPassword((v) => !v)}
              aria-label={showPassword ? "Скрыть пароль" : "Показать пароль"}
            >
              {showPassword ? "Скрыть" : "Показать"}
            </button>
          </div>
          {showPasswordError ? (
            <span id="password-error" className="field-error" role="alert">
              {fieldErrors.password}
            </span>
          ) : (
            <span id="password-hint" className="field-hint">
              Минимум 6 символов
            </span>
          )}
        </div>

        {formError ? (
          <div className="form-alert" role="alert">
            {formError}
          </div>
        ) : null}

        <button type="submit" className="btn primary login-submit" disabled={loading}>
          {loading ? "Вход…" : "Войти"}
        </button>

        <p className="muted login-demo">
          Демо-учётки: <code>admin / Admin123!</code>, <code>methodist / Method123!</code>,{" "}
          <code>dispatcher / Dispatch123!</code>
        </p>
      </form>
    </div>
  );
}
