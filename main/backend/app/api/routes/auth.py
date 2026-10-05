"""Auth routes (stub)."""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    login: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    full_name: str


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest) -> LoginResponse:
    # Stub for MVP scaffold — replace with real AuthService.
    return LoginResponse(
        access_token="dev-token",
        role="methodist",
        full_name=body.login or "Методист",
    )


@router.get("/me")
def me() -> dict:
    return {"login": "demo", "role": "methodist", "full_name": "Демо Пользователь"}
