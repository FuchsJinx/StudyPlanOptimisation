# Тесты и квесты

## Квесты приёмки

Шаблоны пользовательских сценариев для ручной и полуавтоматической проверки:

- [`quests/QUEST_TEMPLATE.md`](quests/QUEST_TEMPLATE.md) — пустой шаблон  
- [`quests/Q-001_import_plx.example.md`](quests/Q-001_import_plx.example.md) — пример заполнения  

Копируйте шаблон как `Q-XXX_short_name.md` и заполняйте по мере реализации модулей.

## Автотесты

Планируется:

- контрактные тесты парсеров PLX/XLSX на фикстурах из `references/`;
- unit-тесты сервисов нагрузки и замен;
- API-тесты FastAPI (`pytest` + `httpx`).

Запуск (когда появятся тесты):

```powershell
pytest -q
```
