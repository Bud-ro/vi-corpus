from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from app.core import control_db, output_kinds
from app.schemas.domain import ChartSummary

CHART_OUTPUT_KINDS = {"plotly_figure"}


def list_charts(workspace_root: Path) -> list[ChartSummary]:
    summaries: list[ChartSummary] = []
    for chart_json in sorted((workspace_root / "charts").glob("*/chart.json")):
        chart_dir = chart_json.parent
        chart = json.loads(chart_json.read_text(encoding="utf-8"))
        source = chart.get("source") if isinstance(chart.get("source"), dict) else {}
        execution_id = source.get("execution_id")
        output_path = source.get("output_path")
        figure = load_source_figure(workspace_root, output_path, execution_id)
        summaries.append(
            ChartSummary(
                id=chart.get("id", chart_dir.name),
                title=chart.get("title", chart_dir.name),
                path=chart_dir.relative_to(workspace_root).as_posix(),
                figure=figure,
                renderer=chart.get("renderer", "plotly"),
                workbook_id=chart.get("workbook_id"),
                step_id=chart.get("step_id"),
                execution_id=execution_id,
                source_output_path=output_path,
                updated_at=_mtime(chart_json),
            )
        )
    real_charts = [chart for chart in summaries if chart.id != "starter_chart"]
    return real_charts or summaries


def delete_chart(workspace_root: Path, chart_id: str) -> None:
    chart_dir = _safe_child_dir(workspace_root / "charts", chart_id)
    if not chart_dir.exists():
        raise FileNotFoundError(chart_id)
    if not chart_dir.is_dir():
        raise ValueError(f"Chart is not a directory: {chart_id}")
    shutil.rmtree(chart_dir)


def register_chart_from_output(
    workspace_root: Path,
    output_path: str,
    execution_dir: Path | None = None,
    workbook_id: str | None = None,
    step_id: str | None = None,
    execution_id: str | None = None,
    chart_id: str | None = None,
    title: str | None = None,
) -> ChartSummary:
    if execution_dir is None or execution_id is None:
        raise ValueError("Chart execution source is required.")
    source = (execution_dir / output_path).resolve()
    if not str(source).startswith(str(execution_dir.resolve())) or not source.exists() or source.is_dir():
        raise ValueError(f"Chart output not found: {output_path}")
    if output_kinds.infer_output_kind(output_path) not in CHART_OUTPUT_KINDS:
        raise ValueError("Charts must be saved from .figure.json outputs.")
    figure = json.loads(source.read_text(encoding="utf-8"))
    clean_id = chart_id or f"{workbook_id}_{source.name.removesuffix('.figure.json')}"
    clean_title = title or _figure_title(figure) or clean_id.replace("_", " ").title()
    return write_chart(
        workspace_root=workspace_root,
        chart_id=clean_id,
        title=clean_title,
        workbook_id=workbook_id,
        step_id=step_id,
        execution_id=execution_id,
        output_path=output_path,
    )


def write_chart(
    workspace_root: Path,
    chart_id: str,
    title: str,
    output_path: str,
    workbook_id: str | None = None,
    step_id: str | None = None,
    execution_id: str | None = None,
) -> ChartSummary:
    chart_id = slugify(chart_id or title)
    if not chart_id:
        raise ValueError("Chart id or title is required.")
    chart_dir = workspace_root / "charts" / chart_id
    chart_dir.mkdir(parents=True, exist_ok=True)
    source = {
        "execution_id": execution_id,
        "output_path": output_path,
    }
    chart = {
        "id": chart_id,
        "title": title,
        "kind": "chart",
        "renderer": "plotly",
        "workbook_id": workbook_id,
        "step_id": step_id,
        "source": {key: value for key, value in source.items() if value is not None},
    }
    (chart_dir / "chart.json").write_text(json.dumps(chart, indent=2) + "\n", encoding="utf-8")
    return ChartSummary(
        id=chart_id,
        title=title,
        path=chart_dir.relative_to(workspace_root).as_posix(),
        figure=load_source_figure(workspace_root, output_path, execution_id),
        renderer="plotly",
        workbook_id=workbook_id,
        step_id=step_id,
        execution_id=execution_id,
        source_output_path=output_path,
        updated_at=_mtime(chart_dir / "chart.json"),
    )


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def load_source_figure(
    workspace_root: Path,
    output_path: str | None,
    execution_id: str | None = None,
) -> dict:
    if not execution_id or not output_path:
        return {}
    source_dirs: list[Path] = []
    try:
        source_dirs.append(control_db.get_execution_path(execution_id))
    except KeyError:
        pass
    source_dirs.append(workspace_root / "executions" / execution_id)
    seen: set[Path] = set()
    for source_dir in source_dirs:
        resolved_source_dir = source_dir.resolve()
        if resolved_source_dir in seen:
            continue
        seen.add(resolved_source_dir)
        source = (resolved_source_dir / output_path).resolve()
        if (
            not str(source).startswith(str(resolved_source_dir))
            or not source.exists()
            or source.is_dir()
        ):
            continue
        try:
            figure = json.loads(source.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if isinstance(figure, dict):
            return figure
    return {}


def _mtime(path: Path) -> str | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()


def _safe_child_dir(parent: Path, child_id: str) -> Path:
    parent = parent.resolve()
    target = (parent / child_id).resolve()
    if target.parent != parent:
        raise ValueError(f"Invalid chart id: {child_id}")
    return target


def _figure_title(figure: dict) -> str | None:
    layout = figure.get("layout") if isinstance(figure.get("layout"), dict) else {}
    raw_title = layout.get("title")
    if isinstance(raw_title, str):
        return raw_title
    if isinstance(raw_title, dict) and isinstance(raw_title.get("text"), str):
        return raw_title["text"]
    return None
