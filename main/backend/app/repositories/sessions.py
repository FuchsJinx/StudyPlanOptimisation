"""Session repository."""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models.session import UserSession
from app.repositories.base import BaseRepository


class SessionRepository(BaseRepository[UserSession]):
    def __init__(self, db: Session):
        super().__init__(db, UserSession)

    def get_by_jti(self, jti: str) -> UserSession | None:
        return self.db.query(UserSession).filter(UserSession.jti == jti).one_or_none()

    def create(
        self,
        *,
        user_id: int,
        jti: str,
        expires_at: datetime,
        user_agent: str | None = None,
    ) -> UserSession:
        row = UserSession(
            user_id=user_id,
            jti=jti,
            expires_at=expires_at,
            user_agent=user_agent,
        )
        return self.add(row)

    def revoke(self, jti: str) -> bool:
        row = self.get_by_jti(jti)
        if row is None:
            return False
        if row.revoked_at is None:
            row.revoked_at = datetime.now(timezone.utc)
            self.db.add(row)
            self.db.commit()
        return True

    def revoke_all_for_user(self, user_id: int) -> int:
        rows = (
            self.db.query(UserSession)
            .filter(UserSession.user_id == user_id, UserSession.revoked_at.is_(None))
            .all()
        )
        now = datetime.now(timezone.utc)
        for row in rows:
            row.revoked_at = now
            self.db.add(row)
        self.db.commit()
        return len(rows)

    def is_active(self, jti: str) -> bool:
        row = self.get_by_jti(jti)
        if row is None or row.revoked_at is not None:
            return False
        exp = row.expires_at
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        return exp > datetime.now(timezone.utc)
