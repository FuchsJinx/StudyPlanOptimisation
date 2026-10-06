"""Auth routes: login, me, logout, session, change-password."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.db.models.user import User
from app.roles import permissions_for, role_label
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    SessionOut,
    UserOut,
)
from app.security import decode_access_token
from app.services.auth import AuthService
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
bearer = HTTPBearer(auto_error=False)


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)) -> LoginResponse:
    ua = request.headers.get("user-agent")
    result = AuthService(db).authenticate(body.login, body.password, user_agent=ua)
    return LoginResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        role=result.role,
        full_name=result.full_name,
        login=result.login,
        permissions=result.permissions,
        email=result.email,
    )


@router.post("/register", response_model=LoginResponse, status_code=201)
def register(body: RegisterRequest, request: Request, db: Session = Depends(get_db)) -> LoginResponse:
    """Публичная регистрация (методист / диспетчер) с авто-входом."""
    ua = request.headers.get("user-agent")
    result = AuthService(db).register(
        login=body.login,
        password=body.password,
        password_confirm=body.password_confirm,
        full_name=body.full_name,
        role=body.role,
        email=body.email,
        user_agent=ua,
    )
    return LoginResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        role=result.role,
        full_name=result.full_name,
        login=result.login,
        permissions=result.permissions,
        email=result.email,
    )


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(user)


@router.get("/session", response_model=SessionOut)
def session_info(user: User = Depends(get_current_user)) -> SessionOut:
    return SessionOut(
        login=user.login,
        full_name=user.full_name,
        role=user.role,
        role_label=role_label(user.role),
        permissions=permissions_for(user.role),
        is_authenticated=True,
    )


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> dict:
    if credentials is None:
        return {"status": "ok", "message": "Сессия уже завершена"}
    payload = decode_access_token(credentials.credentials)
    if payload and payload.get("jti"):
        AuthService(db).logout(payload["jti"])
    return {"status": "ok", "message": "Выход выполнен"}


@router.post("/logout-all")
def logout_all(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> dict:
    count = AuthService(db).logout_all(user.id)
    return {"status": "ok", "message": f"Завершено сессий: {count}", "revoked": count}


@router.post("/change-password")
def change_password(
    body: ChangePasswordRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    AuthService(db).change_password(user.login, body.current_password, body.new_password)
    return {"status": "ok", "message": "Пароль обновлён. Выполните вход снова."}


@router.get("/roles")
def list_roles() -> dict:
    from app.roles import ROLE_LABELS, ROLE_PERMISSIONS

    return {
        "roles": [
            {
                "id": role,
                "label": ROLE_LABELS[role],
                "permissions": sorted(ROLE_PERMISSIONS[role]),
            }
            for role in sorted(ROLE_PERMISSIONS)
        ]
    }
