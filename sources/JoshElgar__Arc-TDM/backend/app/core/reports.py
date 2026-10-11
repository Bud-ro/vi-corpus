from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from app.core import control_db, output_kinds
from app.schemas.domain import ReportSummary

REPORT_OUTPUT_KINDS = {"html"}
REPORT_MEDIA_TYPES = {
    "html": "text/html; charset=utf-8",
}
REPORT_ACTION_TITLE_PATTERN = re.compile(
    r"^(make|create|generate|build|prepare|write|produce|compile|draft)\s+(?:(a|an|the)\s+)?(.+)$",
    re.IGNORECASE,
)
GENERIC_REPORT_TITLES = {"report", "html report"}
PREFIX_GUARD_WORDS = {"and", "or", "versus", "vs"}


def list_reports(workspace_root: Path) -> list[ReportSummary]:
    report_summaries: list[ReportSummary] = []
    for report_json in sorted((workspace_root / "reports").glob("*/report.json")):
        report_summaries.append(_report_summary_from_json(workspace_root, report_json))
    return report_summaries


def get_report(workspace_root: Path, report_id: str) -> ReportSummary:
    report_json = _report_json_path(workspace_root, report_id)
    if not report_json.exists():
        raise FileNotFoundError(report_id)
    return _report_summary_from_json(workspace_root, report_json)


def delete_report(workspace_root: Path, report_id: str) -> None:
    report_dir = _safe_child_dir(workspace_root / "reports", report_id)
    if not report_dir.exists():
        raise FileNotFoundError(report_id)
    if not report_dir.is_dir():
        raise ValueError(f"Report is not a directory: {report_id}")
    shutil.rmtree(report_dir)


def register_report_from_output(
    workspace_root: Path,
    output_path: str,
    report_id: str,
    title: str,
    execution_dir: Path | None = None,
    workbook_id: str | None = None,
    step_id: str | None = None,
    execution_id: str | None = None,
    chart_ids: list[str] | None = None,
) -> ReportSummary:
    if execution_dir is None or execution_id is None:
        raise ValueError("Report execution source is required.")
    source = (execution_dir / output_path).resolve()
    if not str(source).startswith(str(execution_dir.resolve())) or not source.exists() or source.is_dir():
        raise ValueError(f"Report output not found: {output_path}")
    output_kind = output_kinds.infer_output_kind(output_path)
    if output_kind not in REPORT_OUTPUT_KINDS:
        raise ValueError("Reports must be saved from HTML outputs.")
    return write_report(
        workspace_root=workspace_root,
        report_id=report_id,
        title=title,
        workbook_id=workbook_id,
        step_id=step_id,
        execution_id=execution_id,
        output_path=output_path,
        chart_ids=chart_ids or [],
    )


def write_report(
    workspace_root: Path,
    report_id: str,
    title: str,
    output_path: str,
    workbook_id: str | None = None,
    step_id: str | None = None,
    execution_id: str | None = None,
    chart_ids: list[str] | None = None,
) -> ReportSummary:
    title = clean_report_title(title, fallback=report_id)
    report_id = slugify(report_id or title)
    if not report_id:
        raise ValueError("Report id or title is required.")
    report_format = output_kinds.infer_output_kind(output_path)
    if report_format not in REPORT_OUTPUT_KINDS:
        raise ValueError("Reports must be saved from HTML execution outputs.")
    report_dir = workspace_root / "reports" / report_id
    report_dir.mkdir(parents=True, exist_ok=True)
    source = {
        "execution_id": execution_id,
        "output_path": output_path,
    }
    report = {
        "id": report_id,
        "title": title,
        "kind": "report",
        "format": report_format,
        "workbook_id": workbook_id,
        "step_id": step_id,
        "source": {key: value for key, value in source.items() if value is not None},
        "chart_ids": chart_ids or [],
    }
    (report_dir / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return ReportSummary(
        id=report_id,
        title=title,
        path=report_dir.relative_to(workspace_root).as_posix(),
        format=report_format,
        workbook_id=workbook_id,
        step_id=step_id,
        execution_id=execution_id,
        source_output_path=output_path,
        created_at=_mtime(report_dir / "report.json"),
        chart_ids=chart_ids or [],
    )


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def clean_report_title(title: str, fallback: str = "") -> str:
    candidates = [_prettify_title(title), _prettify_title(fallback)]
    for candidate in candidates:
        cleaned = _strip_report_action_prefix(candidate)
        if _specific_report_title(cleaned):
            return cleaned
    for candidate in candidates:
        if candidate:
            return candidate
    return "Report"


def report_file_path(workspace_root: Path, report_id: str) -> Path:
    report_json = _report_json_path(workspace_root, report_id)
    if not report_json.exists():
        raise FileNotFoundError(report_id)
    report = json.loads(report_json.read_text(encoding="utf-8"))
    source = report.get("source") if isinstance(report.get("source"), dict) else {}
    execution_id = source.get("execution_id")
    output_path = source.get("output_path")
    if not output_path or not execution_id:
        raise FileNotFoundError(report_id)
    source_dir = control_db.get_execution_path(execution_id)
    target = (source_dir / output_path).resolve()
    if not str(target).startswith(str(source_dir.resolve())) or not target.exists() or target.is_dir():
        raise FileNotFoundError(report_id)
    if output_kinds.infer_output_kind(output_path) not in REPORT_OUTPUT_KINDS:
        raise ValueError("Report source is not an HTML output.")
    return target


def report_media_type(path: Path) -> str:
    return REPORT_MEDIA_TYPES.get(output_kinds.infer_output_kind(path), "application/octet-stream")


def _mtime(path: Path) -> str | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()


def _report_json_path(workspace_root: Path, report_id: str) -> Path:
    return _safe_child_dir(workspace_root / "reports", report_id) / "report.json"


def _report_summary_from_json(workspace_root: Path, report_json: Path) -> ReportSummary:
    report_dir = report_json.parent
    report = json.loads(report_json.read_text(encoding="utf-8"))
    source = report.get("source") if isinstance(report.get("source"), dict) else {}
    report_id = report.get("id", report_dir.name)
    return ReportSummary(
        id=report_id,
        title=clean_report_title(report.get("title", report_dir.name), fallback=report_id),
        path=report_dir.relative_to(workspace_root).as_posix(),
        format=report.get("format", "file"),
        workbook_id=report.get("workbook_id"),
        step_id=report.get("step_id"),
        execution_id=source.get("execution_id"),
        source_output_path=source.get("output_path"),
        created_at=_mtime(report_json),
        chart_ids=[str(chart_id) for chart_id in report.get("chart_ids", [])],
    )


def _safe_child_dir(parent: Path, child_id: str) -> Path:
    parent = parent.resolve()
    target = (parent / child_id).resolve()
    if target.parent != parent:
        raise ValueError(f"Invalid report id: {child_id}")
    return target


def _prettify_title(value: str) -> str:
    title = str(value or "").strip()
    if not title:
        return ""
    if "_" in title and " " not in title:
        title = title.replace("_", " ")
    title = re.sub(r"\s+", " ", title).strip()
    if title.islower() or title.isupper():
        return title.title()
    return title


def _strip_report_action_prefix(title: str) -> str:
    match = REPORT_ACTION_TITLE_PATTERN.match(title)
    if not match:
        return title
    candidate = match.group(3).strip()
    first_word = candidate.split(maxsplit=1)[0].lower() if candidate else ""
    if first_word in PREFIX_GUARD_WORDS:
        return title
    if candidate.islower() or candidate.isupper():
        return candidate.title()
    return candidate


def _specific_report_title(title: str) -> bool:
    return bool(title) and title.lower() not in GENERIC_REPORT_TITLES
