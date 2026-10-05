# Deploy / CI / Lint

Каталог содержит конфигурацию проверки качества кода и CI.

## Структура

| Путь | Назначение |
|------|------------|
| `ci.yml` | Описание pipeline (зеркало workflow) |
| `lint/ruff.toml` | Lint + format Python (backend) |
| `lint/eslint.config.mjs` | Lint TypeScript/React (frontend) |
| `lint/pre-commit-config.yaml` | Опциональные git-hooks |
| `scripts/lint.ps1` | Локальный запуск на Windows |
| `scripts/lint.sh` | Локальный запуск на Linux/macOS |

Рабочий GitHub Actions workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

## Локальный lint

```powershell
# Windows
.\deploy\scripts\lint.ps1
```

```bash
# Linux / macOS / Git Bash
bash deploy/scripts/lint.sh
```

Требования: Python 3.12+, `pip install ruff`; для frontend — Node 20+ и `npm run lint` в `main/frontend`.

## Jobs CI

1. **lint-python** — `ruff check` + `ruff format --check`
2. **lint-frontend** — `npm run lint` (если есть `package.json`)
3. **test-python** — `pytest` (если есть тесты)

Пока исходников нет, jobs завершаются успешно со статусом *skip*.
