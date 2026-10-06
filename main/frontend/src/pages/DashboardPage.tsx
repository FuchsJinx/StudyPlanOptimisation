import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import { canAccess, roleLabel } from "../auth/roles";
import {
  IconBook,
  IconCalendar,
  IconClock,
  IconDownload,
  IconPeople,
  IconWarn,
} from "../components/Icons";

export function DashboardPage() {
  const { session, permissions } = useAuth();

  return (
    <section className="dashboard">
      <div className="breadcrumbs">
        <span>Учебное планирование</span>
        <span>›</span>
        <strong>Обзор</strong>
      </div>

      <header className="page-header">
        <div>
          <h1>Обзор учебного процесса</h1>
          <p className="muted">
            {session
              ? `${roleLabel(session.role)} · сводка по учебному году 2025/2026`
              : "Сводка по учебному году"}
          </p>
        </div>
        <button type="button" className="btn outline">
          <IconDownload size={16} />
          Скачать сводку
        </button>
      </header>

      <div className="quick-actions-row">
        <span className="quick-actions-label">Быстрые действия</span>
        {canAccess(permissions, "plans") && (
          <Link className="btn outline" to="/import">
            Импортировать УП
          </Link>
        )}
        {canAccess(permissions, "workload") && (
          <Link className="btn outline" to="/workload">
            Создать назначение
          </Link>
        )}
        {canAccess(permissions, "substitutions") && (
          <Link className="btn outline" to="/substitutions">
            Зарегистрировать замену
          </Link>
        )}
        {!canAccess(permissions, "plans") &&
          !canAccess(permissions, "workload") &&
          !canAccess(permissions, "substitutions") && (
            <Link className="btn outline" to="/directories">
              Открыть справочники
            </Link>
          )}
      </div>

      <div className="kpi-grid">
        <div className="card kpi-card">
          <div>
            <div className="kpi-label">Импортировано УП</div>
            <div className="kpi-value">24</div>
            <div className="kpi-hint">18 готовы к нагрузке</div>
          </div>
          <div className="kpi-icon">
            <IconBook size={20} />
          </div>
        </div>
        <div className="card kpi-card">
          <div>
            <div className="kpi-label">Неполная нагрузка</div>
            <div className="kpi-value">6</div>
            <div className="kpi-hint">групп из 28</div>
          </div>
          <div className="kpi-icon warn">
            <IconPeople size={20} />
          </div>
        </div>
        <div className="card kpi-card">
          <div>
            <div className="kpi-label">Конфликты расписания</div>
            <div className="kpi-value">7</div>
            <div className="kpi-hint">требуют решения</div>
          </div>
          <div className="kpi-icon danger">
            <IconWarn size={20} />
          </div>
        </div>
        <div className="card kpi-card">
          <div>
            <div className="kpi-label">Отклонение факта</div>
            <div className="kpi-value">32 ч.</div>
            <div className="kpi-hint">за текущий месяц</div>
          </div>
          <div className="kpi-icon">
            <IconClock size={20} />
          </div>
        </div>
      </div>

      <div className="dashboard-bottom">
        <div className="card">
          <div className="ready-head">
            <h2>Готовность к новому семестру</h2>
            <div className="ready-pct">78%</div>
          </div>
          <div className="progress-list">
            <ProgressRow label="Учебные планы" value="18 из 24" pct={75} />
            <ProgressRow label="Распределение нагрузки" value="74 из 86" pct={86} />
            <ProgressRow label="Расписание" value="22 из 28 групп" pct={79} />
            <ProgressRow label="Сверка данных" value="19 из 24" pct={79} />
          </div>
        </div>

        <div className="card">
          <div className="attention-head">
            <h2>Требуют внимания</h2>
            <Link className="attention-link" to="/journal">
              Все задачи
            </Link>
          </div>
          <div className="attention-list">
            <div className="attention-item">
              <div className="attention-ico crit">
                <IconWarn size={18} />
              </div>
              <div>
                <div className="attention-title">Повреждён файл plan_09_02_07.plx</div>
                <div className="attention-sub">Импорт остановлен · требуется повторная загрузка</div>
              </div>
              <span className="badge badge-err">Критично</span>
            </div>
            <div className="attention-item">
              <div className="attention-ico today">
                <IconCalendar size={18} />
              </div>
              <div>
                <div className="attention-title">7 незакрытых конфликтов</div>
                <div className="attention-sub">Расписание · пересечения аудиторий и преподавателей</div>
              </div>
              <span className="badge badge-warn">Сегодня</span>
            </div>
            <div className="attention-item">
              <div className="attention-ico due">
                <IconClock size={18} />
              </div>
              <div>
                <div className="attention-title">3 ведомости не проверены</div>
                <div className="attention-sub">OCR-сверка журналов успеваемости</div>
              </div>
              <span className="badge badge-muted">до 22 мая</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function ProgressRow({ label, value, pct }: { label: string; value: string; pct: number }) {
  return (
    <div className="progress-row">
      <div className="progress-meta">
        <span>{label}</span>
        <span>{value}</span>
      </div>
      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
