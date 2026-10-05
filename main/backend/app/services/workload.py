"""Workload service stub."""


class WorkloadService:
    """Расчёт и назначение нагрузки — реализация на следующих этапах."""

    def status(self) -> dict:
        return {"module": "workload", "ready": False, "message": "stub"}
