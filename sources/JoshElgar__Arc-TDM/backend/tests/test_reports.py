from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.core import reports


def test_reports_are_html_only(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    execution_dir = tmp_path / "execution"
    outputs_dir = execution_dir / "outputs"
    outputs_dir.mkdir(parents=True)
    (outputs_dir / "summary.html").write_text("<h1>Summary</h1>\n", encoding="utf-8")
    (outputs_dir / "summary.txt").write_text("not html\n", encoding="utf-8")

    report = reports.register_report_from_output(
        workspace_root=workspace_root,
        execution_dir=execution_dir,
        execution_id="summary_execution",
        output_path="outputs/summary.html",
        report_id="summary",
        title="Summary",
    )

    assert report.format == "html"
    report_json = json.loads((workspace_root / "reports" / "summary" / "report.json").read_text(encoding="utf-8"))
    assert report_json["format"] == "html"
    assert report_json["source"]["output_path"] == "outputs/summary.html"

    with pytest.raises(ValueError, match="HTML"):
        reports.register_report_from_output(
            workspace_root=workspace_root,
            execution_dir=execution_dir,
            execution_id="summary_execution",
            output_path="outputs/summary.txt",
            report_id="summary_text",
            title="Summary Text",
        )


def test_report_titles_drop_action_prefixes(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    execution_dir = tmp_path / "execution"
    outputs_dir = execution_dir / "outputs"
    outputs_dir.mkdir(parents=True)
    (outputs_dir / "grip_force_report.html").write_text("<h1>Grip Force</h1>\n", encoding="utf-8")

    report = reports.register_report_from_output(
        workspace_root=workspace_root,
        execution_dir=execution_dir,
        execution_id="execution_1",
        output_path="outputs/grip_force_report.html",
        report_id="make_grip_force_report",
        title="Make Grip Force Report",
    )

    assert report.title == "Grip Force Report"
    report_json = json.loads(
        (workspace_root / "reports" / "make_grip_force_report" / "report.json").read_text(encoding="utf-8")
    )
    assert report_json["title"] == "Grip Force Report"


def test_existing_action_style_report_titles_display_cleanly(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    report_dir = workspace_root / "reports" / "make_grip_force_report"
    report_dir.mkdir(parents=True)
    (report_dir / "report.json").write_text(
        json.dumps(
            {
                "id": "make_grip_force_report",
                "title": "Make Grip Force Report",
                "kind": "report",
                "format": "html",
                "source": {"execution_id": "execution_1", "output_path": "outputs/grip_force_report.html"},
            }
        ),
        encoding="utf-8",
    )

    assert reports.list_reports(workspace_root)[0].title == "Grip Force Report"
