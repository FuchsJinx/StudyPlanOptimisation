"""Admin routes: user management."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.repositories.users import UserRepository
from app.schemas.auth import SeedResult, UserCreate, UserOut
from app.services.auth import AuthService

router = APIRouter()


@router.get("/status")
def status() -> dict:
    return {"module": "admin", "ready": True, "message": "users db ready"}


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)) -> list[UserOut]:
    users = UserRepository(db).list(limit=500)
    return [UserOut.model_validate(u) for u in users]


@router.post("/users", response_model=UserOut, status_code=201)
def create_user(body: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    user = AuthService(db).create_user(
        login=body.login,
        password=body.password,
        full_name=body.full_name,
        role=body.role,
        email=body.email,
    )
    return UserOut.model_validate(user)


@router.post("/users/seed", response_model=SeedResult)
def seed_users(db: Session = Depends(get_db)) -> SeedResult:
    service = AuthService(db)
    created = service.seed_default_users()
    total = UserRepository(db).count()
    if created:
        message = f"Создано пользователей: {created}"
    else:
        message = "Пользователи уже существуют — seed пропущен"
    return SeedResult(created=created, total_users=total, message=message)
