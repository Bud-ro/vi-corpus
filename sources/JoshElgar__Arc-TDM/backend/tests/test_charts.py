from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.core import charts


def test_list_charts_hides_starter_when_real_charts_exist(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace_root = tmp_path / "workspace"
    starter_dir = workspace_root / "charts" / "starter_chart"
    real_dir = workspace_root / "charts" / "station_failure_rate"
    starter_dir.mkdir(parents=True)
    real_dir.mkdir(parents=True)
    (starter_dir / "chart.json").write_text(
        json.dumps({"id": "starter_chart", "title": "Starter Chart"}),
        encoding="utf-8",
    )
    (real_dir / "chart.json").write_text(
        json.dumps({"id": "station_failure_rate", "title": "Station Failure Rate"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(charts, "load_source_figure", lambda *args, **kwargs: {})

    summaries = charts.list_charts(workspace_root)

    assert [chart.id for chart in summaries] == ["station_failure_rate"]


def test_load_source_figure_reads_execution_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    workspace_root = tmp_path / "workspace"
    output_path = workspace_root / "executions" / "execution-1" / "outputs" / "chart.figure.json"
    output_path.parent.mkdir(parents=True)
    output_path.write_text(
        json.dumps({"data": [{"type": "bar", "x": ["A"], "y": [1]}], "layout": {}}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        charts.control_db,
        "get_execution_path",
        lambda execution_id: tmp_path / "stale" / execution_id,
    )

    figure = charts.load_source_figure(workspace_root, "outputs/chart.figure.json", "execution-1")

    assert figure["data"][0]["x"] == ["A"]
