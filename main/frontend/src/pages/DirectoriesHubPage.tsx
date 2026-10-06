import { useEffect, useState, type ReactNode } from "react";
import { Link } from "react-router-dom";
import { apiGet, type DirectorySummary } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { canEditDirectories } from "../auth/roles";
import {
  IconArchive,
  IconBook,
  IconChevron,
  IconClock,
  IconGrid,
  IconHouse,
  IconPeople,
  IconPlus,
} from "../components/Icons";

type DirCard = {
  to: string;
  title: string;
  countKey: keyof DirectorySummary;
  icon: ReactNode;
};

function pluralRecords(n: number): string {
  const mod10 = n % 10;
  const mod100 = n % 100;
  if (mod10 === 1 && mod100 !== 11) return `${n} запись`;
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 10 || mod100 >= 20)) return `${n} записи`;
  return `${n} записей`;
}

const CARDS: DirCard[] = [
  { to: "/directories/specialties", title: "Специальности", countKey: "specialties", icon: <IconBook size={22} /> },
  { to: "/directories/subjects", title: "Дисциплины", countKey: "subjects", icon: <IconArchive size={22} /> },
  { to: "/directories/teachers", title: "Преподаватели", countKey: "teachers", icon: <IconPeople size={22} /> },
  { to: "/directories/groups", title: "Группы", countKey: "groups", icon: <IconGrid size={22} /> },
  { to: "/directories/classrooms", title: "Аудитории", countKey: "classrooms", icon: <IconHouse size={22} /> },
  { to: "/directories/lesson-types", title: "Виды занятий", countKey: "lesson_types", icon: <IconClock size={22} /> },
];

export function DirectoriesHubPage() {
  const { session } = useAuth();
  const canEdit = canEditDirectories(session?.role);
  const [summary, setSummary] = useState<DirectorySummary | null>(null);

  useEffect(() => {
    let cancelled = false;
    apiGet<DirectorySummary>("/directories/summary")
      .then((data) => {
        if (!cancelled) setSummary(data);
      })
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <section>
      <div className="breadcrumbs">
        <span>Учебное планирование</span>
        <span>›</span>
        <strong>Справочники</strong>
      </div>

      <header className="page-header">
        <div>
          <h1>Справочники</h1>
          <p className="muted">Единые нормативные данные учебного процесса</p>
        </div>
        {canEdit ? (
          <Link className="btn primary" to="/directories/groups?new=1">
            <IconPlus size={16} />
            Создать запись
          </Link>
        ) : null}
      </header>

      <div className="dir-grid">
        {CARDS.map((card) => {
          const count = summary?.[card.countKey];
          return (
            <Link key={card.to} to={card.to} className="dir-card">
              <span className="dir-card-ico">{card.icon}</span>
              <span className="dir-card-body">
                <span className="dir-card-title">{card.title}</span>
                <span className="dir-card-count">
                  {count === undefined ? "…" : pluralRecords(count)}
                </span>
              </span>
              <span className="dir-card-chevron">
                <IconChevron size={18} />
              </span>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
