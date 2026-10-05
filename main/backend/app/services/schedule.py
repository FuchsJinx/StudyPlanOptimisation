"""Schedule service stub."""


class ScheduleService:
    """Генерация/правка расписания — реализация на следующих этапах."""

    def status(self) -> dict:
        return {"module": "schedule", "ready": False, "message": "stub"}
