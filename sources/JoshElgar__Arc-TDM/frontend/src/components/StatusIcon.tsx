import { AppIcon } from "./AppIcon";

type StatusKind = "success" | "error" | "running" | "pending" | "inactive" | "unknown";

type StatusIconProps = {
  status?: string | null;
  label?: string;
  size?: number;
};

export function StatusIcon({ status, label, size = 16 }: StatusIconProps) {
  const kind = statusKind(status);
  const title = label ?? statusLabel(status, kind);
  const iconName =
    kind === "success"
      ? "check"
      : kind === "error"
        ? "cross"
        : kind === "running"
          ? "spinner"
          : kind === "pending"
            ? "clock"
            : "dot";

  return (
    <span aria-label={title} className={`status-icon ${kind}`} role="img" title={title}>
      <AppIcon name={iconName} size={size} />
    </span>
  );
}

export function statusKind(status?: string | null): StatusKind {
  const value = (status ?? "").toLowerCase();
  if (["completed", "complete", "success", "succeeded", "ready", "current"].includes(value)) {
    return "success";
  }
  if (["failed", "failure", "error", "invalid"].includes(value)) return "error";
  if (["running", "starting", "in_progress"].includes(value)) return "running";
  if (["blocked", "queued", "pending", "waiting"].includes(value)) return "pending";
  if (["inactive", "stale", "older"].includes(value)) return "inactive";
  return "unknown";
}

function statusLabel(status: string | null | undefined, kind: StatusKind) {
  if (status) return status.replace(/[_-]+/g, " ");
  return kind;
}
