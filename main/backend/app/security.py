"""Password hashing (bcrypt) and JWT helpers.

Пароли никогда не хранятся в открытом виде.
В БД сохраняется только bcrypt-хеш (поле users.password_hash).
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import bcrypt
from jose import JWTError, jwt

from app.config import get_settings

ALGORITHM = "HS256"
BCRYPT_ROUNDS = 12
BCRYPT_PREFIXES = ("$2a$", "$2b$", "$2y$")


def _password_bytes(password: str) -> bytes:
    raw = password.encode("utf-8")
    return raw[:72] if len(raw) > 72 else raw


def is_bcrypt_hash(value: str) -> bool:
    return bool(value) and value.startswith(BCRYPT_PREFIXES) and len(value) >= 59


def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Пароль не может быть пустым")
    hashed = bcrypt.hashpw(_password_bytes(password), bcrypt.gensalt(rounds=BCRYPT_ROUNDS))
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    if not plain_password or not password_hash:
        return False
    if not is_bcrypt_hash(password_hash):
        return False
    try:
        return bcrypt.checkpw(_password_bytes(plain_password), password_hash.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(
    *,
    subject: str,
    role: str,
    full_name: str,
    jti: str | None = None,
) -> tuple[str, str, datetime]:
    """Возвращает (token, jti, expires_at)."""
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    token_jti = jti or uuid4().hex
    payload = {
        "sub": subject,
        "role": role,
        "full_name": full_name,
        "jti": token_jti,
        "exp": expire,
    }
    token = jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)
    return token, token_jti, expire


def decode_access_token(token: str) -> dict | None:
    settings = get_settings()
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except JWTError:
        return None
