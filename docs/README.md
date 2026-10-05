# StudyPlanOptimisation

ПК-приложение для автоматизации работы учебной части СПО: импорт учебных планов (`.plx` / `.xlsx`), расчёт нагрузки преподавателей, составление расписания, учёт замен и сверка ведомостей учёта часов.

Репозиторий: [FuchsJinx/StudyPlanOptimisation](https://github.com/FuchsJinx/StudyPlanOptimisation)

## Цели продукта

- единый каталог учебных планов с нормализованной моделью;
- расчёт и назначение нагрузки, экспорт в Excel;
- генерация и ручная правка расписания с проверкой конфликтов;
- журнал замен с пересчётом фактической нагрузки;
- сверка фото/сканов ведомостей (OCR / опционально Vision LLM).

## Архитектура

Многоуровневая (N-tier):

1. **Presentation** — Electron + React + TypeScript  
2. **API** — FastAPI (REST, localhost / LAN)  
3. **Business Logic** — Curriculum, Workload, Schedule, Substitution, Journal, Reporting, Admin  
4. **DAL** — Repository + Unit of Work (SQLAlchemy)  
5. **Database** — SQLite (+ файлы вложений)

Диаграммы: см. SVG в каталоге `docs/` (компоненты, развёртывание, БД).

## Структура репозитория

```
├── .github/workflows/   # GitHub Actions CI
├── deploy/              # CI-описание, lint-конфиги, скрипты
├── docs/                # Документация и диаграммы
├── main/                # Исходный код (backend + frontend)
│   ├── backend/         # Python / FastAPI
│   └── frontend/        # Electron / React
├── references/          # Эталонные УП, фото, примеры
└── test/                # Тесты и шаблоны квестов
```

## Быстрый старт (после появления кода)

```powershell
# Backend
cd main\backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd main\frontend
npm install
npm run dev
```

## Качество кода

```powershell
.\deploy\scripts\lint.ps1
```

CI запускается на `push` / `pull_request` в `main`: lint Python (ruff), lint frontend (eslint), pytest.

## Роли пользователей

| Роль | Задачи |
|------|--------|
| Методист | Импорт УП, нагрузка, отчёты |
| Диспетчер | Расписание, замены |
| Администратор | Пользователи, backup, настройки |

## Статус

Каркас репозитория: документация, CI/lint, шаблоны тестов. Реализация модулей — по этапам MVP (импорт → нагрузка → расписание → замены → сверка).

## Лицензия

Учебный / курсовой проект. Уточните лицензию при публикации.
