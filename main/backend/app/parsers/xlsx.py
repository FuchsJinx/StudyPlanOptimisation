"""XLSX year-profile parser stub."""
from pathlib import Path


class XlsxParser:
    SUPPORTED_YEARS = (2023, 2024, 2025, 2026)

    def detect_profile(self, path: Path) -> dict:
        name = path.name
        year = None
        for y in self.SUPPORTED_YEARS:
            if str(y) in name:
                year = y
                break
        return {
            "path": str(path),
            "detected_year": year,
            "parser": "xlsx",
            "implemented": False,
        }

    def parse(self, path: Path) -> dict:
        meta = self.detect_profile(path)
        return {**meta, "status": "not_implemented", "rows": []}
