# Frontend (Electron + React + Vite)

## Запуск UI (браузер / Vite)

```powershell
cd main\\frontend
npm install
npm run dev
```

Откроется http://127.0.0.1:5173 (прокси `/api` → backend `:8000`).

## Electron

1. Запустите Vite (`npm run dev`)
2. В другом терминале: `npx electron .` (из `main/frontend`, нужен пакет `electron` — добавьте при упаковке)

Пока Electron main/preload лежат как `.cjs`-заготовки.
