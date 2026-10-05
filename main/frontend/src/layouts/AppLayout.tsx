import { NavLink, Outlet } from "react-router-dom";
import type { NavItem } from "../types";

const NAV: NavItem[] = [
  { to: "/", label: "Главная" },
  { to: "/plans", label: "Каталог УП" },
  { to: "/workload", label: "Нагрузка" },
  { to: "/schedule", label: "Расписание" },
  { to: "/substitutions", label: "Замены" },
  { to: "/journal", label: "Сверка" },
  { to: "/reports", label: "Отчёты" },
  { to: "/settings", label: "Настройки" },
];

export function AppLayout() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">УП</span>
          <div>
            <div className="brand-title">StudyPlan</div>
            <div className="brand-sub">Optimisation</div>
          </div>
        </div>
        <nav className="nav">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
