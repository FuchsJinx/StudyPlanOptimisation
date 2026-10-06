# Backend (FastAPI)

## Запуск

```powershell
cd main\\backend
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Структура

- `app/api` — REST-роуты
- `app/services` — бизнес-логика
- `app/repositories` — доступ к данным
- `app/db` — модели SQLAlchemy и сессия
- `app/parsers` — PLX / XLSX
- `app/schemas` — Pydantic-схемы

## Пользователи (БД)

Таблица `users` создаётся при старте API. Стартовые учётки (если БД пуста):


| Логин      | Пароль       | Роль       |
| ---------- | ------------ | ---------- |
| admin      | Admin123!    | admin      |
| methodist  | Method123!   | methodist  |
| dispatcher | Dispatch123! | dispatcher |


Ручная инициализация:

```powershell
py -3 scripts/init_users_db.py
```

API:

- `POST /api/auth/login`
- `POST /api/auth/register` — публичная регистрация (роли methodist / dispatcher), сразу выдаёт токен
- `GET /api/auth/me`
- `GET /api/admin/users`
- `POST /api/admin/users`
- `POST /api/admin/users/seed`



## Хеширование паролей

- Алгоритм: **bcrypt** (`bcrypt.gensalt(rounds=12)`).
- Модуль: `app/security.py` — `hash_password` / `verify_password`.
- В таблице `users` хранится только `password_hash`, не открытый пароль.
- Создание пользователя и seed всегда вызывают `hash_password`.
- Смена пароля: `POST /api/auth/change-password` (Bearer-токен).

