type Props = {
  status: string;
};

const MAP: Record<string, string> = {
  imported: "ok",
  warning: "warn",
  error: "err",
  draft: "muted",
  ok: "ok",
};

export function StatusBadge({ status }: Props) {
  const kind = MAP[status] ?? "muted";
  return <span className={`badge badge-${kind}`}>{status}</span>;
}
