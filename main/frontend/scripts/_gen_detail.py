# -*- coding: utf-8 -*-
from pathlib import Path

pages = Path(__file__).resolve().parents[1] / "src" / "pages"
old = (pages / "DirectoriesPage.tsx").read_text(encoding="utf-8")
idx = old.find("function GroupsPanel")
assert idx > 0, "panels not found"
panels = old[idx:]

head = r'''import { FormEvent, useCallback, useEffect, useState } from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import {
  apiDelete,
  apiGet,
  apiPatch,
  apiPost,
  type Classroom,
  type LessonType,
  type Specialty,
  type StudyGroup,
  type Subject,
  type Teacher,
} from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { canEditDirectories } from "../auth/roles";
import { PageHeader } from "../components/PageHeader";

export type DirKind =
  | "groups"
  | "teachers"
  | "classrooms"
  | "subjects"
  | "specialties"
  | "lesson-types";

const LABELS: Record<DirKind, string> = {
  groups: "Группы",
  teachers: "Преподаватели",
  classrooms: "Аудитории",
  subjects: "Дисциплины",
  specialties: "Специальности",
  "lesson-types": "Виды занятий",
};

const VALID = new Set<string>(Object.keys(LABELS));

export function DirectoryDetailPage() {
  const { kind: rawKind } = useParams<{ kind: string }>();
  const invalid = !VALID.has(rawKind || "");
  const kind = (invalid ? "groups" : rawKind) as DirKind;
  const { session } = useAuth();
  const canEdit = canEditDirectories(session?.role);
  const [error, setError] = useState<string | null>(null);
  const [groups, setGroups] = useState<StudyGroup[]>([]);
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [specialties, setSpecialties] = useState<Specialty[]>([]);
  const [lessonTypes, setLessonTypes] = useState<LessonType[]>([]);
  const [loading, setLoading] = useState(false);

  const reload = useCallback(async () => {
    if (invalid) return;
    setLoading(true);
    setError(null);
    try {
      if (kind === "groups") setGroups(await apiGet<StudyGroup[]>("/directories/groups"));
      if (kind === "teachers") setTeachers(await apiGet<Teacher[]>("/directories/teachers"));
      if (kind === "classrooms") setClassrooms(await apiGet<Classroom[]>("/directories/classrooms"));
      if (kind === "subjects") setSubjects(await apiGet<Subject[]>("/directories/subjects"));
      if (kind === "specialties") setSpecialties(await apiGet<Specialty[]>("/directories/specialties"));
      if (kind === "lesson-types") setLessonTypes(await apiGet<LessonType[]>("/directories/lesson-types"));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка загрузки");
    } finally {
      setLoading(false);
    }
  }, [kind, invalid]);

  useEffect(() => {
    void reload();
  }, [reload]);

  if (invalid) {
    return <Navigate to="/directories" replace />;
  }

  async function remove(apiKind: string, id: number) {
    if (!canEdit) return;
    if (!window.confirm("Удалить запись?")) return;
    try {
      await apiDelete(`/directories/${apiKind}/${id}`);
      await reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка удаления");
    }
  }

  return (
    <section className="directories-page">
      <Link className="back-link" to="/directories">
        ← Все справочники
      </Link>
      <div className="breadcrumbs">
        <span>Учебное планирование</span>
        <span>›</span>
        <Link to="/directories">Справочники</Link>
        <span>›</span>
        <strong>{LABELS[kind]}</strong>
      </div>
      <PageHeader
        title={LABELS[kind]}
        subtitle={
          canEdit
            ? "Просмотр и редактирование записей справочника"
            : "Просмотр справочника (редактирование — методист и администратор)"
        }
      />

      {error ? <div className="form-alert" style={{ marginBottom: 12 }}>{error}</div> : null}
      {loading ? <p className="muted">Загрузка…</p> : null}

      {kind === "groups" && (
        <GroupsPanel items={groups} canEdit={canEdit} onCreated={reload} onDelete={(id) => remove("groups", id)} />
      )}
      {kind === "teachers" && (
        <TeachersPanel items={teachers} canEdit={canEdit} onCreated={reload} onDelete={(id) => remove("teachers", id)} />
      )}
      {kind === "classrooms" && (
        <ClassroomsPanel items={classrooms} canEdit={canEdit} onCreated={reload} onDelete={(id) => remove("classrooms", id)} />
      )}
      {kind === "subjects" && (
        <SubjectsPanel items={subjects} canEdit={canEdit} onCreated={reload} onDelete={(id) => remove("subjects", id)} />
      )}
      {kind === "specialties" && (
        <SimpleCodeTitlePanel
          title="Добавить специальность"
          endpoint="/directories/specialties"
          items={specialties}
          canEdit={canEdit}
          onCreated={reload}
          onDelete={(id) => remove("specialties", id)}
          emptyText="Нет специальностей"
        />
      )}
      {kind === "lesson-types" && (
        <SimpleCodeTitlePanel
          title="Добавить вид занятий"
          endpoint="/directories/lesson-types"
          items={lessonTypes}
          canEdit={canEdit}
          onCreated={reload}
          onDelete={(id) => remove("lesson-types", id)}
          emptyText="Нет видов занятий"
        />
      )}
    </section>
  );
}

'''

extra = r'''

function SimpleCodeTitlePanel({
  title,
  endpoint,
  items,
  canEdit,
  onCreated,
  onDelete,
  emptyText,
}: {
  title: string;
  endpoint: string;
  items: { id: number; code: string; title: string; is_active: boolean }[];
  canEdit: boolean;
  onCreated: () => Promise<void>;
  onDelete: (id: number) => void;
  emptyText: string;
}) {
  const [code, setCode] = useState("");
  const [itemTitle, setItemTitle] = useState("");
  const [busy, setBusy] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!canEdit) return;
    setBusy(true);
    setFormError(null);
    try {
      await apiPost(endpoint, { code: code.trim(), title: itemTitle.trim() });
      setCode("");
      setItemTitle("");
      await onCreated();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setBusy(false);
    }
  }

  return (
    <>
      {canEdit ? (
        <form className="card inline-form" onSubmit={onSubmit}>
          <h2>{title}</h2>
          <div className="form-row">
            <input placeholder="Код" value={code} onChange={(e) => setCode(e.target.value)} required />
            <input placeholder="Название" value={itemTitle} onChange={(e) => setItemTitle(e.target.value)} required />
            <button className="btn primary" type="submit" disabled={busy}>
              Добавить
            </button>
          </div>
          {formError ? <p className="err-text">{formError}</p> : null}
        </form>
      ) : null}
      <div className="card table-wrap" style={{ marginTop: 12 }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Код</th>
              <th>Название</th>
              <th>Статус</th>
              {canEdit ? <th></th> : null}
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan={canEdit ? 4 : 3} className="muted">
                  {emptyText}
                </td>
              </tr>
            ) : (
              items.map((row) => (
                <tr key={row.id}>
                  <td>{row.code}</td>
                  <td>{row.title}</td>
                  <td>{row.is_active ? "активен" : "скрыт"}</td>
                  {canEdit ? (
                    <td>
                      <button type="button" className="btn ghost" onClick={() => onDelete(row.id)}>
                        Удалить
                      </button>
                    </td>
                  ) : null}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
'''

(pages / "DirectoryDetailPage.tsx").write_text(head + panels + extra, encoding="utf-8")
(pages / "DirectoriesPage.tsx").write_text(
    'export { DirectoriesHubPage as DirectoriesPage } from "./DirectoriesHubPage";\n',
    encoding="utf-8",
)
print("written", (pages / "DirectoryDetailPage.tsx").stat().st_size)
