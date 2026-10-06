"""Auth routes backed by users table."""
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.deps import get_db
from app.repositories.users import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse, UserOut
from app.security import decode_access_token
from app.services.auth import AuthService

router = APIRouter()
bearer = HTTPBearer(auto_error=False)


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    result = AuthService(db).authenticate(body.login, body.password)
    return LoginResponse(
        access_token=result.access_token,
        token_type=result.token_type,
        role=result.role,
        full_name=result.full_name,
        login=result.login,
    )


@router.get("/me", response_model=UserOut)
def me(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> UserOut:
    if credentials is None:
        # Для удобства локальной разработки без токена — первый активный пользователь.
        users = UserRepository(db).list_active()
        if not users:
            from fastapi import HTTPException
            raise HTTPException(status_code=401, detail="Нет пользователей в БД")
        return UserOut.model_validate(users[0])

    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Недействительный токен")

    user = UserRepository(db).get_by_login(payload["sub"])
    if user is None or not user.is_active:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return UserOut.model_validate(user)
