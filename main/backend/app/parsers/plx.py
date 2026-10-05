"""MMIS PLX parser stub (UTF-16 LE XML)."""
from pathlib import Path


class PlxParser:
    def detect(self, path: Path) -> dict:
        raw = path.read_bytes()[:4]
        has_utf16_bom = raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff")
        is_zeroed = len(raw) > 0 and set(raw) == {0}
        return {
            "path": str(path),
            "has_utf16_bom": has_utf16_bom,
            "suspected_corrupt": is_zeroed or (path.stat().st_size == 0),
            "parser": "plx",
            "implemented": False,
        }

    def parse(self, path: Path) -> dict:
        meta = self.detect(path)
        if meta["suspected_corrupt"]:
            return {**meta, "status": "error", "message": "Файл повреждён или пуст"}
        return {**meta, "status": "not_implemented", "rows": []}
