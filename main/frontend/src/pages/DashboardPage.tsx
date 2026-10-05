import { useEffect, useState } from "react";
import { PageHeader } from "../components/PageHeader";
import { apiGet, HealthResponse } from "../api/client";

export function DashboardPage() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiGet<HealthResponse>("/health")
      .then(setHealth)
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <section>
      <PageHeader
        title="Главная панель"
        subtitle="Ключевые показатели и быстрый доступ к операциям"
      />
      <div className="grid-3">
        <div className="card metric">
          <div className="metric-label">УП в каталоге</div>
          <div className="metric-value">—</div>
        </div>
        <div className="card metric">
          <div className="metric-label">Группы без нагрузки</div>
          <div className="metric-value">—</div>
        </div>
        <div className="card metric">
          <div className="metric-label">Конфликты расписания</div>
          <div className="metric-value">—</div>
        </div>
      </div>
      <div className="card" style={{ marginTop: 16 }}>
        <h2>Статус API</h2>
        {error && <p className="err-text">Backend недоступен: {error}</p>}
        {health && (
          <p className="ok-text">
            {health.app} · {health.status} · v{health.version} ({health.env})
          </p>
        )}
        {!health && !error && <p className="muted">Проверка…</p>}
      </div>
    </section>
  );
}
