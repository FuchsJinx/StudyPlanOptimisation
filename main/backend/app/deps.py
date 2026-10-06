"""Shared FastAPI dependencies."""
from collections.abc import Callable, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.session import SessionLocal
from app.roles import has_permission
from app.security import decode_access_token
from app.services.auth import AuthService

bearer_scheme = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Требуется авторизация")
    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload or "jti" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный токен")

    service = AuthService(db)
    service.ensure_active_session(payload["jti"])
    user = service.get_user_by_login(payload["sub"])
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    return user


def require_roles(*roles: str) -> Callable:
    allowed = {r.lower() for r in roles}

    def _dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав. Требуется роль: {', '.join(sorted(allowed))}",
            )
        return user

    return _dependency


def require_permission(permission: str) -> Callable:
    def _dependency(user: User = Depends(get_current_user)) -> User:
        if not has_permission(user.role, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав. Требуется разрешение: {permission}",
            )
        return user

    return _dependency
