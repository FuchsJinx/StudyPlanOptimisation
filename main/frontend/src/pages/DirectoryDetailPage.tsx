import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { Link, Navigate, useParams, useSearchParams } from "react-router-dom";
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
import { ConfirmDialog, Modal } from "../components/ConfirmDialog";
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
const EDU_FORMS = [
  { value: "О", label: "Очная" },
  { value: "З", label: "Заочная" },
  { value: "ОЗ", label: "Очно-заочная" },
];
const SUBJECT_CYCLES = ["ОГСЭ", "ЕН", "ОП", "ПМ", "УП", "ПП", "ГИА"];
const ROOM_TYPES_FALLBACK = ["лекция", "практика", "компьютерный", "лаборатория", "спортзал"];

type DeleteTarget = { id: number; label: string } | null;

export function DirectoryDetailPage() {
  const { kind: rawKind } = useParams<{ kind: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const invalid = !VALID.has(rawKind || "");
  const kind = (invalid ? "groups" : rawKind) as DirKind;
  const { session } = useAuth();
  const canEdit = canEditDirectories(session?.role);

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [groups, setGroups] = useState<StudyGroup[]>([]);
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [specialties, setSpecialties] = useState<Specialty[]>([]);
  const [lessonTypes, setLessonTypes] = useState<LessonType[]>([]);

  const [editorOpen, setEditorOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<DeleteTarget>(null);
  const [deleteBusy, setDeleteBusy] = useState(false);

  const reload = useCallback(async () => {
    if (invalid) return;
    setLoading(true);
    setError(null);
    try {
      const [specs, types] = await Promise.all([
        apiGet<Specialty[]>("/directories/specialties"),
        apiGet<LessonType[]>("/directories/lesson-types"),
      ]);
      setSpecialties(specs);
      setLessonTypes(types);
      if (kind === "groups") setGroups(await apiGet<StudyGroup[]>("/directories/groups"));
      if (kind === "teachers") setTeachers(await apiGet<Teacher[]>("/directories/teachers"));
      if (kind === "classrooms") setClassrooms(await apiGet<Classroom[]>("/directories/classrooms"));
      if (kind === "subjects") setSubjects(await apiGet<Subject[]>("/directories/subjects"));
      if (kind === "specialties") setSpecialties(specs);
      if (kind === "lesson-types") setLessonTypes(types);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка загрузки");
    } finally {
      setLoading(false);
    }
  }, [kind, invalid]);

  useEffect(() => {
    void reload();
  }, [reload]);

  useEffect(() => {
    if (searchParams.get("new") === "1" && canEdit) {
      setEditingId(null);
      setEditorOpen(true);
      searchParams.delete("new");
      setSearchParams(searchParams, { replace: true });
    }
  }, [searchParams, setSearchParams, canEdit]);

  if (invalid) return <Navigate to="/directories" replace />;

  function openCreate() {
    setEditingId(null);
    setEditorOpen(true);
  }

  function openEdit(id: number) {
    setEditingId(id);
    setEditorOpen(true);
  }

  async function confirmDelete() {
    if (!deleteTarget) return;
    setDeleteBusy(true);
    try {
      await apiDelete(`/directories/${kind}/${deleteTarget.id}`);
      setDeleteTarget(null);
      await reload();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка удаления");
      setDeleteTarget(null);
    } finally {
      setDeleteBusy(false);
    }
  }

  const roomTypeOptions = useMemo(() => {
    const fromTypes = lessonTypes.map((t) => t.title.toLowerCase());
    const fromRooms = classrooms.map((c) => (c.room_type || "").toLowerCase()).filter(Boolean);
    return Array.from(new Set([...ROOM_TYPES_FALLBACK, ...fromTypes, ...fromRooms]));
  }, [lessonTypes, classrooms]);

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
            ? "Откройте запись для просмотра и редактирования"
            : "Просмотр справочника (редактирование — методист и администратор)"
        }
        actions={
          canEdit ? (
            <button type="button" className="btn primary" onClick={openCreate}>
              + Добавить
            </button>
          ) : null
        }
      />

      {error ? <div className="form-alert" style={{ marginBottom: 12 }}>{error}</div> : null}
      {loading ? <p className="muted">Загрузка…</p> : null}

      {kind === "groups" && (
        <DataTable
          empty="Нет групп"
          columns={["Код", "Численность", "Форма", "Специальность", "Год", "Статус"]}
          rows={groups.map((g) => ({
            id: g.id,
            label: g.code,
            cells: [
              g.code,
              g.size ?? "—",
              g.education_form,
              specialtyLabel(specialties, g.specialty_code),
              g.study_year ?? "—",
              g.is_active ? "активна" : "скрыта",
            ],
          }))}
          canEdit={canEdit}
          onOpen={openEdit}
          onDelete={(id, label) => setDeleteTarget({ id, label })}
        />
      )}
      {kind === "teachers" && (
        <DataTable
          empty="Нет преподавателей"
          columns={["ФИО", "Ставка", "Бюджет", "Контакты", "Статус"]}
          rows={teachers.map((t) => ({
            id: t.id,
            label: t.full_name,
            cells: [
              t.full_name,
              t.rate ?? "—",
              t.budget_flag ? "да" : "нет",
              t.contacts ?? "—",
              t.is_active ? "активен" : "скрыт",
            ],
          }))}
          canEdit={canEdit}
          onOpen={openEdit}
          onDelete={(id, label) => setDeleteTarget({ id, label })}
        />
      )}
      {kind === "classrooms" && (
        <DataTable
          empty="Нет аудиторий"
          columns={["Код", "Вместимость", "Корпус", "Тип", "Статус"]}
          rows={classrooms.map((c) => ({
            id: c.id,
            label: c.code,
            cells: [
              c.code,
              c.capacity ?? "—",
              c.building ?? "—",
              c.room_type ?? "—",
              c.is_active ? "активен" : "скрыт",
            ],
          }))}
          canEdit={canEdit}
          onOpen={openEdit}
          onDelete={(id, label) => setDeleteTarget({ id, label })}
        />
      )}
      {kind === "subjects" && (
        <DataTable
          empty="Нет дисциплин"
          columns={["Код", "Название", "Кратко", "Цикл", "Статус"]}
          rows={subjects.map((s) => ({
            id: s.id,
            label: s.title,
            cells: [
              s.code,
              s.title,
              s.short_title ?? "—",
              s.cycle ?? "—",
              s.is_active ? "активен" : "скрыт",
            ],
          }))}
          canEdit={canEdit}
          onOpen={openEdit}
          onDelete={(id, label) => setDeleteTarget({ id, label })}
        />
      )}
      {kind === "specialties" && (
        <DataTable
          empty="Нет специальностей"
          columns={["Код", "Название", "Статус"]}
          rows={specialties.map((s) => ({
            id: s.id,
            label: s.title,
            cells: [s.code, s.title, s.is_active ? "активен" : "скрыт"],
          }))}
          canEdit={canEdit}
          onOpen={openEdit}
          onDelete={(id, label) => setDeleteTarget({ id, label })}
        />
      )}
      {kind === "lesson-types" && (
        <DataTable
          empty="Нет видов занятий"
          columns={["Код", "Название", "Статус"]}
          rows={lessonTypes.map((s) => ({
            id: s.id,
            label: s.title,
            cells: [s.code, s.title, s.is_active ? "активен" : "скрыт"],
          }))}
          canEdit={canEdit}
          onOpen={openEdit}
          onDelete={(id, label) => setDeleteTarget({ id, label })}
        />
      )}

      <RecordEditor
        open={editorOpen}
        kind={kind}
        editingId={editingId}
        canEdit={canEdit}
        groups={groups}
        teachers={teachers}
        classrooms={classrooms}
        subjects={subjects}
        specialties={specialties}
        lessonTypes={lessonTypes}
        roomTypeOptions={roomTypeOptions}
        onClose={() => setEditorOpen(false)}
        onSaved={async () => {
          setEditorOpen(false);
          await reload();
        }}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="Удаление записи"
        message={
          deleteTarget
            ? `Удалить «${deleteTarget.label}» из справочника «${LABELS[kind]}»? Действие нельзя отменить.`
            : ""
        }
        busy={deleteBusy}
        onCancel={() => setDeleteTarget(null)}
        onConfirm={() => void confirmDelete()}
      />
    </section>
  );
}

function specialtyLabel(list: Specialty[], code: string | null): string {
  if (!code) return "—";
  const found = list.find((s) => s.code === code);
  return found ? `${found.code} — ${found.title}` : code;
}

function DataTable({
  columns,
  rows,
  empty,
  canEdit,
  onOpen,
  onDelete,
}: {
  columns: string[];
  rows: { id: number; label: string; cells: Array<string | number> }[];
  empty: string;
  canEdit: boolean;
  onOpen: (id: number) => void;
  onDelete: (id: number, label: string) => void;
}) {
  return (
    <div className="card table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c}>{c}</th>
            ))}
            <th></th>
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr>
              <td colSpan={columns.length + 1} className="muted">
                {empty}
              </td>
            </tr>
          ) : (
            rows.map((row) => (
              <tr key={row.id} className="row-clickable" onClick={() => onOpen(row.id)}>
                {row.cells.map((cell, idx) => (
                  <td key={idx}>{cell}</td>
                ))}
                <td onClick={(e) => e.stopPropagation()}>
                  <div className="row-actions">
                    <button type="button" className="btn ghost" onClick={() => onOpen(row.id)}>
                      {canEdit ? "Изменить" : "Открыть"}
                    </button>
                    {canEdit ? (
                      <button
                        type="button"
                        className="btn ghost"
                        onClick={() => onDelete(row.id, row.label)}
                      >
                        Удалить
                      </button>
                    ) : null}
                  </div>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

function RecordEditor({
  open,
  kind,
  editingId,
  canEdit,
  groups,
  teachers,
  classrooms,
  subjects,
  specialties,
  lessonTypes,
  roomTypeOptions,
  onClose,
  onSaved,
}: {
  open: boolean;
  kind: DirKind;
  editingId: number | null;
  canEdit: boolean;
  groups: StudyGroup[];
  teachers: Teacher[];
  classrooms: Classroom[];
  subjects: Subject[];
  specialties: Specialty[];
  lessonTypes: LessonType[];
  roomTypeOptions: string[];
  onClose: () => void;
  onSaved: () => Promise<void>;
}) {
  const isNew = editingId == null;
  const title = `${isNew ? "Создание" : canEdit ? "Редактирование" : "Просмотр"}: ${LABELS[kind]}`;

  if (kind === "groups") {
    const item = groups.find((g) => g.id === editingId) || null;
    return (
      <GroupForm
        open={open}
        title={title}
        item={item}
        canEdit={canEdit}
        specialties={specialties}
        onClose={onClose}
        onSaved={onSaved}
      />
    );
  }
  if (kind === "teachers") {
    const item = teachers.find((t) => t.id === editingId) || null;
    return (
      <TeacherForm open={open} title={title} item={item} canEdit={canEdit} onClose={onClose} onSaved={onSaved} />
    );
  }
  if (kind === "classrooms") {
    const item = classrooms.find((c) => c.id === editingId) || null;
    return (
      <ClassroomForm
        open={open}
        title={title}
        item={item}
        canEdit={canEdit}
        roomTypeOptions={roomTypeOptions}
        onClose={onClose}
        onSaved={onSaved}
      />
    );
  }
  if (kind === "subjects") {
    const item = subjects.find((s) => s.id === editingId) || null;
    return (
      <SubjectForm open={open} title={title} item={item} canEdit={canEdit} onClose={onClose} onSaved={onSaved} />
    );
  }
  if (kind === "specialties") {
    const item = specialties.find((s) => s.id === editingId) || null;
    return (
      <CodeTitleForm
        open={open}
        title={title}
        item={item}
        canEdit={canEdit}
        endpoint="/directories/specialties"
        onClose={onClose}
        onSaved={onSaved}
      />
    );
  }
  const item = lessonTypes.find((s) => s.id === editingId) || null;
  return (
    <CodeTitleForm
      open={open}
      title={title}
      item={item}
      canEdit={canEdit}
      endpoint="/directories/lesson-types"
      onClose={onClose}
      onSaved={onSaved}
    />
  );
}

function GroupForm({
  open,
  title,
  item,
  canEdit,
  specialties,
  onClose,
  onSaved,
}: {
  open: boolean;
  title: string;
  item: StudyGroup | null;
  canEdit: boolean;
  specialties: Specialty[];
  onClose: () => void;
  onSaved: () => Promise<void>;
}) {
  const [code, setCode] = useState("");
  const [size, setSize] = useState("");
  const [form, setForm] = useState("О");
  const [specialty, setSpecialty] = useState("");
  const [year, setYear] = useState("");
  const [active, setActive] = useState(true);
  const [busy, setBusy] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setCode(item?.code ?? "");
    setSize(item?.size != null ? String(item.size) : "");
    setForm(item?.education_form || "О");
    setSpecialty(item?.specialty_code || "");
    setYear(item?.study_year != null ? String(item.study_year) : "");
    setActive(item?.is_active ?? true);
    setFormError(null);
  }, [open, item]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!canEdit) return;
    setBusy(true);
    setFormError(null);
    const body = {
      code: code.trim(),
      size: size ? Number(size) : null,
      education_form: form,
      specialty_code: specialty || null,
      study_year: year ? Number(year) : null,
      is_active: active,
    };
    try {
      if (item) await apiPatch(`/directories/groups/${item.id}`, body);
      else await apiPost("/directories/groups", body);
      await onSaved();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal
      open={open}
      title={title}
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn outline" onClick={onClose}>
            Закрыть
          </button>
          {canEdit ? (
            <button type="submit" form="group-form" className="btn primary" disabled={busy}>
              {busy ? "Сохранение…" : "Сохранить"}
            </button>
          ) : null}
        </>
      }
    >
      <form id="group-form" className="editor-grid" onSubmit={onSubmit}>
        <label className="field">
          <span>Код группы</span>
          <input value={code} onChange={(e) => setCode(e.target.value)} required disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Численность</span>
          <input type="number" min={1} value={size} onChange={(e) => setSize(e.target.value)} disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Форма обучения</span>
          <select value={form} onChange={(e) => setForm(e.target.value)} disabled={!canEdit}>
            {EDU_FORMS.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </label>
        <label className="field">
          <span>Специальность</span>
          <select value={specialty} onChange={(e) => setSpecialty(e.target.value)} disabled={!canEdit}>
            <option value="">— не выбрана —</option>
            {specialties.map((s) => (
              <option key={s.id} value={s.code}>
                {s.code} — {s.title}
              </option>
            ))}
          </select>
        </label>
        <label className="field">
          <span>Учебный год набора</span>
          <input type="number" value={year} onChange={(e) => setYear(e.target.value)} disabled={!canEdit} />
        </label>
        {item ? (
          <label className="field checkbox-field">
            <span>Активна</span>
            <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} disabled={!canEdit} />
          </label>
        ) : null}
        {formError ? <div className="form-alert">{formError}</div> : null}
      </form>
    </Modal>
  );
}

function TeacherForm({
  open,
  title,
  item,
  canEdit,
  onClose,
  onSaved,
}: {
  open: boolean;
  title: string;
  item: Teacher | null;
  canEdit: boolean;
  onClose: () => void;
  onSaved: () => Promise<void>;
}) {
  const [fullName, setFullName] = useState("");
  const [rate, setRate] = useState("1");
  const [budget, setBudget] = useState(true);
  const [contacts, setContacts] = useState("");
  const [active, setActive] = useState(true);
  const [busy, setBusy] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setFullName(item?.full_name ?? "");
    setRate(item?.rate != null ? String(item.rate) : "1");
    setBudget(item?.budget_flag ?? true);
    setContacts(item?.contacts ?? "");
    setActive(item?.is_active ?? true);
    setFormError(null);
  }, [open, item]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!canEdit) return;
    setBusy(true);
    setFormError(null);
    const body = {
      full_name: fullName.trim(),
      rate: rate ? Number(rate) : null,
      budget_flag: budget,
      contacts: contacts.trim() || null,
      is_active: active,
    };
    try {
      if (item) await apiPatch(`/directories/teachers/${item.id}`, body);
      else await apiPost("/directories/teachers", body);
      await onSaved();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal
      open={open}
      title={title}
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn outline" onClick={onClose}>
            Закрыть
          </button>
          {canEdit ? (
            <button type="submit" form="teacher-form" className="btn primary" disabled={busy}>
              {busy ? "Сохранение…" : "Сохранить"}
            </button>
          ) : null}
        </>
      }
    >
      <form id="teacher-form" className="editor-grid" onSubmit={onSubmit}>
        <label className="field">
          <span>ФИО</span>
          <input value={fullName} onChange={(e) => setFullName(e.target.value)} required disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Ставка</span>
          <select value={rate} onChange={(e) => setRate(e.target.value)} disabled={!canEdit}>
            {["0.25", "0.5", "0.75", "1", "1.25", "1.5"].map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </label>
        <label className="field checkbox-field">
          <span>Бюджет</span>
          <input type="checkbox" checked={budget} onChange={(e) => setBudget(e.target.checked)} disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Контакты</span>
          <input value={contacts} onChange={(e) => setContacts(e.target.value)} disabled={!canEdit} />
        </label>
        {item ? (
          <label className="field checkbox-field">
            <span>Активен</span>
            <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} disabled={!canEdit} />
          </label>
        ) : null}
        {formError ? <div className="form-alert">{formError}</div> : null}
      </form>
    </Modal>
  );
}

function ClassroomForm({
  open,
  title,
  item,
  canEdit,
  roomTypeOptions,
  onClose,
  onSaved,
}: {
  open: boolean;
  title: string;
  item: Classroom | null;
  canEdit: boolean;
  roomTypeOptions: string[];
  onClose: () => void;
  onSaved: () => Promise<void>;
}) {
  const [code, setCode] = useState("");
  const [capacity, setCapacity] = useState("");
  const [building, setBuilding] = useState("");
  const [roomType, setRoomType] = useState("");
  const [active, setActive] = useState(true);
  const [busy, setBusy] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setCode(item?.code ?? "");
    setCapacity(item?.capacity != null ? String(item.capacity) : "");
    setBuilding(item?.building ?? "");
    setRoomType(item?.room_type ?? "");
    setActive(item?.is_active ?? true);
    setFormError(null);
  }, [open, item]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!canEdit) return;
    setBusy(true);
    setFormError(null);
    const body = {
      code: code.trim(),
      capacity: capacity ? Number(capacity) : null,
      building: building.trim() || null,
      room_type: roomType || null,
      is_active: active,
    };
    try {
      if (item) await apiPatch(`/directories/classrooms/${item.id}`, body);
      else await apiPost("/directories/classrooms", body);
      await onSaved();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal
      open={open}
      title={title}
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn outline" onClick={onClose}>
            Закрыть
          </button>
          {canEdit ? (
            <button type="submit" form="room-form" className="btn primary" disabled={busy}>
              {busy ? "Сохранение…" : "Сохранить"}
            </button>
          ) : null}
        </>
      }
    >
      <form id="room-form" className="editor-grid" onSubmit={onSubmit}>
        <label className="field">
          <span>Номер / код</span>
          <input value={code} onChange={(e) => setCode(e.target.value)} required disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Вместимость</span>
          <input type="number" min={1} value={capacity} onChange={(e) => setCapacity(e.target.value)} disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Корпус</span>
          <input value={building} onChange={(e) => setBuilding(e.target.value)} disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Тип аудитории</span>
          <select value={roomType} onChange={(e) => setRoomType(e.target.value)} disabled={!canEdit}>
            <option value="">— не выбран —</option>
            {roomTypeOptions.map((opt) => (
              <option key={opt} value={opt}>
                {opt}
              </option>
            ))}
          </select>
        </label>
        {item ? (
          <label className="field checkbox-field">
            <span>Активна</span>
            <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} disabled={!canEdit} />
          </label>
        ) : null}
        {formError ? <div className="form-alert">{formError}</div> : null}
      </form>
    </Modal>
  );
}

function SubjectForm({
  open,
  title,
  item,
  canEdit,
  onClose,
  onSaved,
}: {
  open: boolean;
  title: string;
  item: Subject | null;
  canEdit: boolean;
  onClose: () => void;
  onSaved: () => Promise<void>;
}) {
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [shortTitle, setShortTitle] = useState("");
  const [cycle, setCycle] = useState("");
  const [active, setActive] = useState(true);
  const [busy, setBusy] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setCode(item?.code ?? "");
    setName(item?.title ?? "");
    setShortTitle(item?.short_title ?? "");
    setCycle(item?.cycle ?? "");
    setActive(item?.is_active ?? true);
    setFormError(null);
  }, [open, item]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!canEdit) return;
    setBusy(true);
    setFormError(null);
    const body = {
      code: code.trim(),
      title: name.trim(),
      short_title: shortTitle.trim() || null,
      cycle: cycle || null,
      is_active: active,
    };
    try {
      if (item) await apiPatch(`/directories/subjects/${item.id}`, body);
      else await apiPost("/directories/subjects", body);
      await onSaved();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal
      open={open}
      title={title}
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn outline" onClick={onClose}>
            Закрыть
          </button>
          {canEdit ? (
            <button type="submit" form="subject-form" className="btn primary" disabled={busy}>
              {busy ? "Сохранение…" : "Сохранить"}
            </button>
          ) : null}
        </>
      }
    >
      <form id="subject-form" className="editor-grid" onSubmit={onSubmit}>
        <label className="field">
          <span>Код</span>
          <input value={code} onChange={(e) => setCode(e.target.value)} required disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Название</span>
          <input value={name} onChange={(e) => setName(e.target.value)} required disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Краткое название</span>
          <input value={shortTitle} onChange={(e) => setShortTitle(e.target.value)} disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Цикл</span>
          <select value={cycle} onChange={(e) => setCycle(e.target.value)} disabled={!canEdit}>
            <option value="">— не выбран —</option>
            {SUBJECT_CYCLES.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </label>
        {item ? (
          <label className="field checkbox-field">
            <span>Активна</span>
            <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} disabled={!canEdit} />
          </label>
        ) : null}
        {formError ? <div className="form-alert">{formError}</div> : null}
      </form>
    </Modal>
  );
}

function CodeTitleForm({
  open,
  title,
  item,
  canEdit,
  endpoint,
  onClose,
  onSaved,
}: {
  open: boolean;
  title: string;
  item: { id: number; code: string; title: string; is_active: boolean } | null;
  canEdit: boolean;
  endpoint: string;
  onClose: () => void;
  onSaved: () => Promise<void>;
}) {
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [active, setActive] = useState(true);
  const [busy, setBusy] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    if (!open) return;
    setCode(item?.code ?? "");
    setName(item?.title ?? "");
    setActive(item?.is_active ?? true);
    setFormError(null);
  }, [open, item]);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!canEdit) return;
    setBusy(true);
    setFormError(null);
    const body = { code: code.trim(), title: name.trim(), is_active: active };
    try {
      if (item) await apiPatch(`${endpoint}/${item.id}`, body);
      else await apiPost(endpoint, body);
      await onSaved();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Ошибка");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Modal
      open={open}
      title={title}
      onClose={onClose}
      footer={
        <>
          <button type="button" className="btn outline" onClick={onClose}>
            Закрыть
          </button>
          {canEdit ? (
            <button type="submit" form="code-title-form" className="btn primary" disabled={busy}>
              {busy ? "Сохранение…" : "Сохранить"}
            </button>
          ) : null}
        </>
      }
    >
      <form id="code-title-form" className="editor-grid" onSubmit={onSubmit}>
        <label className="field">
          <span>Код</span>
          <input value={code} onChange={(e) => setCode(e.target.value)} required disabled={!canEdit} />
        </label>
        <label className="field">
          <span>Название</span>
          <input value={name} onChange={(e) => setName(e.target.value)} required disabled={!canEdit} />
        </label>
        {item ? (
          <label className="field checkbox-field">
            <span>Активна</span>
            <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} disabled={!canEdit} />
          </label>
        ) : null}
        {formError ? <div className="form-alert">{formError}</div> : null}
      </form>
    </Modal>
  );
}
