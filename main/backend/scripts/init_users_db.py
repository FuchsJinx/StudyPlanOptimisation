#!/usr/bin/env python
"""Create SQLite schema and seed default users.

Usage (from main/backend):
  py -3 scripts/init_users_db.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.db.seed import seed_users_if_empty
from app.db.session import SessionLocal, init_db
from app.repositories.users import UserRepository


def main() -> None:
    settings = get_settings()
    db_path = settings.database_url.replace("sqlite:///", "")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"DB: {settings.database_url}")
    init_db()
    print("Schema ensured (users and other tables).")

    created = seed_users_if_empty()
    db = SessionLocal()
    try:
        users = UserRepository(db).list(limit=100)
        print(f"Seed created: {created}")
        print(f"Users total: {len(users)}")
        for u in users:
            print(f"  - {u.login:12} | {u.role:12} | {u.full_name}")
    finally:
        db.close()

    print()
    print("Default passwords (change in production):")
    print("  admin      / Admin123!")
    print("  methodist  / Method123!")
    print("  dispatcher / Dispatch123!")


if __name__ == "__main__":
    main()
