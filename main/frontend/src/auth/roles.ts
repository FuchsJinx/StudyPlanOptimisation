import type { Role } from "../types";

export type NavItemConfig = {
  to: string;
  label: string;
  permission: string;
  badge?: number;
  icon?: "home" | "catalog" | "import" | "workload" | "schedule" | "swap" | "check" | "reports" | "dirs" | "help";
};

export const NAV_WORKSPACE: NavItemConfig[] = [
  { to: "/", label: "Обзор", permission: "dashboard", icon: "home" },
  { to: "/plans", label: "Каталог УП", permission: "plans", icon: "catalog", badge: 24 },
  { to: "/import", label: "Импорт", permission: "plans", icon: "import" },
  { to: "/workload", label: "Нагрузка", permission: "workload", icon: "workload" },
  { to: "/schedule", label: "Расписание", permission: "schedule", icon: "schedule" },
  { to: "/substitutions", label: "Замены", permission: "substitutions", icon: "swap", badge: 3 },
  { to: "/journal", label: "Сверка", permission: "journal", icon: "check" },
  { to: "/reports", label: "Отчёты", permission: "reports", icon: "reports" },
  { to: "/directories", label: "Справочники", permission: "directories", icon: "dirs" },
];

export const NAV_SYSTEM: NavItemConfig[] = [
  { to: "/settings", label: "Помощь", permission: "settings", icon: "help" },
];

/** @deprecated use NAV_WORKSPACE */
export const NAV_BY_PERMISSION = NAV_WORKSPACE;

export const DASHBOARD_MODULES: NavItemConfig[] = [
  { to: "/directories", label: "Справочники", permission: "directories" },
  { to: "/plans", label: "Каталог УП", permission: "plans" },
  { to: "/workload", label: "Нагрузка", permission: "workload" },
  { to: "/schedule", label: "Расписание", permission: "schedule" },
  { to: "/substitutions", label: "Замены", permission: "substitutions" },
  { to: "/journal", label: "Сверка журналов", permission: "journal" },
  { to: "/reports", label: "Отчёты", permission: "reports" },
  { to: "/settings", label: "Настройки", permission: "settings" },
];

const FALLBACK_PERMISSIONS: Record<Role, string[]> = {
  admin: [
    "dashboard",
    "directories",
    "plans",
    "workload",
    "schedule",
    "substitutions",
    "journal",
    "reports",
    "settings",
    "profile",
    "admin",
    "users",
  ],
  methodist: [
    "dashboard",
    "directories",
    "plans",
    "workload",
    "journal",
    "reports",
    "settings",
    "profile",
  ],
  dispatcher: [
    "dashboard",
    "directories",
    "schedule",
    "substitutions",
    "reports",
    "settings",
    "profile",
  ],
};

export function permissionsForRole(role: Role, fromServer?: string[]): string[] {
  const fallback = FALLBACK_PERMISSIONS[role] ?? [];
  if (!fromServer?.length) return fallback;
  return Array.from(new Set([...fromServer, ...fallback]));
}

export function canAccess(permissions: string[], permission: string): boolean {
  return permissions.includes(permission);
}

export function canEditDirectories(role: Role | undefined): boolean {
  return role === "admin" || role === "methodist";
}

export function roleLabel(role: Role): string {
  switch (role) {
    case "admin":
      return "Администратор";
    case "methodist":
      return "Методист";
    case "dispatcher":
      return "Диспетчер";
    default:
      return role;
  }
}
