from __future__ import annotations

import json
import queue
import subprocess
import sys
import threading
from pathlib import Path

from app.core import assets, charts, control_db, duck, execution_outputs, git_service, output_kinds, real_runs, reports, workbooks
from app.schemas.domain import CheckResult, ExecutionSummary, ReportSummary, WorkbookStep


def start_workbook_execution(
    workspace_id: str,
    workspace_root: Path,
    workbook_id: str,
    step_ids: list[str] | None = None,
    background: bool = True,
) -> ExecutionSummary:
    workbook = workbooks.get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)
    git_service.ensure_committed(workspace_root, f"Prepare workbook execution: {workbook.title}")
    workbook_commit = (
        git_service.latest_commit_for_path(workspace_root, f"workbooks/{workbook_id}")
        or git_service.head_commit(workspace_root)
    )
    execution = control_db.create_execution(
        workspace_id=workspace_id,
        workbook_id=workbook.id,
        template_id=workbook.template_id,
        target_type="asset",
        target_id=workbook.linked_asset_id,
        executions_root=workspace_root / "executions",
        workbook_git_commit=workbook_commit,
    )
    execution_dir = control_db.get_execution_path(execution.id)
    args = (workspace_id, workspace_root, workbook.id, execution.id, execution_dir, step_ids or [])
    if not background:
        execute_workbook_steps(*args)
        return control_db.get_execution(execution.id)
    thread = threading.Thread(target=execute_workbook_steps, args=args, daemon=True)
    thread.start()
    return execution


def execute_workbook_steps(
    workspace_id: str,
    workspace_root: Path,
    workbook_id: str,
    execution_id: str,
    execution_dir: Path,
    step_ids: list[str] | None = None,
) -> None:
    workbook = workbooks.get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)
    template = workbooks.get_template(workspace_root, workbook.template_id)
    selected_steps = [step for step in workbooks.computed_steps(workspace_root, workbook, step_ids) if step.active]
    control_db.update_execution(execution_id, "running")
    workbooks.update_workbook_status(workspace_root, workbook_id, "computing")
    execution_outputs.append_log(execution_dir, "Execution started.")
    _write_execution_json(execution_dir, execution_id, workbook, "running")
    try:
        chart_summaries = []
        report_summaries: list[ReportSummary] = []
        check_results: list[CheckResult] = []
        _write_target_json(workspace_root, execution_dir, workbook, template)
        for step in selected_steps:
            execution_outputs.append_log(execution_dir, f"Starting step: {step.title}", step_id=step.id)
            existing_outputs = _output_paths(execution_dir)
            _execute_step(workspace_root, execution_dir, workbook.id, step)
            new_outputs = _new_outputs(execution_dir, existing_outputs)
            if not new_outputs:
                execution_outputs.append_log(execution_dir, f"Step wrote no outputs: {step.id}", step_id=step.id)
                execution_outputs.append_log(execution_dir, f"Completed step: {step.id}", step_id=step.id)
                continue
            for output_path in new_outputs:
                kind = output_kinds.infer_output_kind(output_path)
                title = _output_title(output_path, step.title)
                if kind == "plotly_figure":
                    chart_summaries.append(
                        charts.register_chart_from_output(
                            workspace_root=workspace_root,
                            execution_dir=execution_dir,
                            workbook_id=workbook.id,
                            step_id=step.id,
                            execution_id=execution_id,
                            output_path=output_path,
                            chart_id=_artifact_id(workbook.id, step, output_path),
                            title=title,
                        )
                    )
                elif kind == "html":
                    report_summaries.append(
                        reports.register_report_from_output(
                            workspace_root=workspace_root,
                            execution_dir=execution_dir,
                            workbook_id=workbook.id,
                            step_id=step.id,
                            execution_id=execution_id,
                            output_path=output_path,
                            report_id=_artifact_id(workbook.id, step, output_path),
                            title=title,
                            chart_ids=[chart.id for chart in chart_summaries],
                        )
                    )
                elif kind == "check_result":
                    check_results.append(_read_check_result(execution_dir, step, output_path))
            execution_outputs.append_log(execution_dir, f"Completed step: {step.id}", step_id=step.id)
        _write_execution_json(execution_dir, execution_id, workbook, "succeeded")
        _write_summary(execution_dir, chart_summaries, report_summaries, check_results)
        execution_outputs.append_log(execution_dir, "Execution completed.")
        control_db.update_execution(execution_id, "succeeded")
        workbooks.update_workbook_status(workspace_root, workbook_id, "ready")
        git_service.commit_if_dirty(workspace_root, f"Record workbook execution: {workbook.title}")
    except Exception as exc:  # pragma: no cover - captured for UI.
        execution_outputs.append_log(execution_dir, f"Execution failed: {exc}", level="error")
        _write_execution_json(execution_dir, execution_id, workbook, "failed", str(exc))
        control_db.update_execution(execution_id, "failed", str(exc))
        workbooks.update_workbook_status(workspace_root, workbook_id, "failed")
        git_service.commit_if_dirty(workspace_root, f"Record failed workbook execution: {workbook.title}")


def _execute_step(workspace_root: Path, execution_dir: Path, workbook_id: str, step: WorkbookStep) -> None:
    entrypoint = workbooks.step_dir(workspace_root, workbook_id, step.id) / step.entrypoint
    if not entrypoint.exists():
        raise ValueError(f"Step needs {entrypoint.name}: {step.id}")
    _run_python_entrypoint(workspace_root, execution_dir, entrypoint, step.id)


def _run_python_entrypoint(workspace_root: Path, execution_dir: Path, entrypoint: Path, step_id: str) -> None:
    process = subprocess.Popen(
        [
            sys.executable,
            "-u",
            str(entrypoint),
            "--workspace",
            str(workspace_root),
            "--execution",
            str(execution_dir),
            "--duckdb",
            str(duck.db_path(workspace_root)),
        ],
        cwd=workspace_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
    )
    output_queue: queue.Queue[tuple[str, str | None]] = queue.Queue()
    stderr_lines: list[str] = []

    def enqueue_stream(stream, source: str) -> None:
        try:
            for line in stream:
                output_queue.put((source, line.rstrip("\n").rstrip("\r")))
        finally:
            output_queue.put((source, None))

    assert process.stdout is not None
    assert process.stderr is not None
    readers = [
        threading.Thread(target=enqueue_stream, args=(process.stdout, "stdout"), daemon=True),
        threading.Thread(target=enqueue_stream, args=(process.stderr, "stderr"), daemon=True),
    ]
    for reader in readers:
        reader.start()

    closed_streams = 0
    while closed_streams < len(readers):
        source, line = output_queue.get()
        if line is None:
            closed_streams += 1
            continue
        if source == "stderr":
            stderr_lines.append(line)
        execution_outputs.append_log(execution_dir, line, step_id=step_id, source=source)

    returncode = process.wait()
    for reader in readers:
        reader.join()
    if returncode != 0:
        raise RuntimeError("\n".join(stderr_lines).strip() or f"Step failed: {entrypoint}")


def _write_target_json(workspace_root: Path, execution_dir: Path, workbook, template) -> None:
    execution_dir.mkdir(parents=True, exist_ok=True)
    asset = assets.get_asset(workspace_root, workbook.linked_asset_id).model_dump()
    asset_runs = [run_summary.model_dump() for run_summary in real_runs.list_runs(workspace_root, asset_id=workbook.linked_asset_id)]
    data = {
        "workbook": workbook.model_dump(),
        "template": template.model_dump(exclude={"step_files"}),
        "target": asset,
        "asset": asset,
        "runs": asset_runs,
        "data_sources": _execution_workbook_data_sources(workspace_root, workbook),
    }
    (execution_dir / "target.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _execution_workbook_data_sources(workspace_root: Path, workbook) -> list[dict]:
    data_sources: list[dict] = []
    for source in workbook.data_sources:
        item = source.model_dump()
        path = str(item.get("path") or "").strip()
        if path and not path.startswith("duckdb:"):
            source_path = (workspace_root / path).resolve()
            try:
                source_path.relative_to(workspace_root.resolve())
            except ValueError:
                source_path = None
            if source_path and source_path.exists() and source_path.is_file():
                table_name = duck.ingest_file(source_path, workspace_root)
                if table_name:
                    item["duckdb_source"] = f"duckdb:{table_name}"
        data_sources.append(item)
    return data_sources


def _write_execution_json(
    execution_dir: Path,
    execution_id: str,
    workbook,
    status: str,
    error: str | None = None,
) -> None:
    execution_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": execution_id,
        "workbook_id": workbook.id,
        "template_id": workbook.template_id,
        "target_type": "asset",
        "target_id": workbook.linked_asset_id,
        "linked_asset_id": workbook.linked_asset_id,
        "status": status,
        "error": error,
    }
    (execution_dir / "execution.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _output_paths(execution_dir: Path) -> set[str]:
    outputs_dir = execution_dir / "outputs"
    if not outputs_dir.exists():
        return set()
    return {
        path.relative_to(execution_dir).as_posix()
        for path in outputs_dir.rglob("*")
        if path.is_file()
    }


def _new_outputs(execution_dir: Path, previous: set[str]) -> list[str]:
    return sorted(path for path in _output_paths(execution_dir) - previous if path != "outputs/summary.json")


def _output_title(output_path: str, fallback: str) -> str:
    name = Path(output_path).name
    for suffix in (".figure.json", ".html", ".json", ".csv"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    title = name.replace("_", " ").replace("-", " ").strip().title()
    return title or fallback


def _artifact_id(workbook_id: str, step: WorkbookStep, output_path: str) -> str:
    name = Path(output_path).name
    for suffix in (".figure.json", ".html", ".json", ".csv"):
        if name.endswith(suffix):
            name = name[: -len(suffix)]
            break
    output_slug = workbooks.slugify(name)
    if not output_slug or output_slug == step.id:
        return f"{workbook_id}-{step.id}"
    return f"{workbook_id}-{step.id}-{output_slug}"


def _read_check_result(execution_dir: Path, step: WorkbookStep, output_path: str) -> CheckResult:
    data = json.loads((execution_dir / output_path).read_text(encoding="utf-8"))
    return CheckResult.model_validate(
        {
            **data,
            "id": str(data.get("id") or step.id),
            "name": str(data.get("name") or step.title),
            "step_id": step.id,
            "message": str(data.get("message") or ""),
            "output_path": output_path,
        }
    )


def _write_summary(
    execution_dir: Path,
    charts_created,
    reports_created: list[ReportSummary],
    checks_created: list[CheckResult],
) -> None:
    summary = {
        "charts": [chart.model_dump(exclude={"figure"}) for chart in charts_created],
        "reports": [report.model_dump() for report in reports_created],
        "checks": [check.model_dump(exclude_none=True) for check in checks_created],
    }
    (execution_dir / "outputs").mkdir(parents=True, exist_ok=True)
    (execution_dir / "outputs" / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
