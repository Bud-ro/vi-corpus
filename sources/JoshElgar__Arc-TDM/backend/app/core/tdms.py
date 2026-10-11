from __future__ import annotations

import datetime as dt
import json
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterator


CATALOG_COLUMNS = [
    "group_name",
    "channel_name",
    "length",
    "dtype",
    "unit",
    "time_basis",
    "sample_rate_hz",
    "properties",
]
SAMPLE_COLUMNS = ["sample_index", "timestamp", "elapsed_seconds", "value", "unit"]


def write_manifest(workspace_root: Path, path: Path, sha256: str) -> dict[str, Any]:
    workspace_root = workspace_root.resolve()
    path = path.resolve()
    relative_path = path.relative_to(workspace_root).as_posix()
    manifest = {
        "path": relative_path,
        "sha256": sha256,
        "size": path.stat().st_size,
        "kind": "tdms",
        "duckdb_table": None,
        "channels": scan_channels(path),
    }
    target = manifest_path(workspace_root, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def catalog_page(
    workspace_root: Path,
    path: Path,
    relative_path: str,
    page: int,
    page_size: int,
) -> tuple[list[str], list[dict[str, Any]], bool]:
    manifest = read_manifest(workspace_root, relative_path)
    channels = manifest.get("channels") if manifest else None
    if not isinstance(channels, list):
        channels = scan_channels(path)

    offset = page * page_size
    rows = [_catalog_row(channel) for channel in channels[offset : offset + page_size + 1]]
    return CATALOG_COLUMNS, rows[:page_size], len(rows) > page_size


def channel_page(
    path: Path,
    group_name: str,
    channel_name: str,
    page: int,
    page_size: int,
) -> tuple[list[str], list[dict[str, Any]], bool]:
    offset = page * page_size
    with open_tdms(path) as tdms_file:
        group, channel = find_channel(tdms_file, group_name, channel_name)
        values = channel_values(channel, offset, page_size + 1)
        properties = combined_properties(group, channel)
        unit = unit_for(properties)
        elapsed_values, timestamp_values = time_values(properties, offset, len(values))

    rows = [
        {
            "sample_index": offset + index,
            "timestamp": timestamp_values[index] if timestamp_values else None,
            "elapsed_seconds": elapsed_values[index] if elapsed_values else None,
            "value": json_safe(value),
            "unit": unit,
        }
        for index, value in enumerate(values[:page_size])
    ]
    return SAMPLE_COLUMNS, rows, len(values) > page_size


def scan_channels(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with open_tdms(path) as tdms_file:
        for group in tdms_file.groups():
            for channel in group.channels():
                properties = combined_properties(group, channel)
                increment = numeric_property(properties, "wf_increment")
                rows.append(
                    {
                        "group_name": group.name,
                        "channel_name": channel.name,
                        "length": len(channel),
                        "dtype": str(channel.dtype),
                        "unit": unit_for(properties),
                        "time_basis": time_basis_for(properties),
                        "sample_rate_hz": sample_rate_for(increment),
                        "properties": {
                            key: stringify_property(value) for key, value in properties.items()
                        },
                    }
                )
    return rows


def manifest_path(workspace_root: Path, path: Path) -> Path:
    return workspace_root / "files" / "manifests" / f"{path.stem}.json"


def read_manifest(workspace_root: Path, relative_path: str) -> dict[str, Any] | None:
    manifests_root = workspace_root / "files" / "manifests"
    if not manifests_root.exists():
        return None
    for manifest in manifests_root.glob("*.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("path") == relative_path and data.get("kind") == "tdms":
            return data
    return None


@contextmanager
def open_tdms(path: Path) -> Iterator[Any]:
    from nptdms import TdmsFile

    opened = TdmsFile.open(path) if hasattr(TdmsFile, "open") else TdmsFile.read(path)
    if hasattr(opened, "__enter__"):
        with opened as tdms_file:
            yield tdms_file
        return

    try:
        yield opened
    finally:
        close = getattr(opened, "close", None)
        if callable(close):
            close()


def find_channel(tdms_file: Any, group_name: str, channel_name: str) -> tuple[Any, Any]:
    for group in tdms_file.groups():
        if group.name != group_name:
            continue
        for channel in group.channels():
            if channel.name == channel_name:
                return group, channel
    raise KeyError(f"Sensor channel not found: {group_name}/{channel_name}")


def channel_values(channel: Any, offset: int, count: int) -> list[Any]:
    if count <= 0:
        return []
    stop = offset + count
    try:
        values = channel[offset:stop]
    except Exception:
        values = list(channel)[offset:stop]
    if hasattr(values, "tolist"):
        values = values.tolist()
    return list(values)


def combined_properties(group: Any, channel: Any) -> dict[str, Any]:
    return {
        **{f"group.{key}": value for key, value in group.properties.items()},
        **channel.properties,
    }


def _catalog_row(channel: Any) -> dict[str, Any]:
    properties = channel.get("properties")
    properties_text = json.dumps(properties, sort_keys=True) if isinstance(properties, dict) else "{}"
    return {
        "group_name": channel.get("group_name", ""),
        "channel_name": channel.get("channel_name", ""),
        "length": channel.get("length"),
        "dtype": channel.get("dtype", ""),
        "unit": channel.get("unit", ""),
        "time_basis": channel.get("time_basis", "sample_index"),
        "sample_rate_hz": channel.get("sample_rate_hz"),
        "properties": properties_text,
    }


def unit_for(properties: dict[str, Any]) -> str:
    for key in ["unit_string", "unit", "units", "Unit", "Units", "wf_yunit_string"]:
        value = properties.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def time_basis_for(properties: dict[str, Any]) -> str:
    increment = numeric_property(properties, "wf_increment")
    if increment is None:
        return "sample_index"
    if datetime_property(properties.get("wf_start_time")) is not None:
        return "absolute_timestamp"
    return "elapsed_seconds"


def sample_rate_for(increment: float | None) -> float | None:
    if increment is None or increment == 0:
        return None
    return 1.0 / increment


def time_values(
    properties: dict[str, Any],
    offset: int,
    count: int,
) -> tuple[list[float] | None, list[str] | None]:
    increment = numeric_property(properties, "wf_increment")
    if increment is None:
        return None, None

    start_offset = numeric_property(properties, "wf_start_offset") or 0.0
    elapsed = [start_offset + (offset + index) * increment for index in range(count)]
    start_time = datetime_property(properties.get("wf_start_time"))
    if start_time is None:
        return elapsed, None

    timestamps = [
        (start_time + dt.timedelta(seconds=seconds)).isoformat()
        for seconds in elapsed
    ]
    return elapsed, timestamps


def numeric_property(properties: dict[str, Any], key: str) -> float | None:
    value = properties.get(key)
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def datetime_property(value: Any) -> dt.datetime | None:
    if value is None:
        return None
    if isinstance(value, dt.datetime):
        return value
    as_datetime = getattr(value, "as_datetime", None)
    if callable(as_datetime):
        converted = as_datetime()
        if isinstance(converted, dt.datetime):
            return converted
    if isinstance(value, str):
        try:
            return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def json_safe(value: Any) -> Any:
    item = getattr(value, "item", None)
    if callable(item):
        try:
            return json_safe(item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    return value


def stringify_property(value: Any) -> str:
    safe_value = json_safe(value)
    if isinstance(safe_value, (dict, list)):
        return json.dumps(safe_value, sort_keys=True)
    return str(safe_value)
