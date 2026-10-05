import { useEffect, useState } from "react";
import { PageHeader } from "../components/PageHeader";
import { StatusBadge } from "../components/StatusBadge";
import { Plan, apiGet } from "../api/client";

export function PlansPage() {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiGet<Plan[]>("/plans")
      .then(setPlans)
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <section>
      <PageHeader
        title="Каталог учебных планов"
        subtitle="Импорт .plx / .xlsx, статусы и поиск"
        actions={<button className="btn primary">Импортировать УП</button>}
      />
      {error && <p className="err-text">{error}</p>}
      <div className="card table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Код</th>
              <th>Название</th>
              <th>Год</th>
              <th>Форма</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            {plans.length === 0 ? (
              <tr>
                <td colSpan={5} className="muted">
                  Планы пока не импортированы
                </td>
              </tr>
            ) : (
              plans.map((p) => (
                <tr key={p.id}>
                  <td>{p.code ?? "—"}</td>
                  <td>{p.title}</td>
                  <td>{p.study_year}</td>
                  <td>{p.education_form}</td>
                  <td>
                    <StatusBadge status={p.import_status} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
