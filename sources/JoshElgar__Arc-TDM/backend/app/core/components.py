from __future__ import annotations

import csv
import json
import math
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from app.core import assets, duck, real_runs, workbooks
from app.schemas.domain import (
    AssetSummary,
    ComponentDocLink,
    ComponentModelDefinition,
    ComponentRecordingStartResponse,
    ComponentRecordingStopResponse,
    ComponentSample,
    ComponentWorkbookCreateRequest,
    TestRunWrite,
    WorkbookDataSource,
    WorkbookStep,
    WorkbookSummary,
    WorkbookTemplateWrite,
    WorkbookWrite,
)

COMPONENT_TEMPLATE_ID = "component-recording-review"
DEFAULT_SAMPLE_RATE_HZ = 25
MAX_SAMPLE_RATE_HZ = 100
MAX_STREAM_SAMPLES = 10_000
CSV_COLUMNS = [
    "timestamp",
    "asset_id",
    "component_model_id",
    "sequence",
    "ax_g",
    "ay_g",
    "az_g",
    "temperature_c",
    "event",
]


CATALOG = [
    ComponentModelDefinition(
        id="bosch-bmi270",
        name="Bosch BMI270",
        vendor="Bosch Sensortec",
        kind="6-axis IMU",
        description="Low-power accelerometer and gyroscope for wearable motion sensing.",
        default_sample_rate_hz=25,
        channels=[
            {"id": "ax_g", "label": "Accel X", "unit": "g"},
            {"id": "ay_g", "label": "Accel Y", "unit": "g"},
            {"id": "az_g", "label": "Accel Z", "unit": "g"},
            {"id": "temperature_c", "label": "Temperature", "unit": "C"},
        ],
        docs=[
            ComponentDocLink(label="Datasheet", url="https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi270/"),
            ComponentDocLink(label="SDK", url="https://github.com/boschsensortec/BMI270_SensorAPI"),
        ],
        notes="Simulator emits accelerometer and temperature channels for the MVP.",
    ),
    ComponentModelDefinition(
        id="st-iis2dlpc",
        name="STMicroelectronics IIS2DLPC",
        vendor="STMicroelectronics",
        kind="3-axis accelerometer",
        description="Ultra-low-power digital accelerometer for industrial sensing.",
        default_sample_rate_hz=25,
        channels=[
            {"id": "ax_g", "label": "Accel X", "unit": "g"},
            {"id": "ay_g", "label": "Accel Y", "unit": "g"},
            {"id": "az_g", "label": "Accel Z", "unit": "g"},
            {"id": "temperature_c", "label": "Temperature", "unit": "C"},
        ],
        docs=[
            ComponentDocLink(label="Product page", url="https://www.st.com/en/mems-and-sensors/iis2dlpc.html"),
            ComponentDocLink(label="Drivers", url="https://github.com/STMicroelectronics/iis2dlpc-pid"),
        ],
    ),
    ComponentModelDefinition(
        id="tdk-icm-42688-p",
        name="TDK ICM-42688-P",
        vendor="TDK InvenSense",
        kind="6-axis IMU",
        description="High-performance 6-axis motion sensor for inertial measurements.",
        default_sample_rate_hz=25,
        channels=[
            {"id": "ax_g", "label": "Accel X", "unit": "g"},
            {"id": "ay_g", "label": "Accel Y", "unit": "g"},
            {"id": "az_g", "label": "Accel Z", "unit": "g"},
            {"id": "temperature_c", "label": "Temperature", "unit": "C"},
        ],
        docs=[
            ComponentDocLink(label="Product page", url="https://invensense.tdk.com/products/motion-tracking/6-axis/icm-42688-p/"),
        ],
    ),
    ComponentModelDefinition(
        id="analog-adxl355",
        name="Analog Devices ADXL355",
        vendor="Analog Devices",
        kind="3-axis accelerometer",
        description="Low-noise precision MEMS accelerometer for vibration and tilt sensing.",
        default_sample_rate_hz=25,
        channels=[
            {"id": "ax_g", "label": "Accel X", "unit": "g"},
            {"id": "ay_g", "label": "Accel Y", "unit": "g"},
            {"id": "az_g", "label": "Accel Z", "unit": "g"},
            {"id": "temperature_c", "label": "Temperature", "unit": "C"},
        ],
        docs=[
            ComponentDocLink(label="Product page", url="https://www.analog.com/en/products/adxl355.html"),
        ],
    ),
]


@dataclass
class RecordingState:
    id: str
    workspace_id: str
    asset_id: str
    component_model_id: str
    sample_rate_hz: int
    started_at: str
    samples: list[ComponentSample] = field(default_factory=list)
    events: list[str] = field(default_factory=list)


@dataclass
class CompletedRecording:
    id: str
    asset_id: str
    component_model_id: str
    sample_rate_hz: int
    started_at: str
    stopped_at: str
    sample_count: int
    event_count: int
    file_path: str
    run_id: str


_LOCK = threading.Lock()
_ACTIVE_RECORDINGS: dict[tuple[str, str], RecordingState] = {}
_COMPLETED_RECORDINGS: dict[tuple[str, str], CompletedRecording] = {}
_PENDING_EVENTS: dict[tuple[str, str], list[str]] = {}


def list_component_models() -> list[ComponentModelDefinition]:
    return CATALOG


def get_component_model(component_model_id: str) -> ComponentModelDefinition:
    for component_model in CATALOG:
        if component_model.id == component_model_id:
            return component_model
    raise KeyError(component_model_id)


def get_asset_component(
    workspace_root: Path,
    asset_id: str,
) -> tuple[AssetSummary, ComponentModelDefinition]:
    asset = assets.get_asset(workspace_root, asset_id)
    if asset.asset_type != "component":
        raise ValueError("Asset is not a component.")
    if not asset.component_model_id:
        raise ValueError("Component asset has no supported model.")
    try:
        model = get_component_model(asset.component_model_id)
    except KeyError as exc:
        raise ValueError("Component asset model is not supported.") from exc
    return asset, model


def stream_samples(
    workspace_id: str,
    workspace_root: Path,
    asset_id: str,
    sample_rate_hz: int | None = None,
) -> Iterator[str]:
    asset, component_model = get_asset_component(workspace_root, asset_id)
    rate = _clean_sample_rate(sample_rate_hz or component_model.default_sample_rate_hz)
    started = time.monotonic()
    for sequence in range(MAX_STREAM_SAMPLES):
        elapsed = time.monotonic() - started
        sample = _sample_for(asset.id, component_model.id, sequence, elapsed)
        event = _consume_pending_event(workspace_id, asset.id)
        if event:
            sample = sample.model_copy(update={"event": event})
        _append_to_recording(workspace_id, asset.id, sample)
        yield f"data: {sample.model_dump_json()}\n\n"
        time.sleep(1 / rate)


def start_recording(
    workspace_id: str,
    workspace_root: Path,
    asset_id: str,
    sample_rate_hz: int | None = None,
) -> ComponentRecordingStartResponse:
    asset, component_model = get_asset_component(workspace_root, asset_id)
    rate = _clean_sample_rate(sample_rate_hz or component_model.default_sample_rate_hz)
    recording = RecordingState(
        id=f"{asset.id}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        workspace_id=workspace_id,
        asset_id=asset.id,
        component_model_id=component_model.id,
        sample_rate_hz=rate,
        started_at=utc_now(),
    )
    with _LOCK:
        _ACTIVE_RECORDINGS[(workspace_id, asset.id)] = recording
    return ComponentRecordingStartResponse(
        id=recording.id,
        asset_id=recording.asset_id,
        component_model_id=recording.component_model_id,
        sample_rate_hz=recording.sample_rate_hz,
        started_at=recording.started_at,
    )


def add_event(workspace_id: str, workspace_root: Path, asset_id: str, label: str) -> None:
    asset, _ = get_asset_component(workspace_root, asset_id)
    clean_label = label.strip()
    if not clean_label:
        raise ValueError("Event label is required.")
    with _LOCK:
        _PENDING_EVENTS.setdefault((workspace_id, asset.id), []).append(clean_label)
        recording = _ACTIVE_RECORDINGS.get((workspace_id, asset.id))
        if recording:
            recording.events.append(clean_label)


def stop_recording(
    workspace_id: str,
    workspace_root: Path,
    asset_id: str,
    recording_id: str,
) -> ComponentRecordingStopResponse:
    asset, component_model = get_asset_component(workspace_root, asset_id)
    with _LOCK:
        recording = _ACTIVE_RECORDINGS.pop((workspace_id, asset.id), None)
    if not recording or recording.id != recording_id:
        raise KeyError(recording_id)
    if not recording.samples:
        recording.samples.append(_sample_for(asset.id, component_model.id, 0, 0))

    stopped_at = utc_now()
    file_path = _write_recording_csv(workspace_root, recording)
    run_id = _save_recording_run(workspace_root, asset, component_model, recording, stopped_at).id
    completed = CompletedRecording(
        id=recording.id,
        asset_id=asset.id,
        component_model_id=component_model.id,
        sample_rate_hz=recording.sample_rate_hz,
        started_at=recording.started_at,
        stopped_at=stopped_at,
        sample_count=len(recording.samples),
        event_count=len(recording.events),
        file_path=file_path,
        run_id=run_id,
    )
    with _LOCK:
        _COMPLETED_RECORDINGS[(workspace_id, recording.id)] = completed
    return ComponentRecordingStopResponse(**completed.__dict__)


def create_workbook_from_recording(
    workspace_id: str,
    workspace_root: Path,
    asset_id: str,
    request: ComponentWorkbookCreateRequest,
) -> WorkbookSummary:
    with _LOCK:
        recording = _COMPLETED_RECORDINGS.get((workspace_id, request.recording_id))
    if recording is None:
        raise KeyError(request.recording_id)
    if recording.asset_id != asset_id:
        raise ValueError("Recording does not belong to this asset.")
    asset, component_model = get_asset_component(workspace_root, recording.asset_id)
    ensure_component_workbook_template(workspace_root)
    title = request.title.strip() if request.title and request.title.strip() else f"{asset.name} Recording Workbook"
    workbook_id = workbooks.slugify(f"{recording.id}-workbook")
    return workbooks.save_workbook(
        workspace_root,
        WorkbookWrite(
            id=workbook_id,
            title=title,
            template_id=COMPONENT_TEMPLATE_ID,
            linked_asset_id=asset.id,
            step_order=[],
            data_sources=[
                WorkbookDataSource(
                    id="recording",
                    name=f"{asset.name} Recording",
                    path=recording.file_path,
                    kind="file",
                    notes=f"Recorded at {recording.sample_rate_hz} Hz from the simulated component stream.",
                )
            ],
            tags=["component", "recording"],
            properties={
                "component_model_id": component_model.id,
                "recording_id": recording.id,
                "run_id": recording.run_id,
                "sample_rate_hz": str(recording.sample_rate_hz),
            },
            status="ready",
        ),
        workspace_id=workspace_id,
    )


def ensure_component_workbook_template(workspace_root: Path) -> None:
    template_dir = workspace_root / "workbook_templates" / "workbook" / COMPONENT_TEMPLATE_ID
    template_json = template_dir / "template.json"
    step = WorkbookStep(
        id="plot-recording",
        title="Plot Recording",
        prompt="Plot accelerometer axes over time and mark recorded events.",
        input_refs=["recording"],
        entrypoint="main.py",
        active=True,
    )
    if template_json.exists() and (template_dir / "steps" / step.id / "main.py").exists():
        return
    workbooks.save_template(
        workspace_root,
        WorkbookTemplateWrite(
            id=COMPONENT_TEMPLATE_ID,
            name="Component Recording Review",
            description="Starter workbook for component sensor recordings.",
            steps=[step.id],
            tags=["component"],
            properties={},
        ),
        steps=[step.model_copy(update={"script": COMPONENT_TEMPLATE_SCRIPT})],
    )


def _save_recording_run(
    workspace_root: Path,
    asset: AssetSummary,
    component_model: ComponentModelDefinition,
    recording: RecordingState,
    stopped_at: str,
):
    return real_runs.save_run(
        workspace_root,
        TestRunWrite(
            id=recording.id,
            name=f"{asset.name} Recording",
            asset_id=asset.id,
            start_time=recording.started_at,
            end_time=stopped_at,
            notes="Recorded from Arc's simulated component stream.",
            tags=["component", "recording", "simulated"],
            properties={
                "component_model_id": component_model.id,
                "recording_id": recording.id,
                "sample_rate_hz": str(recording.sample_rate_hz),
                "sample_count": str(len(recording.samples)),
                "event_count": str(len(recording.events)),
                "source": "simulated",
            },
        ),
    )


def _write_recording_csv(workspace_root: Path, recording: RecordingState) -> str:
    target_dir = workspace_root / "files" / "local" / "component-recordings" / recording.asset_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{recording.id}.csv"
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for sample in recording.samples:
            writer.writerow(sample.model_dump())
    sha = duck.file_sha256(target)
    table_name = duck.ingest_file(target, workspace_root)
    manifest = workspace_root / "files" / "manifests" / f"component-recording-{recording.id}.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "path": target.relative_to(workspace_root).as_posix(),
                "sha256": sha,
                "size": target.stat().st_size,
                "duckdb_table": table_name,
                "source": "component-recording",
                "asset_id": recording.asset_id,
                "component_model_id": recording.component_model_id,
                "recording_id": recording.id,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return target.relative_to(workspace_root).as_posix()


def _sample_for(asset_id: str, component_model_id: str, sequence: int, elapsed: float) -> ComponentSample:
    return ComponentSample(
        timestamp=utc_now(),
        asset_id=asset_id,
        component_model_id=component_model_id,
        sequence=sequence,
        ax_g=round(math.sin(elapsed * 2.4) * 0.45, 5),
        ay_g=round(math.cos(elapsed * 1.7) * 0.32, 5),
        az_g=round(1.0 + math.sin(elapsed * 0.8) * 0.08, 5),
        temperature_c=round(24.0 + math.sin(elapsed * 0.12) * 1.8, 3),
    )


def _append_to_recording(workspace_id: str, asset_id: str, sample: ComponentSample) -> None:
    with _LOCK:
        recording = _ACTIVE_RECORDINGS.get((workspace_id, asset_id))
        if recording:
            recording.samples.append(sample)


def _consume_pending_event(workspace_id: str, asset_id: str) -> str | None:
    with _LOCK:
        events = _PENDING_EVENTS.get((workspace_id, asset_id), [])
        if not events:
            return None
        return events.pop(0)


def _clean_sample_rate(value: int) -> int:
    return min(max(int(value or DEFAULT_SAMPLE_RATE_HZ), 1), MAX_SAMPLE_RATE_HZ)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


COMPONENT_TEMPLATE_SCRIPT = r'''from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--execution", required=True)
    parser.add_argument("--duckdb", required=True)
    args = parser.parse_args()

    workspace = Path(args.workspace)
    execution = Path(args.execution)
    target = json.loads((execution / "target.json").read_text(encoding="utf-8"))
    source = next((item for item in target.get("data_sources", []) if item.get("id") == "recording"), None)
    if not source:
        raise SystemExit("No component recording data source is attached.")

    data_path = workspace / source["path"]
    df = pd.read_csv(data_path)
    if df.empty:
        raise SystemExit("Component recording is empty.")

    elapsed = (pd.to_datetime(df["timestamp"]) - pd.to_datetime(df["timestamp"]).iloc[0]).dt.total_seconds()
    fig = go.Figure()
    for column, label in [("ax_g", "Accel X"), ("ay_g", "Accel Y"), ("az_g", "Accel Z")]:
        if column in df:
            fig.add_trace(go.Scatter(x=elapsed, y=df[column], mode="lines", name=label))

    event_rows = df[df.get("event", "").fillna("").astype(str).str.len() > 0]
    for _, row in event_rows.iterrows():
        x = elapsed.loc[row.name]
        fig.add_vline(x=x, line_width=1, line_dash="dot", annotation_text=str(row["event"]))

    fig.update_layout(
        title="Component Recording",
        xaxis_title="Elapsed seconds",
        yaxis_title="Acceleration (g)",
        height=420,
        margin={"l": 44, "r": 20, "t": 54, "b": 44},
    )
    outputs = execution / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    (outputs / "component-recording.figure.json").write_text(fig.to_json(), encoding="utf-8")


if __name__ == "__main__":
    main()
'''
