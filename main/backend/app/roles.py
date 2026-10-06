"""Система ролей и прав доступа."""
from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    METHODIST = "methodist"
    DISPATCHER = "dispatcher"


ROLE_LABELS: dict[str, str] = {
    Role.ADMIN.value: "Администратор",
    Role.METHODIST.value: "Методист",
    Role.DISPATCHER.value: "Диспетчер",
}

# Права модулей интерфейса / API
ROLE_PERMISSIONS: dict[str, set[str]] = {
    Role.ADMIN.value: {
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
    },
    Role.METHODIST.value: {
        "dashboard",
        "directories",
        "plans",
        "workload",
        "journal",
        "reports",
        "settings",
        "profile",
    },
    Role.DISPATCHER.value: {
        "dashboard",
        "directories",
        "schedule",
        "substitutions",
        "reports",
        "settings",
        "profile",
    },
}

ALLOWED_ROLES = set(ROLE_PERMISSIONS.keys())


def normalize_role(role: str) -> str:
    value = (role or "").strip().lower()
    if value not in ALLOWED_ROLES:
        raise ValueError(f"Неизвестная роль: {role}")
    return value


def role_label(role: str) -> str:
    return ROLE_LABELS.get(role, role)


def has_permission(role: str, permission: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, set())
    return permission in perms


def permissions_for(role: str) -> list[str]:
    return sorted(ROLE_PERMISSIONS.get(role, set()))
