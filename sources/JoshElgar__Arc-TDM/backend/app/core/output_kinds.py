from __future__ import annotations

from pathlib import Path


def infer_output_kind(path: str | Path) -> str:
    normalized = Path(path).as_posix().lower()
    name = Path(path).name.lower()
    suffix = Path(path).suffix.lower()
    if normalized.startswith("outputs/checks/") and suffix == ".json":
        return "check_result"
    if name.endswith(".figure.json"):
        return "plotly_figure"
    if name.endswith(".table.json"):
        return "table_json"
    if suffix == ".json":
        return "json"
    if suffix in {".txt", ".log", ".md"}:
        return "text"
    if suffix in {".html", ".htm"}:
        return "html"
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        return "image"
    return suffix.lstrip(".") or "file"
