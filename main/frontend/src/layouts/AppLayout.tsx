import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { NAV_SYSTEM, NAV_WORKSPACE, canAccess, roleLabel } from "../auth/roles";
import { IconGrid, IconInfo, IconRefresh, NAV_ICON_MAP } from "../components/Icons";

function initials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
}

export function AppLayout() {
  const { session, permissions, logout } = useAuth();
  const navigate = useNavigate();

  const workspace = NAV_WORKSPACE.filter((item) => canAccess(permissions, item.permission));
  const system = NAV_SYSTEM.filter((item) => canAccess(permissions, item.permission));

  function onLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">
            <IconGrid size={18} />
          </span>
          <div>
            <div className="brand-title">Учебный контур</div>
            <div className="brand-sub">Методический центр</div>
          </div>
        </div>

        <div>
          <div className="nav-section-label">Рабочее пространство</div>
          <nav className="nav">
            {workspace.map((item) => {
              const Icon = item.icon ? NAV_ICON_MAP[item.icon] : null;
              return (
                <NavLink
                  key={`${item.to}-${item.label}`}
                  to={item.to}
                  end={item.to === "/"}
                  className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
                >
                  {Icon ? <Icon size={18} /> : null}
                  <span>{item.label}</span>
                  {item.badge ? <span className="nav-badge">{item.badge}</span> : null}
                </NavLink>
              );
            })}
          </nav>
        </div>

        <div>
          <div className="nav-section-label">Система</div>
          <nav className="nav">
            {system.map((item) => {
              const Icon = item.icon ? NAV_ICON_MAP[item.icon] : null;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
                >
                  {Icon ? <Icon size={18} /> : null}
                  <span>{item.label}</span>
                </NavLink>
              );
            })}
          </nav>
        </div>

        <div className="sidebar-footer">
          <NavLink to="/profile" className="user-chip-link">
            <span className="user-avatar">{initials(session?.fullName ?? "")}</span>
            <span className="user-meta">
              <span className="user-name">{session?.fullName ?? "—"}</span>
              <span className="user-role">{session ? roleLabel(session.role) : ""}</span>
            </span>
          </NavLink>
          <button type="button" className="btn ghost logout-btn" onClick={onLogout}>
            Выйти
          </button>
        </div>
      </aside>

      <div className="app-main">
        <header className="topbar">
          <div className="topbar-left">
            <span>2025 / 2026 учебный год</span>
            <span className="topbar-sep">|</span>
            <span>Все специальности</span>
          </div>
          <div className="topbar-right">
            <NavLink to="/profile" className="role-pill">
              {session ? roleLabel(session.role) : "—"}
            </NavLink>
            <button
              type="button"
              className="icon-btn"
              title="Обновить"
              onClick={() => window.location.reload()}
            >
              <IconRefresh />
            </button>
            <button type="button" className="icon-btn" title="Уведомления">
              <IconInfo />
              <span className="notif-dot">5</span>
            </button>
            <span className="status-ok">Данные актуальны</span>
          </div>
        </header>
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
