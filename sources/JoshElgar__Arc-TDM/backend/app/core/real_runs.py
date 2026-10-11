from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from app.core import assets
from app.schemas.domain import TestRunSummary, TestRunWrite

REQUIRED_RUN_FIELDS = {"id", "name", "asset_id", "start_time", "end_time"}


def list_runs(workspace_root: Path, workspace_id: str | None = None, asset_id: str | None = None) -> list[TestRunSummary]:
    workspace_root = workspace_root.resolve()
    summaries: list[TestRunSummary] = []
    for run_json in sorted((workspace_root / "runs").glob("*/run.json")):
        try:
            run = _summary_from_json(workspace_root, run_json, workspace_id=workspace_id)
        except ValueError:
            continue
        if asset_id and run.asset_id != asset_id:
            continue
        summaries.append(run)
    return sorted(summaries, key=lambda run: run.start_time, reverse=True)


def get_run(workspace_root: Path, run_id: str, workspace_id: str | None = None) -> TestRunSummary:
    workspace_root = workspace_root.resolve()
    run_json = _run_json_path(workspace_root, run_id)
    if not run_json.exists():
        raise FileNotFoundError(run_id)
    return _summary_from_json(workspace_root, run_json, workspace_id=workspace_id)


def save_run(workspace_root: Path, run: TestRunWrite, workspace_id: str | None = None) -> TestRunSummary:
    workspace_root = workspace_root.resolve()
    run_id = slugify(run.id or run.name)
    if not run_id:
        raise ValueError("Run id or name is required.")
    if run.start_time >= run.end_time:
        raise ValueError("Run end_time must be after start_time.")
    assets.get_asset(workspace_root, run.asset_id)
    clean = run.model_copy(update={"id": run_id, "tags": _clean_tags(run.tags)})
    run_dir = workspace_root / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "run.json").write_text(clean.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return _summary_from_json(workspace_root, run_dir / "run.json", workspace_id=workspace_id)


def delete_run(workspace_root: Path, run_id: str) -> None:
    workspace_root = workspace_root.resolve()
    run_dir = _safe_child_dir(workspace_root / "runs", run_id)
    if not run_dir.exists():
        raise FileNotFoundError(run_id)
    if not run_dir.is_dir():
        raise ValueError(f"Run is not a directory: {run_id}")
    shutil.rmtree(run_dir)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def _summary_from_json(
    workspace_root: Path,
    run_json: Path,
    workspace_id: str | None = None,
) -> TestRunSummary:
    run_dir = run_json.parent
    data = json.loads(run_json.read_text(encoding="utf-8"))
    missing_fields = sorted(REQUIRED_RUN_FIELDS - set(data))
    if missing_fields:
        raise ValueError(f"Run is missing required fields: {', '.join(missing_fields)}")
    run_id = str(data.get("id") or run_dir.name)
    asset_id = str(data.get("asset_id") or "")
    try:
        asset_name = assets.get_asset(workspace_root, asset_id).name
    except (FileNotFoundError, ValueError):
        asset_name = None
    return TestRunSummary(
        id=run_id,
        name=str(data.get("name") or run_id),
        asset_id=asset_id,
        asset_name=asset_name,
        start_time=str(data.get("start_time") or ""),
        end_time=str(data.get("end_time") or ""),
        notes=str(data.get("notes") or ""),
        tags=_clean_tags(data.get("tags") if isinstance(data.get("tags"), list) else []),
        properties=_clean_properties(data.get("properties")),
        path=run_dir.relative_to(workspace_root).as_posix(),
        workbook_count=0,
        execution_count=0,
    )


def _run_json_path(workspace_root: Path, run_id: str) -> Path:
    return _safe_child_dir(workspace_root / "runs", run_id) / "run.json"


def _safe_child_dir(parent: Path, child_id: str) -> Path:
    parent = parent.resolve()
    target = (parent / child_id).resolve()
    if target.parent != parent:
        raise ValueError(f"Invalid run id: {child_id}")
    return target


def _clean_tags(tags: object) -> list[str]:
    if not isinstance(tags, list):
        return []
    clean: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        value = str(tag).strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        clean.append(value)
    return clean


def _clean_properties(properties: object) -> dict[str, str]:
    if not isinstance(properties, dict):
        return {}
    return {str(key): str(value) for key, value in properties.items() if str(key).strip()}
