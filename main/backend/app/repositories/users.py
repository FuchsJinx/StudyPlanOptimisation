"""User repository."""
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_login(self, login: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.login == login)
            .one_or_none()
        )

    def list_active(self) -> list[User]:
        return list(
            self.db.query(User)
            .filter(User.is_active.is_(True))
            .order_by(User.login)
            .all()
        )

    def count(self) -> int:
        return int(self.db.query(User).count())
