from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from app.core import assets, control_db
from app.schemas.domain import (
    ChartSummary,
    ReportSummary,
    PanelSummary,
    WorkbookDataSource,
    WorkbookStep,
    WorkbookDetail,
    WorkbookSummary,
    WorkbookTemplateSummary,
    WorkbookTemplateWrite,
    WorkbookWrite,
    CheckResult,
)


def list_templates(workspace_root: Path) -> list[WorkbookTemplateSummary]:
    workspace_root = workspace_root.resolve()
    return [
        _template_from_json(workspace_root, template_json)
        for template_json in sorted((workspace_root / "workbook_templates").glob("*/*/template.json"))
    ]


def get_template(workspace_root: Path, template_id: str, kind: str | None = None) -> WorkbookTemplateSummary:
    workspace_root = workspace_root.resolve()
    template_json = _template_json_path(workspace_root, template_id, kind=kind)
    if not template_json.exists():
        raise FileNotFoundError(template_id)
    return _template_from_json(workspace_root, template_json)


def save_template(workspace_root: Path, template: WorkbookTemplateWrite, steps: list[WorkbookStep] | None = None) -> WorkbookTemplateSummary:
    workspace_root = workspace_root.resolve()
    template_id = slugify(template.id or template.name)
    if not template_id:
        raise ValueError("Workbook template id or name is required.")
    step_ids = [slugify(step.id or step.title) for step in steps] if steps is not None else template.steps
    clean = template.model_copy(update={"id": template_id, "steps": step_ids, "tags": _clean_tags(template.tags)})
    template_dir = workspace_root / "workbook_templates" / "workbook" / template_id
    template_dir.mkdir(parents=True, exist_ok=True)
    (template_dir / "template.json").write_text(clean.model_dump_json(indent=2) + "\n", encoding="utf-8")
    if steps is not None:
        steps_root = template_dir / "steps"
        if steps_root.exists():
            for existing_step_dir in steps_root.iterdir():
                if existing_step_dir.is_dir() and existing_step_dir.name not in set(step_ids):
                    shutil.rmtree(existing_step_dir)
        for step in steps:
            save_template_step_file(workspace_root, "workbook", template_id, step)
    return get_template(workspace_root, template_id)


def save_template_step_file(workspace_root: Path, kind: str, template_id: str, step: WorkbookStep) -> WorkbookStep:
    workspace_root = workspace_root.resolve()
    template_dir = _template_dir(workspace_root, template_id)
    return _save_step(template_dir / "steps", step)


def save_template_step(
    workspace_root: Path,
    template_id: str,
    step: WorkbookStep,
    kind: str | None = None,
) -> WorkbookStep:
    workspace_root = workspace_root.resolve()
    template = get_template(workspace_root, template_id, kind=kind)
    saved = save_template_step_file(workspace_root, "workbook", template_id, step)
    step_order = template.steps if saved.id in template.steps else [*template.steps, saved.id]
    template_write = WorkbookTemplateWrite(
        id=template.id,
        name=template.name,
        description=template.description,
        steps=step_order,
        tags=template.tags,
        properties=template.properties,
    )
    save_template(workspace_root, template_write)
    return saved


def save_workbook_step(workspace_root: Path, workbook_id: str, step: WorkbookStep, workspace_id: str | None = None) -> WorkbookStep:
    workspace_root = workspace_root.resolve()
    workbook = get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)
    workbook_dir = _workbook_dir(workspace_root, workbook.id)
    saved = _save_step(workbook_dir / "steps", step)
    step_order = workbook.step_order if saved.id in workbook.step_order else [*workbook.step_order, saved.id]
    save_workbook(workspace_root, workbook.model_copy(update={"step_order": step_order}), workspace_id=workspace_id)
    return saved


def delete_workbook_step(workspace_root: Path, workbook_id: str, step_id: str, workspace_id: str | None = None) -> None:
    workspace_root = workspace_root.resolve()
    workbook = get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)
    step_dir = _safe_child_dir(_workbook_dir(workspace_root, workbook.id) / "steps", step_id)
    if not step_dir.exists():
        raise FileNotFoundError(step_id)
    if not step_dir.is_dir():
        raise ValueError(f"Step is not a directory: {step_id}")
    shutil.rmtree(step_dir)
    save_workbook(
        workspace_root,
        workbook.model_copy(update={"step_order": [candidate for candidate in workbook.step_order if candidate != step_id]}),
        workspace_id=workspace_id,
    )


def list_workbooks(workspace_root: Path, workspace_id: str | None = None) -> list[WorkbookSummary]:
    workspace_root = workspace_root.resolve()
    return [
        _workbook_from_json(workspace_root, workbook_json, workspace_id=workspace_id)
        for workbook_json in sorted((workspace_root / "workbooks").glob("*/workbook.json"))
    ]


def get_workbook(workspace_root: Path, workbook_id: str, workspace_id: str | None = None) -> WorkbookSummary:
    workspace_root = workspace_root.resolve()
    workbook_json = _workbook_json_path(workspace_root, workbook_id)
    if not workbook_json.exists():
        raise FileNotFoundError(workbook_id)
    return _workbook_from_json(workspace_root, workbook_json, workspace_id=workspace_id)


def get_workbook_detail(
    workspace_root: Path,
    workbook_id: str,
    workspace_id: str | None = None,
    charts: list[ChartSummary] | None = None,
    reports: list[ReportSummary] | None = None,
    checks: list[CheckResult] | None = None,
) -> WorkbookDetail:
    workspace_root = workspace_root.resolve()
    workbook = get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)
    template = get_template(workspace_root, workbook.template_id)
    steps = list_workbook_steps(workspace_root, workbook.id)
    step_ids = workbook.step_order or [step.id for step in steps]
    steps_by_id = {step.id: step for step in steps}
    steps = [steps_by_id[step_id] for step_id in step_ids if step_id in steps_by_id]
    visible_step_ids = {step.id for step in steps}
    executions = control_db.list_executions(workspace_id, workbook_id=workbook_id) if workspace_id else []
    workbook_checks = checks if checks is not None else _latest_check_results(executions)
    workbook_charts = [
        chart for chart in charts or [] if chart.workbook_id == workbook_id and chart.step_id in visible_step_ids
    ]
    workbook_reports = [
        report for report in reports or [] if report.workbook_id == workbook_id and report.step_id in visible_step_ids
    ]
    workbook_checks = [check for check in workbook_checks if check.step_id in visible_step_ids]
    return WorkbookDetail(
        workbook=workbook,
        template=template,
        steps=steps,
        panels=_panels_from_outputs(workbook_charts, workbook_reports, workbook_checks, executions[0].id if executions else None),
        executions=executions,
        charts=workbook_charts,
        reports=workbook_reports,
        checks=workbook_checks,
    )


def save_workbook(workspace_root: Path, workbook: WorkbookWrite, workspace_id: str | None = None) -> WorkbookSummary:
    workspace_root = workspace_root.resolve()
    workbook_id = slugify(workbook.id or workbook.title)
    if not workbook_id:
        raise ValueError("Workbook id or title is required.")
    template = get_template(workspace_root, workbook.template_id)
    if not workbook.linked_asset_id.strip():
        raise ValueError("Workbook needs a linked asset.")
    assets.get_asset(workspace_root, workbook.linked_asset_id)
    workbook_dir = workspace_root / "workbooks" / workbook_id
    is_new = not (workbook_dir / "workbook.json").exists()
    existing_step_ids = [step.id for step in _steps_from_dir(workbook_dir / "steps")]
    step_order = workbook.step_order or existing_step_ids or template.steps
    clean = workbook.model_copy(
        update={
            "id": workbook_id,
            "step_order": step_order,
            "data_sources": _clean_data_sources(workbook.data_sources),
            "tags": _clean_tags(workbook.tags),
        }
    )
    workbook_dir.mkdir(parents=True, exist_ok=True)
    (workbook_dir / "workbook.json").write_text(clean.model_dump_json(indent=2) + "\n", encoding="utf-8")
    if is_new:
        _copy_template_steps_to_workbook(workspace_root, template, workbook_dir)
    return get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)


def duplicate_workbook(
    workspace_root: Path,
    workbook_id: str,
    new_id: str | None = None,
    title: str | None = None,
    linked_asset_id: str | None = None,
    data_sources: list[WorkbookDataSource] | None = None,
    workspace_id: str | None = None,
) -> WorkbookSummary:
    workspace_root = workspace_root.resolve()
    source = get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)
    duplicate_title = title.strip() if title and title.strip() else f"{source.title} Copy"
    duplicate_id = slugify(new_id or duplicate_title)
    if not duplicate_id:
        raise ValueError("Duplicate workbook needs a title or id.")
    source_dir = _workbook_dir(workspace_root, source.id)
    target_dir = workspace_root / "workbooks" / duplicate_id
    if (target_dir / "workbook.json").exists():
        raise ValueError(f"Workbook already exists: {duplicate_id}")
    duplicate_asset_id = linked_asset_id if linked_asset_id is not None else source.linked_asset_id
    if not duplicate_asset_id or not duplicate_asset_id.strip():
        raise ValueError("Workbook needs a linked asset.")
    assets.get_asset(workspace_root, duplicate_asset_id)
    target_dir.mkdir(parents=True, exist_ok=True)
    if (source_dir / "steps").exists():
        shutil.copytree(source_dir / "steps", target_dir / "steps", dirs_exist_ok=True)
    duplicate = source.model_copy(
        update={
            "id": duplicate_id,
            "title": duplicate_title,
            "linked_asset_id": duplicate_asset_id,
            "data_sources": _clean_data_sources(data_sources if data_sources is not None else source.data_sources),
            "status": "ready",
        }
    )
    (target_dir / "workbook.json").write_text(
        duplicate.model_dump_json(
            indent=2,
            exclude={"path", "template_name", "linked_asset_name", "latest_execution_id", "latest_execution_status", "updated_at"},
        )
        + "\n",
        encoding="utf-8",
    )
    return get_workbook(workspace_root, duplicate_id, workspace_id=workspace_id)


def update_workbook_status(workspace_root: Path, workbook_id: str, status: str) -> None:
    workspace_root = workspace_root.resolve()
    workbook_json = _workbook_json_path(workspace_root, workbook_id)
    if not workbook_json.exists():
        raise FileNotFoundError(workbook_id)
    data = json.loads(workbook_json.read_text(encoding="utf-8"))
    data["status"] = status
    data["updated_at"] = utc_now()
    workbook_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def delete_workbook(workspace_root: Path, workbook_id: str) -> None:
    workspace_root = workspace_root.resolve()
    workbook_dir = _safe_child_dir(workspace_root / "workbooks", workbook_id)
    if not workbook_dir.exists():
        raise FileNotFoundError(workbook_id)
    if not workbook_dir.is_dir():
        raise ValueError(f"Workbook is not a directory: {workbook_id}")
    shutil.rmtree(workbook_dir)


def computed_steps(workspace_root: Path, workbook: WorkbookSummary, step_ids: list[str] | None = None) -> list[WorkbookStep]:
    workspace_root = workspace_root.resolve()
    steps = list_workbook_steps(workspace_root, workbook.id)
    wanted = step_ids or workbook.step_order or [step.id for step in steps]
    steps_by_id = {step.id: step for step in steps}
    return [steps_by_id[step_id] for step_id in wanted if step_id in steps_by_id]


def _panels_from_outputs(
    charts: list[ChartSummary],
    reports: list[ReportSummary],
    checks: list[CheckResult],
    fallback_execution_id: str | None,
) -> list[PanelSummary]:
    panels: list[PanelSummary] = []
    panels.extend(
        PanelSummary(
            id=f"chart:{chart.id}",
            title=chart.title,
            kind="chart",
            step_id=chart.step_id,
            execution_id=chart.execution_id,
            source_output_path=chart.source_output_path,
        )
        for chart in charts
    )
    panels.extend(
        PanelSummary(
            id=f"report:{report.id}",
            title=report.title,
            kind="report",
            step_id=report.step_id,
            execution_id=report.execution_id,
            source_output_path=report.source_output_path,
        )
        for report in reports
    )
    panels.extend(
        PanelSummary(
            id=f"check:{check.id}",
            title=check.name,
            kind="check",
            step_id=check.step_id or check.id,
            execution_id=fallback_execution_id,
            source_output_path=check.output_path,
            status=check.status,
        )
        for check in checks
    )
    return panels


def step_dir(workspace_root: Path, workbook_id: str, step_id: str) -> Path:
    workspace_root = workspace_root.resolve()
    return _safe_child_dir(_safe_child_dir(workspace_root / "workbooks", workbook_id) / "steps", step_id)


def list_workbook_steps(workspace_root: Path, workbook_id: str) -> list[WorkbookStep]:
    workspace_root = workspace_root.resolve()
    return _steps_from_dir(_workbook_dir(workspace_root, workbook_id) / "steps")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _template_from_json(workspace_root: Path, template_json: Path) -> WorkbookTemplateSummary:
    template_dir = template_json.parent
    data = json.loads(template_json.read_text(encoding="utf-8"))
    template_id = str(data.get("id") or template_dir.name)
    steps = [_step_from_json(step_json) for step_json in sorted((template_dir / "steps").glob("*/step.json"))]
    step_order = [str(step_id) for step_id in data.get("steps", [])] if isinstance(data.get("steps"), list) else [step.id for step in steps]
    return WorkbookTemplateSummary(
        id=template_id,
        name=str(data.get("name") or template_id),
        description=str(data.get("description") or ""),
        steps=step_order,
        step_files=steps,
        tags=_clean_tags(data.get("tags") if isinstance(data.get("tags"), list) else []),
        properties=_clean_properties(data.get("properties")),
        path=template_dir.relative_to(workspace_root).as_posix(),
        workbook_count=_count_template_workbooks(workspace_root, template_id),
    )


def _step_from_json(step_json: Path) -> WorkbookStep:
    step = WorkbookStep.model_validate_json(step_json.read_text(encoding="utf-8"))
    script_path = step_json.parent / step.entrypoint
    if script_path.exists() and script_path.is_file():
        step = step.model_copy(update={"script": script_path.read_text(encoding="utf-8")})
    return step


def _workbook_from_json(workspace_root: Path, workbook_json: Path, workspace_id: str | None = None) -> WorkbookSummary:
    workbook_dir = workbook_json.parent
    data = json.loads(workbook_json.read_text(encoding="utf-8"))
    workbook_id = str(data.get("id") or workbook_dir.name)
    template_id = str(data.get("template_id") or "")
    linked_asset_id = str(data.get("linked_asset_id") or "").strip()
    if not linked_asset_id:
        raise ValueError(f"Workbook is missing linked_asset_id: {workbook_id}")
    executions = control_db.list_executions(workspace_id, workbook_id=workbook_id) if workspace_id else []
    latest = executions[0] if executions else None
    try:
        template_name = get_template(workspace_root, template_id).name
    except (FileNotFoundError, ValueError):
        template_name = None
    return WorkbookSummary(
        id=workbook_id,
        title=str(data.get("title") or workbook_id),
        template_id=template_id,
        template_name=template_name,
        linked_asset_id=linked_asset_id,
        linked_asset_name=_linked_asset_name(workspace_root, linked_asset_id),
        step_order=[str(step_id) for step_id in data.get("step_order", [])] if isinstance(data.get("step_order"), list) else [],
        data_sources=_data_sources(data.get("data_sources")),
        tags=_clean_tags(data.get("tags") if isinstance(data.get("tags"), list) else []),
        properties=_clean_properties(data.get("properties")),
        status=data.get("status") if data.get("status") in {"draft", "ready", "computing", "failed", "locked", "archived"} else "ready",
        latest_execution_id=latest.id if latest else None,
        latest_execution_status=latest.status if latest else None,
        latest_execution_started_at=latest.started_at if latest else None,
        path=workbook_dir.relative_to(workspace_root).as_posix(),
        updated_at=data.get("updated_at") if isinstance(data.get("updated_at"), str) else _mtime(workbook_json),
    )


def _template_json_path(workspace_root: Path, template_id: str, kind: str | None = None) -> Path:
    return _template_dir(workspace_root, template_id, kind=kind) / "template.json"


def _workbook_json_path(workspace_root: Path, workbook_id: str) -> Path:
    return _workbook_dir(workspace_root, workbook_id) / "workbook.json"


def _template_dir(workspace_root: Path, template_id: str, kind: str | None = None) -> Path:
    templates_root = workspace_root / "workbook_templates"
    clean_id = slugify(template_id)
    if not clean_id:
        raise ValueError("Workbook template id is required.")
    return _safe_child_dir(_safe_child_dir(templates_root, "workbook"), clean_id)


def _workbook_dir(workspace_root: Path, workbook_id: str) -> Path:
    clean_id = slugify(workbook_id)
    if not clean_id:
        raise ValueError("Workbook id is required.")
    return _safe_child_dir(workspace_root / "workbooks", clean_id)


def _save_step(steps_root: Path, step: WorkbookStep) -> WorkbookStep:
    step_id = slugify(step.id or step.title)
    if not step_id:
        raise ValueError("Step id or title is required.")
    step_dir = steps_root / step_id
    step_dir.mkdir(parents=True, exist_ok=True)
    script = step.script
    clean = step.model_copy(update={"id": step_id, "script": None})
    (step_dir / "step.json").write_text(clean.model_dump_json(indent=2, exclude_none=True) + "\n", encoding="utf-8")
    if script is not None:
        (step_dir / step.entrypoint).write_text(script.rstrip() + "\n", encoding="utf-8")
    return _step_from_json(step_dir / "step.json")


def _steps_from_dir(steps_root: Path) -> list[WorkbookStep]:
    if not steps_root.exists():
        return []
    return [_step_from_json(step_json) for step_json in sorted(steps_root.glob("*/step.json"))]


def _copy_template_steps_to_workbook(workspace_root: Path, template: WorkbookTemplateSummary, workbook_dir: Path) -> None:
    steps_root = workbook_dir / "steps"
    steps_root.mkdir(parents=True, exist_ok=True)
    for step in template.step_files:
        _save_step(steps_root, step)


def _safe_child_dir(parent: Path, child_id: str) -> Path:
    parent = parent.resolve()
    target = (parent / child_id).resolve()
    if target.parent != parent:
        raise ValueError(f"Invalid id: {child_id}")
    return target


def _linked_asset_name(workspace_root: Path, asset_id: str | None) -> str | None:
    if not asset_id:
        return None
    try:
        return assets.get_asset(workspace_root, asset_id).name
    except (FileNotFoundError, ValueError):
        return None


def _data_sources(raw: object) -> list[WorkbookDataSource]:
    if not isinstance(raw, list):
        return []
    sources: list[WorkbookDataSource] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        try:
            sources.append(WorkbookDataSource.model_validate(item))
        except ValueError:
            continue
    return _clean_data_sources(sources)


def _clean_data_sources(data_sources: object) -> list[WorkbookDataSource]:
    if not isinstance(data_sources, list):
        return []
    clean: list[WorkbookDataSource] = []
    seen: set[str] = set()
    for source in data_sources:
        try:
            item = source if isinstance(source, WorkbookDataSource) else WorkbookDataSource.model_validate(source)
        except ValueError:
            continue
        source_id = slugify(item.id or item.name or item.path)
        path = item.path.strip()
        if not source_id or not path or source_id in seen:
            continue
        seen.add(source_id)
        clean.append(
            item.model_copy(
                update={
                    "id": source_id,
                    "name": item.name.strip() or source_id,
                    "path": path,
                    "kind": item.kind.strip() or "file",
                    "notes": item.notes.strip(),
                }
            )
        )
    return clean


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


def _count_template_workbooks(workspace_root: Path, template_id: str) -> int:
    count = 0
    for workbook_json in (workspace_root / "workbooks").glob("*/workbook.json"):
        try:
            data = json.loads(workbook_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("template_id") == template_id:
            count += 1
    return count


def _mtime(path: Path) -> str | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()


def _latest_check_results(executions) -> list[CheckResult]:
    if not executions:
        return []
    try:
        execution_dir = control_db.get_execution_path(executions[0].id)
    except KeyError:
        return []
    summary = execution_dir / "outputs" / "summary.json"
    if not summary.exists():
        return []
    try:
        data = json.loads(summary.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    checks = data.get("checks")
    if not isinstance(checks, list):
        return []
    results: list[CheckResult] = []
    for check in checks:
        if isinstance(check, dict):
            results.append(CheckResult.model_validate(check))
    return results
