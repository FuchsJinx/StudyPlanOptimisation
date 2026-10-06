"""Authentication and user bootstrap service."""
from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.users import UserRepository
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

ALLOWED_ROLES = {"admin", "methodist", "dispatcher"}


@dataclass
class AuthResult:
    access_token: str
    token_type: str
    role: str
    full_name: str
    login: str


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def seed_default_users(self) -> int:
        """Создаёт стартовых пользователей, если таблица пуста. Возвращает число созданных."""
        if self.users.count() > 0:
            return 0
        created = 0
        for item in DEFAULT_USERS:
            user = User(
                login=item["login"],
                password_hash=hash_password(item["password"]),
                full_name=item["full_name"],
                role=item["role"],
                email=item["email"],
                is_active=True,
            )
            self.db.add(user)
            created += 1
        self.db.commit()
        return created

    def authenticate(self, login: str, password: str) -> AuthResult:
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
        token = create_access_token(
            subject=user.login,
            role=user.role,
            full_name=user.full_name,
        )
        return AuthResult(
            access_token=token,
            token_type="bearer",
            role=user.role,
            full_name=user.full_name,
            login=user.login,
        )

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
        if role not in ALLOWED_ROLES:
            raise HTTPException(status_code=400, detail=f"Роль должна быть одной из: {sorted(ALLOWED_ROLES)}")
        if self.users.get_by_login(login_norm):
            raise HTTPException(status_code=409, detail="Пользователь с таким логином уже существует")
        user = User(
            login=login_norm,
            password_hash=hash_password(password),
            full_name=full_name.strip(),
            role=role,
            email=email,
            is_active=True,
        )
        return self.users.add(user)
