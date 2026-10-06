"""Auth / user schemas."""
from datetime import datetime
import re

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel

LOGIN_RE = re.compile(r"^[a-zA-Z0-9._-]{3,50}$")


class LoginRequest(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("login")
    @classmethod
    def validate_login(cls, value: str) -> str:
        login = value.strip()
        if not LOGIN_RE.match(login):
            raise ValueError("Логин: латиница, цифры, точка, _ и - (3–50 символов)")
        return login


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str
    login: str
    permissions: list[str] = []
    email: str | None = None


class UserOut(ORMModel):
    id: int
    login: str
    full_name: str
    role: str
    email: str | None = None
    is_active: bool
    created_at: datetime | None = None


class UserCreate(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    full_name: str = Field(min_length=1, max_length=100)
    role: str = Field(default="methodist")
    email: str | None = None

    @field_validator("login")
    @classmethod
    def validate_login(cls, value: str) -> str:
        login = value.strip()
        if not LOGIN_RE.match(login):
            raise ValueError("Логин: латиница, цифры, точка, _ и - (3–50 символов)")
        return login


class RegisterRequest(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    password_confirm: str = Field(min_length=6, max_length=128)
    full_name: str = Field(min_length=2, max_length=100)
    role: str = Field(default="methodist")
    email: str | None = Field(default=None, max_length=120)

    @field_validator("login")
    @classmethod
    def validate_login(cls, value: str) -> str:
        login = value.strip()
        if not LOGIN_RE.match(login):
            raise ValueError("Логин: латиница, цифры, точка, _ и - (3–50 символов)")
        return login

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        name = " ".join(value.split())
        if len(name) < 2:
            raise ValueError("Укажите ФИО")
        return name

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None:
            return None
        email = value.strip()
        if not email:
            return None
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Некорректный email")
        return email

    @field_validator("role")
    @classmethod
    def validate_public_role(cls, value: str) -> str:
        role = (value or "").strip().lower()
        if role not in {"methodist", "dispatcher"}:
            raise ValueError("При регистрации доступны роли: методист или диспетчер")
        return role


class SeedResult(BaseModel):
    created: int
    total_users: int
    message: str


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=6, max_length=128)


class SessionOut(BaseModel):
    login: str
    full_name: str
    role: str
    role_label: str
    permissions: list[str]
    is_authenticated: bool = True
