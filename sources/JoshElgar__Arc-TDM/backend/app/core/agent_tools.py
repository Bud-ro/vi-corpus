from __future__ import annotations

import json
from pathlib import Path

from agents import function_tool

from app.core import assets, control_db, execution_outputs, executions, files, git_service, real_runs, workbooks
from app.core.timing import ChatTimer, optional_span
from app.schemas.domain import (
    AssetWrite,
    TestRunWrite,
    WorkbookStep,
    WorkbookTemplateWrite,
    WorkbookWrite,
)


def build_workspace_tools(
    workspace_root: Path,
    workspace_id: str = control_db.DEFAULT_WORKSPACE_ID,
    timer: ChatTimer | None = None,
):
    @function_tool
    def list_workspace_files() -> str:
        """List files in the current Arc workspace."""
        with optional_span(timer, "tool.list_workspace_files"):
            entries = files.list_files(workspace_root)
            return json.dumps([entry.model_dump() for entry in entries], indent=2)

    @function_tool
    def read_workspace_file(path: str) -> str:
        """Read a text file from the current Arc workspace."""
        with optional_span(timer, "tool.read_workspace_file", path=path):
            try:
                read = files.read_workspace_text_file(workspace_root, path, limit=20000)
            except FileNotFoundError as exc:
                raise ValueError(f"File not found: {path}") from exc
            return read.text

    @function_tool
    def list_assets() -> str:
        """List physical assets in the workspace."""
        with optional_span(timer, "tool.list_assets"):
            return json.dumps([asset.model_dump() for asset in assets.list_assets(workspace_root)], indent=2)

    @function_tool
    def save_asset(asset_json: str) -> str:
        """Create or update an asset from JSON with id, name, tags, and properties."""
        with optional_span(timer, "tool.save_asset"):
            asset = AssetWrite.model_validate(json.loads(asset_json))
            saved = assets.save_asset(workspace_root, asset)
            git_service.commit_if_dirty(workspace_root, f"Save asset: {saved.name}")
            return saved.model_dump_json(indent=2)

    @function_tool
    def list_runs() -> str:
        """List real-world test runs in the workspace."""
        with optional_span(timer, "tool.list_runs"):
            items = real_runs.list_runs(workspace_root, workspace_id=workspace_id)
            return json.dumps([item.model_dump() for item in items], indent=2)

    @function_tool
    def save_run(run_json: str) -> str:
        """Create or update a real-world test run from JSON with asset_id and start/end time."""
        with optional_span(timer, "tool.save_run"):
            run = TestRunWrite.model_validate(json.loads(run_json))
            saved = real_runs.save_run(workspace_root, run, workspace_id=workspace_id)
            git_service.commit_if_dirty(workspace_root, f"Save run: {saved.name}")
            return saved.model_dump_json(indent=2)

    @function_tool
    def list_workbook_templates() -> str:
        """List workbook templates and their step contracts."""
        with optional_span(timer, "tool.list_workbook_templates"):
            items = workbooks.list_templates(workspace_root)
            return json.dumps([item.model_dump(exclude={"step_files"}) for item in items], indent=2)

    @function_tool
    def save_workbook_template(template_json: str, steps_json: str = "[]") -> str:
        """Create or update a workbook template and optional step definitions."""
        with optional_span(timer, "tool.save_workbook_template"):
            template = WorkbookTemplateWrite.model_validate(json.loads(template_json))
            raw_steps = json.loads(steps_json) if steps_json.strip() else []
            if not isinstance(raw_steps, list):
                raise ValueError("steps_json must be a JSON array.")
            steps = [WorkbookStep.model_validate(step) for step in raw_steps]
            saved = workbooks.save_template(workspace_root, template, steps=steps if steps else None)
            git_service.commit_if_dirty(workspace_root, f"Save workbook template: {saved.name}")
            return saved.model_dump_json(indent=2)

    @function_tool
    def save_workbook_template_step(template_id: str, step_json: str, kind: str = "") -> str:
        """Create or update one reusable, independently runnable template step with one clear responsibility."""
        with optional_span(timer, "tool.save_workbook_step", template_id=template_id):
            step = WorkbookStep.model_validate(json.loads(step_json))
            saved = workbooks.save_template_step(workspace_root, template_id, step, kind=kind or None)
            git_service.commit_if_dirty(workspace_root, f"Save workbook template step: {saved.title}")
            return saved.model_dump_json(indent=2)

    @function_tool
    def save_workbook_step(workbook_id: str, step_json: str) -> str:
        """Create or update one independently runnable workbook step with one clear responsibility and useful result."""
        with optional_span(timer, "tool.save_workbook_step", template_id=workbook_id):
            step = WorkbookStep.model_validate(json.loads(step_json))
            saved = workbooks.save_workbook_step(workspace_root, workbook_id, step, workspace_id=workspace_id)
            git_service.commit_if_dirty(workspace_root, f"Save workbook step: {saved.title}")
            return saved.model_dump_json(indent=2)

    @function_tool
    def list_workbooks() -> str:
        """List workbooks in the workspace."""
        with optional_span(timer, "tool.list_workbooks"):
            items = workbooks.list_workbooks(workspace_root, workspace_id=workspace_id)
            return json.dumps([item.model_dump() for item in items], indent=2)

    @function_tool
    def save_workbook(workbook_json: str) -> str:
        """Create or update a workbook from JSON with template_id and one asset/run target."""
        with optional_span(timer, "tool.save_workbook"):
            workbook = WorkbookWrite.model_validate(json.loads(workbook_json))
            saved = workbooks.save_workbook(workspace_root, workbook, workspace_id=workspace_id)
            git_service.commit_if_dirty(workspace_root, f"Save workbook: {saved.title}")
            return saved.model_dump_json(indent=2)

    @function_tool
    def compute_workbook(workbook_id: str) -> str:
        """Start a workbook execution and return the queued execution id."""
        with optional_span(timer, "tool.compute_workbook", workbook_id=workbook_id):
            execution = executions.start_workbook_execution(workspace_id, workspace_root, workbook_id)
            return execution.model_dump_json(indent=2)

    @function_tool
    def list_execution_outputs(execution_id: str) -> str:
        """List output files produced by a workbook execution."""
        with optional_span(timer, "tool.list_execution_outputs", execution_id=execution_id):
            execution_dir = control_db.get_execution_path(execution_id)
            return json.dumps([item.model_dump() for item in execution_outputs.list_outputs(execution_dir)], indent=2)

    @function_tool
    def preview_execution_output(execution_id: str, path: str) -> str:
        """Preview a workbook execution output file."""
        with optional_span(timer, "tool.preview_execution_output", execution_id=execution_id, path=path):
            preview = execution_outputs.preview_output(control_db.get_execution_path(execution_id), path)
            return preview.model_dump_json(indent=2)

    @function_tool
    def get_git_status() -> str:
        """Get git status for the current Arc workspace."""
        with optional_span(timer, "tool.get_git_status"):
            return json.dumps(
                {
                    "branch": git_service.branch(workspace_root),
                    "porcelain": git_service.status(workspace_root),
                },
                indent=2,
            )

    return [
        list_workspace_files,
        read_workspace_file,
        list_assets,
        save_asset,
        list_runs,
        save_run,
        list_workbook_templates,
        save_workbook_template,
        save_workbook_template_step,
        save_workbook_step,
        list_workbooks,
        save_workbook,
        compute_workbook,
        list_execution_outputs,
        preview_execution_output,
        get_git_status,
    ]
