"""Authentication, roles and session service."""
from __future__ import annotations

from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.sessions import SessionRepository
from app.repositories.users import UserRepository
from app.roles import ALLOWED_ROLES, normalize_role, permissions_for, role_label
from app.security import create_access_token, hash_password, verify_password

DEFAULT_USERS = (
    {
        "login": "admin",
        "password": "Admin123!",
        "full_name": "Администратор системы",
        "role": "admin",
        "email": "admin@local",
    },
    {
        "login": "methodist",
        "password": "Method123!",
        "full_name": "Методист учебной части",
        "role": "methodist",
        "email": "methodist@local",
    },
    {
        "login": "dispatcher",
        "password": "Dispatch123!",
        "full_name": "Диспетчер расписания",
        "role": "dispatcher",
        "email": "dispatcher@local",
    },
)


@dataclass
class AuthResult:
    access_token: str
    token_type: str
    role: str
    full_name: str
    login: str
    jti: str
    permissions: list[str]
    email: str | None = None


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)
        self.sessions = SessionRepository(db)

    def seed_default_users(self) -> int:
        if self.users.count() > 0:
            return 0
        created = 0
        for item in DEFAULT_USERS:
            user = User(
                login=item["login"],
                password_hash=hash_password(item["password"]),
                full_name=item["full_name"],
                role=normalize_role(item["role"]),
                email=item["email"],
                is_active=True,
            )
            self.db.add(user)
            created += 1
        self.db.commit()
        return created

    def authenticate(self, login: str, password: str, user_agent: str | None = None) -> AuthResult:
        user = self.users.get_by_login(login.strip())
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
            )
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
            )
        token, jti, expires_at = create_access_token(
            subject=user.login,
            role=user.role,
            full_name=user.full_name,
        )
        self.sessions.create(
            user_id=user.id,
            jti=jti,
            expires_at=expires_at,
            user_agent=user_agent,
        )
        return AuthResult(
            access_token=token,
            token_type="bearer",
            role=user.role,
            full_name=user.full_name,
            login=user.login,
            jti=jti,
            permissions=permissions_for(user.role),
            email=user.email,
        )

    def logout(self, jti: str) -> bool:
        return self.sessions.revoke(jti)

    def logout_all(self, user_id: int) -> int:
        return self.sessions.revoke_all_for_user(user_id)

    def create_user(
        self,
        *,
        login: str,
        password: str,
        full_name: str,
        role: str,
        email: str | None = None,
    ) -> User:
        login_norm = login.strip()
        if not login_norm or not password:
            raise HTTPException(status_code=400, detail="Логин и пароль обязательны")
        try:
            role_norm = normalize_role(role)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Роль должна быть одной из: {sorted(ALLOWED_ROLES)}",
            ) from None
        if self.users.get_by_login(login_norm):
            raise HTTPException(status_code=409, detail="Пользователь с таким логином уже существует")
        user = User(
            login=login_norm,
            password_hash=hash_password(password),
            full_name=full_name.strip(),
            role=role_norm,
            email=email,
            is_active=True,
        )
        return self.users.add(user)

    def register(
        self,
        *,
        login: str,
        password: str,
        password_confirm: str,
        full_name: str,
        role: str,
        email: str | None = None,
        user_agent: str | None = None,
    ) -> AuthResult:
        if password != password_confirm:
            raise HTTPException(status_code=400, detail="Пароли не совпадают")
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Пароль не короче 6 символов")
        public_roles = {"methodist", "dispatcher"}
        role_norm = (role or "").strip().lower()
        if role_norm not in public_roles:
            raise HTTPException(
                status_code=400,
                detail="При регистрации доступны роли: методист или диспетчер",
            )
        self.create_user(
            login=login,
            password=password,
            full_name=full_name,
            role=role_norm,
            email=email,
        )
        return self.authenticate(login, password, user_agent=user_agent)

    def change_password(self, login: str, current_password: str, new_password: str) -> None:
        if len(new_password) < 6:
            raise HTTPException(status_code=400, detail="Новый пароль не короче 6 символов")
        user = self.users.get_by_login(login.strip())
        if user is None or not user.is_active:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Текущий пароль неверен")
        user.password_hash = hash_password(new_password)
        self.db.add(user)
        self.db.commit()
        # после смены пароля гасим все сессии пользователя
        self.sessions.revoke_all_for_user(user.id)

    def get_user_by_login(self, login: str) -> User | None:
        return self.users.get_by_login(login)

    def ensure_active_session(self, jti: str) -> None:
        if not self.sessions.is_active(jti):
            raise HTTPException(status_code=401, detail="Сессия недействительна или завершена")

    @staticmethod
    def describe_role(role: str) -> dict:
        return {
            "role": role,
            "label": role_label(role),
            "permissions": permissions_for(role),
        }
