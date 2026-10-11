export function formatArcTime(value?: string | Date | null) {
  if (!value) return "";
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return "";

  const deltaMs = Date.now() - date.getTime();
  const deltaSeconds = Math.max(0, Math.floor(deltaMs / 1000));
  if (deltaSeconds < 60) return `${deltaSeconds} ${plural("second", deltaSeconds)} ago`;

  const deltaMinutes = Math.floor(deltaSeconds / 60);
  if (deltaMinutes < 60) return `${deltaMinutes} ${plural("minute", deltaMinutes)} ago`;

  const deltaHours = deltaMs / (1000 * 60 * 60);
  if (deltaHours < 24) {
    return new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit" }).format(date);
  }

  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit"
  }).format(date);
}

export function formatArcDuration(start?: string | null, end?: string | null) {
  if (!start) return "";
  const startedAt = new Date(start);
  const endedAt = end ? new Date(end) : new Date();
  if (Number.isNaN(startedAt.getTime()) || Number.isNaN(endedAt.getTime())) return "";

  const totalSeconds = Math.max(0, Math.floor((endedAt.getTime() - startedAt.getTime()) / 1000));
  if (totalSeconds < 60) return `${totalSeconds}s`;

  const totalMinutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  if (totalMinutes < 60) return seconds ? `${totalMinutes}m ${seconds}s` : `${totalMinutes}m`;

  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return minutes ? `${hours}h ${minutes}m` : `${hours}h`;
}

export function formatBytes(value?: number | null) {
  if (!value) return "";
  if (value < 1000) return `${value} B`;
  if (value < 1_000_000) return `${(value / 1000).toFixed(1)} KB`;
  if (value < 1_000_000_000) return `${(value / 1_000_000).toFixed(1)} MB`;
  return `${(value / 1_000_000_000).toFixed(1)} GB`;
}

export function shortId(id?: string | null, length = 8) {
  return id ? id.slice(0, length) : "";
}

export function fileName(path: string) {
  return path.split("/").pop() ?? path;
}

function plural(word: string, count: number) {
  return count === 1 ? word : `${word}s`;
}
