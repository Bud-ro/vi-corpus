from __future__ import annotations

from pathlib import Path

from app.core import assets, components, workspace
from app.schemas.domain import AssetWrite, ComponentWorkbookCreateRequest


def test_component_catalog_has_initial_parts() -> None:
    ids = {component.id for component in components.list_component_models()}

    assert {
        "bosch-bmi270",
        "st-iis2dlpc",
        "tdk-icm-42688-p",
        "analog-adxl355",
    } <= ids


def test_component_recording_writes_normal_arc_artifacts(tmp_path: Path) -> None:
    workspace_root = workspace.ensure_workspace(tmp_path / "workspace")
    workspace_id = "workspace-1"
    assets.save_asset(
        workspace_root,
        AssetWrite(
            id="headset-imu",
            name="Headset IMU",
            asset_type="component",
            component_model_id="bosch-bmi270",
        ),
    )
    started = components.start_recording(workspace_id, workspace_root, "headset-imu", sample_rate_hz=5)
    stream = components.stream_samples(workspace_id, workspace_root, "headset-imu", sample_rate_hz=5)
    next(stream)
    components.add_event(workspace_id, workspace_root, "headset-imu", "shake event")
    next(stream)

    stopped = components.stop_recording(
        workspace_id,
        workspace_root,
        "headset-imu",
        started.id,
    )

    assert stopped.sample_count == 2
    assert stopped.event_count == 1
    assert stopped.asset_id == "headset-imu"
    assert (workspace_root / stopped.file_path).exists()
    assert (workspace_root / "assets" / stopped.asset_id / "asset.json").exists()
    assert (workspace_root / "runs" / stopped.run_id / "run.json").exists()
    assert "shake event" in (workspace_root / stopped.file_path).read_text(encoding="utf-8")


def test_component_recording_creates_workbook_with_attached_file(tmp_path: Path) -> None:
    workspace_root = workspace.ensure_workspace(tmp_path / "workspace")
    workspace_id = "workspace-1"
    assets.save_asset(
        workspace_root,
        AssetWrite(
            id="precision-accelerometer",
            name="Precision Accelerometer",
            asset_type="component",
            component_model_id="analog-adxl355",
        ),
    )
    started = components.start_recording(workspace_id, workspace_root, "precision-accelerometer")

    stopped = components.stop_recording(
        workspace_id,
        workspace_root,
        "precision-accelerometer",
        started.id,
    )
    workbook = components.create_workbook_from_recording(
        workspace_id,
        workspace_root,
        "precision-accelerometer",
        request=ComponentWorkbookCreateRequest(recording_id=stopped.id),
    )

    assert workbook.linked_asset_id == stopped.asset_id
    assert workbook.template_id == components.COMPONENT_TEMPLATE_ID
    assert workbook.data_sources[0].path == stopped.file_path
    assert (workspace_root / "workbooks" / workbook.id / "steps" / "plot-recording" / "main.py").exists()


def test_recording_rejects_system_assets(tmp_path: Path) -> None:
    workspace_root = workspace.ensure_workspace(tmp_path / "workspace")
    assets.save_asset(
        workspace_root,
        AssetWrite(id="headset", name="Headset", asset_type="system"),
    )

    try:
        components.start_recording("workspace-1", workspace_root, "headset")
    except ValueError as exc:
        assert str(exc) == "Asset is not a component."
    else:
        raise AssertionError("System asset should not start a component recording")
