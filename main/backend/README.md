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

API docs: http://127.0.0.1:8000/docs

## Структура

- `app/api` — REST-роуты
- `app/services` — бизнес-логика
- `app/repositories` — доступ к данным
- `app/db` — модели SQLAlchemy и сессия
- `app/parsers` — PLX / XLSX
- `app/schemas` — Pydantic-схемы
