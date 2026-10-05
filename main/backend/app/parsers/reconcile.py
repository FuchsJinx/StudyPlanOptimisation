"""PLX vs XLSX reconcile stub."""


def reconcile_by_filename(plx_name: str, xlsx_name: str) -> dict:
    """Грубая связка по имени файла (год/код/форма)."""
    return {
        "plx": plx_name,
        "xlsx": xlsx_name,
        "matched": PathStem(plx_name) == PathStem(xlsx_name),
        "implemented": False,
    }


def PathStem(name: str) -> str:
    stem = name
    for suffix in (".plx.xlsx", ".xlsx", ".plx"):
        if stem.lower().endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    return stem.lower().replace(" ", "")
