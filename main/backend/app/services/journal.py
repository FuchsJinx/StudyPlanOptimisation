"""Journal / OCR service stub."""


class JournalService:
    def status(self) -> dict:
        return {"module": "journal", "ready": False, "message": "stub"}
