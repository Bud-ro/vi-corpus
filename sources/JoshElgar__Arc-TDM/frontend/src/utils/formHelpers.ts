export function slugify(value: string) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function parseCommaList(value: string) {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

export function parseProperties(value: string) {
  const trimmed = value.trim();
  if (!trimmed) return {};
  const parsed = JSON.parse(trimmed) as unknown;
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
    throw new Error("Properties must be a JSON object.");
  }
  return Object.fromEntries(
    Object.entries(parsed).map(([key, item]) => [key, String(item)])
  );
}

export function formatProperties(properties: Record<string, string>) {
  return Object.keys(properties).length ? JSON.stringify(properties, null, 2) : "";
}

export function toLocalInputValue(value?: string | null) {
  if (!value) return "";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value.replace(/Z$/, "");
  const offsetMs = date.getTimezoneOffset() * 60_000;
  return new Date(date.getTime() - offsetMs).toISOString().slice(0, 16);
}

export function fromLocalInputValue(value: string) {
  if (!value) return "";
  return new Date(value).toISOString();
}
