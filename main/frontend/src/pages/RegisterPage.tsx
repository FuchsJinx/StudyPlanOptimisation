import { FormEvent, useMemo, useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { IconBook, IconGrid } from "../components/Icons";
import { formatApiDetail } from "../lib/loginValidation";
import type { Role } from "../types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

const ROLE_OPTIONS: { value: Role; label: string }[] = [
  { value: "methodist", label: "Методист" },
  { value: "dispatcher", label: "Диспетчер" },
];

const LOGIN_RE = /^[a-zA-Z0-9._-]{3,50}$/;

type FieldErrors = {
  login?: string;
  fullName?: string;
  password?: string;
  passwordConfirm?: string;
  email?: string;
};

export function RegisterPage() {
  const navigate = useNavigate();
  const { isAuthenticated, loginSuccess } = useAuth();
  const [login, setLogin] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirm, setPasswordConfirm] = useState("");
  const [role, setRole] = useState<Role>("methodist");
  const [submitAttempted, setSubmitAttempted] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fieldErrors: FieldErrors = useMemo(() => {
    const errors: FieldErrors = {};
    const loginValue = login.trim();
    if (!loginValue) errors.login = "Введите логин";
    else if (!LOGIN_RE.test(loginValue)) errors.login = "Латиница, цифры, . _ - · от 3 до 50";

    if (!fullName.trim() || fullName.trim().length < 2) errors.fullName = "Укажите ФИО";

    if (!password) errors.password = "Введите пароль";
    else if (password.length < 6) errors.password = "Пароль не короче 6 символов";

    if (!passwordConfirm) errors.passwordConfirm = "Повторите пароль";
    else if (passwordConfirm !== password) errors.passwordConfirm = "Пароли не совпадают";

    if (email.trim()) {
      const parts = email.trim().split("@");
      if (parts.length !== 2 || !parts[1].includes(".")) errors.email = "Некорректный email";
    }
    return errors;
  }, [login, fullName, password, passwordConfirm, email]);

  const hasErrors = Object.keys(fieldErrors).length > 0;

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setSubmitAttempted(true);
    setFormError(null);
    if (hasErrors) {
      setFormError("Исправьте ошибки в форме");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          login: login.trim(),
          password,
          password_confirm: passwordConfirm,
          full_name: fullName.trim(),
          role,
          email: email.trim() || null,
        }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(formatApiDetail(data.detail) || `Ошибка регистрации (${res.status})`);
      }
      loginSuccess(data);
      navigate("/", { replace: true });
    } catch (err) {
      const message =
        err instanceof TypeError
          ? "Сервер недоступен. Запустите backend на порту 8000."
          : err instanceof Error
            ? err.message
            : "Не удалось зарегистрироваться";
      setFormError(message);
    } finally {
      setLoading(false);
    }
  }

  function err(key: keyof FieldErrors) {
    return submitAttempted ? fieldErrors[key] : undefined;
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
        <h1>Регистрация</h1>
        <p className="login-card-lead">Создайте учётную запись образовательной организации</p>

        <div className={`field ${err("fullName") ? "field-invalid" : ""}`}>
          <label htmlFor="full_name">ФИО</label>
          <input
            id="full_name"
            value={fullName}
            onChange={(e) => {
              setFullName(e.target.value);
              setFormError(null);
            }}
            autoComplete="name"
            autoFocus
            required
            placeholder="Иванова Мария Петровна"
          />
          {err("fullName") ? <span className="field-error">{err("fullName")}</span> : null}
        </div>

        <div className={`field ${err("login") ? "field-invalid" : ""}`}>
          <label htmlFor="reg_login">Логин</label>
          <input
            id="reg_login"
            value={login}
            onChange={(e) => {
              setLogin(e.target.value);
              setFormError(null);
            }}
            autoComplete="username"
            required
            minLength={3}
            maxLength={50}
            placeholder="m.ivanova"
          />
          {err("login") ? <span className="field-error">{err("login")}</span> : null}
        </div>

        <div className={`field ${err("email") ? "field-invalid" : ""}`}>
          <label htmlFor="email">Email (необязательно)</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              setFormError(null);
            }}
            autoComplete="email"
            placeholder="ivanova@college.ru"
          />
          {err("email") ? <span className="field-error">{err("email")}</span> : null}
        </div>

        <div className="field">
          <label htmlFor="reg_role">Роль</label>
          <select
            id="reg_role"
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

        <div className={`field ${err("password") ? "field-invalid" : ""}`}>
          <label htmlFor="reg_password">Пароль</label>
          <input
            id="reg_password"
            type="password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              setFormError(null);
            }}
            autoComplete="new-password"
            required
            minLength={6}
            placeholder="не менее 6 символов"
          />
          {err("password") ? <span className="field-error">{err("password")}</span> : null}
        </div>

        <div className={`field ${err("passwordConfirm") ? "field-invalid" : ""}`}>
          <label htmlFor="reg_password_confirm">Подтверждение пароля</label>
          <input
            id="reg_password_confirm"
            type="password"
            value={passwordConfirm}
            onChange={(e) => {
              setPasswordConfirm(e.target.value);
              setFormError(null);
            }}
            autoComplete="new-password"
            required
            minLength={6}
            placeholder="повторите пароль"
          />
          {err("passwordConfirm") ? (
            <span className="field-error">{err("passwordConfirm")}</span>
          ) : null}
        </div>

        {formError ? (
          <div className="form-alert" role="alert">
            {formError}
          </div>
        ) : null}

        <button type="submit" className="btn primary login-submit" disabled={loading}>
          {loading ? "Регистрация…" : "Зарегистрироваться"}
        </button>

        <p className="login-switch">
          Уже есть аккаунт? <Link to="/login">Войти</Link>
        </p>
      </form>

      <p className="login-footer">ГБПОУ «Технологический колледж № 1» · Версия 2.4.1</p>
    </div>
  );
}
