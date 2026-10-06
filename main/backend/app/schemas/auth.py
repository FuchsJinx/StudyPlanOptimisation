"""Auth / user schemas."""
from datetime import datetime
import re

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel

LOGIN_RE = re.compile(r"^[a-zA-Z0-9._-]{3,50}$")


class LoginRequest(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    # min_length=1: короткие неверные пароли получают 401, а не 422
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


class SeedResult(BaseModel):
    created: int
    total_users: int
    message: str
