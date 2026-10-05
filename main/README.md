# main — исходный код StudyPlanOptimisation

## Состав

| Каталог | Стек | Назначение |
|---------|------|------------|
| `backend/` | Python 3.12, FastAPI, SQLAlchemy, SQLite | API, парсеры, бизнес-логика, БД |
| `frontend/` | React, TypeScript, Vite, Electron | UI методиста/диспетчера |

## Быстрый старт

### 1. Backend

```powershell
cd main\\backend
py -3 -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Проверка: http://127.0.0.1:8000/api/health и http://127.0.0.1:8000/docs

### 2. Frontend

```powershell
cd main\\frontend
npm install
npm run dev
```

## Карта модулей backend

```
app/
  api/routes/     auth, plans, workload, schedule, substitutions, journal, reports, admin
  services/       бизнес-логика (часть — stub)
  repositories/   доступ к данным
  db/models/      ORM-модели по главе 8
  parsers/        PLX / XLSX / reconcile (stub)
  schemas/        Pydantic DTO
```

## Дальше по плану

1. Реализовать `PlxParser` / `XlsxParser` на фикстурах из `references/`
2. CRUD справочников и импорт УП в UI
3. Нагрузка → расписание → замены → сверка
