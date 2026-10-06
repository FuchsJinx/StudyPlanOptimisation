import { Link } from "react-router-dom";
import { IconGrid } from "../components/Icons";

export function SessionExpiredPage() {
  return (
    <div className="login-screen">
      <div className="login-brand-top">
        <span className="login-logo-mark">
          <IconGrid size={22} />
        </span>
        <h1 className="login-brand-name">Учебный контур</h1>
      </div>

      <div className="login-card session-error-card">
        <div className="session-error-code">401</div>
        <h1>Сессия недействительна</h1>
        <p className="login-card-lead">
          Токен доступа истёк или был отозван. Войдите снова, чтобы продолжить работу.
        </p>
        <Link className="btn primary login-submit" to="/login" replace>
          Вернуться ко входу
        </Link>
        <p className="login-switch" style={{ marginTop: 8 }}>
          Нет аккаунта? <Link to="/register">Зарегистрироваться</Link>
        </p>
      </div>

      <p className="login-footer">ГБПОУ «Технологический колледж № 1» · Версия 2.4.1</p>
    </div>
  );
}
