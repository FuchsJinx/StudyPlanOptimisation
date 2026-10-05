# Локальный lint (Windows PowerShell)
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Set-Location $Root

Write-Host "==> Python (ruff)"
$pyFiles = Get-ChildItem -Path "main\backend" -Filter "*.py" -Recurse -ErrorAction SilentlyContinue
if ($pyFiles) {
  py -3 -m ruff check main/backend --config deploy/lint/ruff.toml
  py -3 -m ruff format main/backend --check --config deploy/lint/ruff.toml
} else {
  Write-Host "skip: нет Python-файлов в main/backend"
}

Write-Host "==> Frontend (eslint)"
if (Test-Path "main\frontend\package.json") {
  Push-Location "main\frontend"
  npm run lint
  Pop-Location
} else {
  Write-Host "skip: нет package.json в main/frontend"
}

Write-Host "Lint OK"
