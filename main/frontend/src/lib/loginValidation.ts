export type LoginFields = {
  login: string;
  password: string;
};

export type LoginFieldErrors = {
  login?: string;
  password?: string;
};

const LOGIN_RE = /^[a-zA-Z0-9._-]{3,50}$/;

export function validateLoginFields(values: LoginFields): LoginFieldErrors {
  const errors: LoginFieldErrors = {};
  const login = values.login.trim();
  const password = values.password;

  if (!login) {
    errors.login = "Введите логин";
  } else if (login.length < 3) {
    errors.login = "Логин не короче 3 символов";
  } else if (login.length > 50) {
    errors.login = "Логин не длиннее 50 символов";
  } else if (!LOGIN_RE.test(login)) {
    errors.login = "Допустимы латиница, цифры, точка, _ и -";
  }

  if (!password) {
    errors.password = "Введите пароль";
  } else if (password.length < 6) {
    errors.password = "Пароль не короче 6 символов";
  } else if (password.length > 128) {
    errors.password = "Пароль слишком длинный";
  }

  return errors;
}

export function hasLoginErrors(errors: LoginFieldErrors): boolean {
  return Boolean(errors.login || errors.password);
}

export function formatApiDetail(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (item && typeof item === "object" && "msg" in item) {
          const loc = Array.isArray((item as { loc?: unknown }).loc)
            ? (item as { loc: unknown[] }).loc.slice(1).join(".")
            : "";
          const msg = String((item as { msg: unknown }).msg);
          return loc ? `${loc}: ${msg}` : msg;
        }
        return String(item);
      })
      .join("; ");
  }
  if (detail == null) return "Не удалось войти";
  return String(detail);
}
