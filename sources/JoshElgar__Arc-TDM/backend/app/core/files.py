from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import UploadFile

from app.core import duck, tdms
from app.schemas.domain import FileEntry, FilePreview, FileTablePage, UploadResponse, WorkspaceFileRead


TEXT_FILE_READ_LIMIT = 200_000
LOCAL_DATA_ROOT = Path("files/local")
SHARED_DATA_ROOT = Path("files/shared")
DATA_ROOTS = (LOCAL_DATA_ROOT, SHARED_DATA_ROOT)
HIDDEN_WORKSPACE_PATH_MARKERS = ("tdms_index",)
VISIBLE_DATA_FILE_EXTENSIONS = {
    ".arrow",
    ".csv",
    ".dat",
    ".docx",
    ".feather",
    ".h5",
    ".hdf5",
    ".htm",
    ".html",
    ".json",
    ".jsonl",
    ".jsx",
    ".log",
    ".md",
    ".ndjson",
    ".parquet",
    ".pdf",
    ".pq",
    ".py",
    ".sql",
    ".tdm",
    ".tdms",
    ".toml",
    ".tsv",
    ".ts",
    ".tsx",
    ".txt",
    ".xls",
    ".xlsx",
    ".xml",
    ".yaml",
    ".yml",
}
BINARY_PREVIEW_EXTENSIONS = {
    ".arrow",
    ".docx",
    ".feather",
    ".h5",
    ".hdf5",
    ".parquet",
    ".pdf",
    ".pq",
    ".tdms",
    ".xls",
    ".xlsx",
}
TABULAR_DATA_EXTENSIONS = {".csv", ".json", ".jsonl", ".ndjson", ".parquet", ".pq", ".tsv"}
HTML_DATA_EXTENSIONS = {".html", ".htm"}
DATA_FILE_MEDIA_TYPES = {
    ".htm": "text/html; charset=utf-8",
    ".html": "text/html; charset=utf-8",
}
DATASET_MEMBER_EXTENSIONS = {".csv", ".tdms", ".tsv"}
DATASET_CSV_EXTENSIONS = {".csv", ".tsv"}
DATASET_MEMBER_COLUMNS = ["file", "type", "size", "status"]
TDMS_DATASET_CATALOG_COLUMNS = [
    "group_name",
    "channel_name",
    "length",
    "dtype",
    "unit",
    "time_basis",
    "sample_rate_hz",
    "files",
    "properties",
]
TDMS_DATASET_SAMPLE_COLUMNS = ["sample_index", "file", "local_index", "timestamp", "elapsed_seconds", "value", "unit"]
CSV_DATASET_COLUMNS = ["column_name", "files"]
SKIPPED_WORKSPACE_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}


def is_hidden_workspace_path(path: Path | str) -> bool:
    return any(
        marker in part.lower()
        for part in Path(path).parts
        for marker in HIDDEN_WORKSPACE_PATH_MARKERS
    )


def safe_path(workspace_root: Path, relative_path: str) -> Path:
    root = workspace_root.resolve()
    target = (root / relative_path).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        raise ValueError("Path escapes workspace.")
    return target


def read_workspace_text_file(
    workspace_root: Path,
    relative_path: str,
    limit: int = TEXT_FILE_READ_LIMIT,
) -> WorkspaceFileRead:
    path = safe_path(workspace_root, relative_path)
    if not path.exists() or path.is_dir():
        raise FileNotFoundError(relative_path)
    visible_relative_path = _visible_relative_path(workspace_root, path)

    with path.open("rb") as handle:
        data = handle.read(limit + 1)
    truncated = len(data) > limit
    if truncated:
        data = data[:limit]

    stat = path.stat()
    return WorkspaceFileRead(
        path=visible_relative_path,
        name=path.name,
        language=language_for_path(path),
        size=stat.st_size,
        modified_at=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
        text=data.decode("utf-8", errors="replace"),
        truncated=truncated,
    )


def language_for_path(path: Path) -> str | None:
    return {
        ".css": "css",
        ".html": "html",
        ".js": "javascript",
        ".json": "json",
        ".jsx": "javascript",
        ".md": "markdown",
        ".py": "python",
        ".sql": "sql",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".txt": "text",
        ".yaml": "yaml",
        ".yml": "yaml",
    }.get(path.suffix.lower())


def list_files(workspace_root: Path) -> list[FileEntry]:
    entries: list[FileEntry] = []
    root = workspace_root.resolve()

    def visit(directory: Path) -> None:
        for path in sorted(directory.iterdir()):
            relative = path.relative_to(root).as_posix()
            if path.is_dir() and path.name in SKIPPED_WORKSPACE_DIRS:
                continue
            if is_hidden_workspace_path(relative):
                continue
            stat = path.stat()
            entries.append(
                FileEntry(
                    path=relative,
                    name=path.name,
                    kind="directory" if path.is_dir() else "file",
                    size=None if path.is_dir() else stat.st_size,
                    modified_at=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                )
            )
            if path.is_dir():
                visit(path)

    if not root.exists():
        return entries
    visit(root)
    return entries


def list_user_files(workspace_root: Path) -> list[FileEntry]:
    entries: list[FileEntry] = []
    dataset_paths = {
        metadata.get("path"): metadata
        for metadata in list_dataset_metadata(workspace_root)
        if isinstance(metadata.get("path"), str)
    }

    for relative_path, metadata in sorted(dataset_paths.items()):
        path = safe_path(workspace_root, relative_path)
        if not path.exists() or not path.is_dir():
            continue
        stat = path.stat()
        members = dataset_members(workspace_root, path)
        entries.append(
            FileEntry(
                path=_relative_source_path(workspace_root, path),
                name=path.name,
                kind="directory",
                size=sum(int(member["size"]) for member in members),
                modified_at=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                source_kind="dataset",
                dataset_kind=str(metadata.get("dataset_kind") or "mixed"),
                status="ready",
                member_count=len(members),
            )
        )

    for data_root in DATA_ROOTS:
        root = workspace_root / data_root
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(workspace_root).as_posix()
            if _is_inside_dataset(relative, dataset_paths):
                continue
            if is_hidden_workspace_path(relative):
                continue
            if not is_visible_data_file(path):
                continue
            stat = path.stat()
            entries.append(
                FileEntry(
                    path=relative,
                    name=path.name,
                    kind="file",
                    size=stat.st_size,
                    modified_at=datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                )
            )
    return sorted(entries, key=lambda entry: entry.path)


def list_data_files(workspace_root: Path) -> list[FileEntry]:
    return list_user_files(workspace_root)


def is_visible_data_file(path: Path | str) -> bool:
    return Path(path).suffix.lower() in VISIBLE_DATA_FILE_EXTENSIONS


def is_data_source_path(workspace_root: Path, path: Path) -> bool:
    resolved = path.resolve()
    for data_root in DATA_ROOTS:
        try:
            resolved.relative_to((workspace_root / data_root).resolve())
            return True
        except ValueError:
            continue
    return False


def data_file_path(workspace_root: Path, relative_path: str) -> Path:
    path = safe_path(workspace_root, relative_path)
    if not _is_data_file_path(workspace_root, path):
        raise ValueError("Only local or shared data files can be served.")
    if not path.exists() or path.is_dir() or not is_visible_data_file(path):
        raise FileNotFoundError(relative_path)
    return path


def data_file_media_type(path: Path) -> str:
    return DATA_FILE_MEDIA_TYPES.get(path.suffix.lower(), "application/octet-stream")


def delete_data_file(workspace_root: Path, relative_path: str) -> None:
    path = safe_path(workspace_root, relative_path)
    if not is_data_source_path(workspace_root, path):
        raise ValueError("Only local or shared data sources can be deleted.")
    if not path.exists():
        raise FileNotFoundError(relative_path)
    manifest_path = _relative_source_path(workspace_root, path)
    if path.is_dir():
        shutil.rmtree(path)
    else:
        if not is_visible_data_file(path):
            raise FileNotFoundError(relative_path)
        path.unlink()
    delete_manifest_for_file(workspace_root, manifest_path)
    if duck.db_path(workspace_root).exists():
        duck.prune_missing_source_files(workspace_root)


def delete_manifest_for_file(workspace_root: Path, relative_path: str) -> None:
    manifests_root = workspace_root / "files" / "manifests"
    if not manifests_root.exists():
        return
    for manifest in manifests_root.glob("*.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("path") == relative_path:
            manifest.unlink()


def preview_file(workspace_root: Path, relative_path: str) -> FilePreview:
    path = safe_path(workspace_root, relative_path)
    if not path.exists():
        raise FileNotFoundError(relative_path)
    if path.is_dir():
        metadata = describe_dataset(workspace_root, path)
        return FilePreview(
            path=_relative_source_path(workspace_root, path),
            kind=f"{metadata.get('dataset_kind', 'mixed')}_dataset",
            columns=DATASET_MEMBER_COLUMNS,
            rows=_dataset_member_rows(metadata)[:20],
            text="\n".join(str(issue) for issue in metadata.get("issues", [])) or None,
        )
    relative_path = _visible_relative_path(workspace_root, path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        columns, rows = duck.preview_tabular_file(path)
        return FilePreview(path=relative_path, kind=suffix.lstrip("."), columns=columns, rows=rows)
    if suffix == ".tdms":
        columns, rows, _ = tdms.catalog_page(
            workspace_root,
            path,
            relative_path,
            page=0,
            page_size=20,
        )
        return FilePreview(path=relative_path, kind="tdms", columns=columns, rows=rows)
    if suffix == ".json":
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            text = json.dumps(json.loads(text), indent=2)
        except json.JSONDecodeError:
            pass
        return FilePreview(path=relative_path, kind="json", text=text[:8000])
    text = path.read_text(encoding="utf-8", errors="replace")
    return FilePreview(path=relative_path, kind="text", text=text[:8000])


def table_file(
    workspace_root: Path,
    relative_path: str,
    page: int = 0,
    page_size: int = 100,
    tdms_group: str | None = None,
    tdms_channel: str | None = None,
) -> FileTablePage:
    path = safe_path(workspace_root, relative_path)
    if not path.exists():
        raise FileNotFoundError(relative_path)
    if path.is_dir():
        if not is_data_source_path(workspace_root, path):
            raise ValueError("Only local or shared data folders can be previewed.")
        return dataset_table_page(
            workspace_root,
            path,
            page=page,
            page_size=page_size,
            tdms_group=tdms_group,
            tdms_channel=tdms_channel,
        )
    relative_path = _visible_relative_path(workspace_root, path)

    page = max(page, 0)
    page_size = min(max(page_size, 1), 500)
    suffix = path.suffix.lower()
    kind = suffix.lstrip(".") or "file"

    if suffix == ".tdms":
        try:
            if tdms_group and tdms_channel:
                columns, rows, has_next = tdms.channel_page(
                    path,
                    tdms_group,
                    tdms_channel,
                    page,
                    page_size,
                )
                kind = "tdms_channel"
            else:
                columns, rows, has_next = tdms.catalog_page(
                    workspace_root,
                    path,
                    path.relative_to(workspace_root.resolve()).as_posix(),
                    page,
                    page_size,
                )
                kind = "tdms"
            return FileTablePage(
                path=relative_path,
                kind=kind,
                columns=columns,
                rows=rows,
                page=page,
                page_size=page_size,
                has_next=has_next,
            )
        except KeyError as exc:
            raise ValueError(str(exc)) from exc

    if suffix in TABULAR_DATA_EXTENSIONS:
        try:
            columns, rows, has_next = duck.table_page_for_file(workspace_root, path, page, page_size)
            return FileTablePage(
                path=relative_path,
                kind=kind,
                columns=columns,
                rows=rows,
                page=page,
                page_size=page_size,
                has_next=has_next,
            )
        except Exception:
            if suffix not in {".csv", ".tsv"}:
                raise
            columns, rows, has_next = duck.csv_page(path, page, page_size)
            return FileTablePage(
                path=relative_path,
                kind=kind,
                columns=columns,
                rows=rows,
                page=page,
                page_size=page_size,
                has_next=has_next,
            )

    if suffix == ".tdm":
        return FileTablePage(
            path=relative_path,
            kind="tdm",
            page=page,
            page_size=page_size,
            text="TDM preview is waiting on real sample files so Arc can choose the right parser path.",
        )

    if suffix in HTML_DATA_EXTENSIONS:
        return FileTablePage(
            path=relative_path,
            kind="html",
            page=page,
            page_size=page_size,
            text="Open the preview.",
        )

    if suffix in BINARY_PREVIEW_EXTENSIONS:
        label = suffix.lstrip(".").lower()
        return FileTablePage(
            path=relative_path,
            kind=kind,
            page=page,
            page_size=page_size,
            text=f"{label} preview is not available yet.",
        )

    text = path.read_text(encoding="utf-8", errors="replace")
    return FileTablePage(
        path=relative_path,
        kind=kind if kind != "file" else "text",
        page=page,
        page_size=page_size,
        text=text[:12000],
    )


def _visible_relative_path(workspace_root: Path, path: Path) -> str:
    relative_path = path.relative_to(workspace_root.resolve()).as_posix()
    if is_hidden_workspace_path(relative_path):
        raise FileNotFoundError(relative_path)
    return relative_path


async def upload_file(workspace_root: Path, upload: UploadFile) -> UploadResponse:
    return await upload_single_file(workspace_root, upload, destination="local")


async def upload_single_file(
    workspace_root: Path,
    upload: UploadFile,
    destination: str = "local",
    name: str | None = None,
) -> UploadResponse:
    target_dir = workspace_root / data_root_for(destination)
    target_dir.mkdir(parents=True, exist_ok=True)
    target_name = safe_data_name(name or Path(upload.filename or "upload.bin").name, fallback="upload.bin")
    target = target_dir / target_name
    if not is_visible_data_file(target):
        raise ValueError("Choose a supported data file.")
    with target.open("wb") as handle:
        shutil.copyfileobj(upload.file, handle)
    sha = duck.file_sha256(target)
    if target.suffix.lower() == ".tdms":
        table_name = None
        tdms.write_manifest(workspace_root.resolve(), target, sha)
    else:
        table_name = duck.ingest_file(target, workspace_root)
        manifest = workspace_root / "files" / "manifests" / f"{target.stem}.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "path": target.relative_to(workspace_root).as_posix(),
                    "sha256": sha,
                    "size": target.stat().st_size,
                    "duckdb_table": table_name,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return UploadResponse(
        path=target.relative_to(workspace_root).as_posix(),
        sha256=sha,
        size=target.stat().st_size,
        duckdb_table=table_name,
    )


async def upload_data_source(
    workspace_root: Path,
    uploads: list[UploadFile],
    destination: str,
    name: str | None = None,
) -> UploadResponse:
    clean_uploads = [upload for upload in uploads if upload.filename]
    if not clean_uploads:
        raise ValueError("Choose at least one file.")
    if len(clean_uploads) == 1:
        return await upload_single_file(workspace_root, clean_uploads[0], destination=destination, name=name)

    target_root = workspace_root / data_root_for(destination)
    target_root.mkdir(parents=True, exist_ok=True)
    dataset_name = safe_data_name(name or common_dataset_name(clean_uploads), fallback="dataset")
    target_dir = target_root / dataset_name
    target_dir.mkdir(parents=True, exist_ok=True)
    for upload in clean_uploads:
        member_name = safe_data_name(Path(upload.filename or "upload.bin").name, fallback="upload.bin")
        target = target_dir / member_name
        if target.exists():
            raise ValueError(f"Dataset already contains a file named {member_name}.")
        if not is_visible_data_file(target):
            raise ValueError(f"Choose supported data files. Unsupported file: {member_name}")
        with target.open("wb") as handle:
            shutil.copyfileobj(upload.file, handle)

    metadata = describe_dataset(workspace_root, target_dir)
    if metadata.get("status") == "ready":
        write_dataset_metadata(workspace_root, target_dir, str(metadata.get("dataset_kind") or "mixed"))
    return UploadResponse(
        path=str(metadata["path"]),
        size=int(metadata.get("size") or 0),
        kind="dataset",
        dataset_kind=str(metadata.get("dataset_kind") or "mixed"),
        status=str(metadata.get("status") or "ready"),
        member_count=int(metadata.get("member_count") or 0),
    )


def dataset_table_page(
    workspace_root: Path,
    path: Path,
    page: int = 0,
    page_size: int = 100,
    tdms_group: str | None = None,
    tdms_channel: str | None = None,
) -> FileTablePage:
    page = max(page, 0)
    page_size = min(max(page_size, 1), 500)
    metadata = describe_dataset(workspace_root, path)
    relative_path = str(metadata["path"])
    dataset_kind = str(metadata.get("dataset_kind") or "mixed")
    status = str(metadata.get("status") or "ready")
    issues = [str(issue) for issue in metadata.get("issues", []) if str(issue).strip()]

    if dataset_kind == "tdms" and status == "ready":
        if tdms_group and tdms_channel:
            return tdms_dataset_channel_page(
                workspace_root,
                metadata,
                tdms_group,
                tdms_channel,
                page,
                page_size,
            )
        rows = metadata.get("channels") if isinstance(metadata.get("channels"), list) else []
        offset = page * page_size
        page_rows = [_tdms_dataset_catalog_row(row) for row in rows[offset : offset + page_size + 1]]
        return FileTablePage(
            path=relative_path,
            kind="tdms_dataset",
            columns=TDMS_DATASET_CATALOG_COLUMNS,
            rows=page_rows[:page_size],
            page=page,
            page_size=page_size,
            has_next=len(page_rows) > page_size,
            row_count=len(rows),
        )

    if dataset_kind == "csv" and status == "ready":
        columns = metadata.get("columns") if isinstance(metadata.get("columns"), list) else []
        offset = page * page_size
        rows = [{"column_name": str(column), "files": metadata.get("member_count", 0)} for column in columns]
        page_rows = rows[offset : offset + page_size + 1]
        return FileTablePage(
            path=relative_path,
            kind="csv_dataset",
            columns=CSV_DATASET_COLUMNS,
            rows=page_rows[:page_size],
            page=page,
            page_size=page_size,
            has_next=len(page_rows) > page_size,
            row_count=len(rows),
        )

    rows = _dataset_member_rows(metadata)
    offset = page * page_size
    page_rows = rows[offset : offset + page_size + 1]
    return FileTablePage(
        path=relative_path,
        kind=f"{dataset_kind}_dataset",
        columns=DATASET_MEMBER_COLUMNS,
        rows=page_rows[:page_size],
        page=page,
        page_size=page_size,
        has_next=len(page_rows) > page_size,
        row_count=len(rows),
        text="\n".join(issues) if issues else None,
    )


def tdms_dataset_channel_page(
    workspace_root: Path,
    metadata: dict[str, Any],
    group_name: str,
    channel_name: str,
    page: int,
    page_size: int,
) -> FileTablePage:
    offset = page * page_size
    remaining_offset = offset
    rows: list[dict[str, Any]] = []
    has_next = False
    global_index = 0
    for member in metadata.get("members", []):
        if not isinstance(member, dict):
            continue
        member_path = safe_path(workspace_root, str(member.get("path") or ""))
        channel_summary = _member_channel_summary(member, group_name, channel_name)
        channel_length = int(channel_summary.get("length") or 0)
        if remaining_offset >= channel_length:
            remaining_offset -= channel_length
            global_index += channel_length
            continue
        read_count = page_size + 1 - len(rows)
        local_offset = remaining_offset
        member_rows = tdms_channel_rows(member_path, group_name, channel_name, local_offset, read_count)
        member_has_next = local_offset + len(member_rows) < channel_length
        for row in member_rows:
            local_index = int(row.get("sample_index") or 0)
            rows.append(
                {
                    "sample_index": global_index + local_index,
                    "file": Path(str(member.get("path") or "")).name,
                    "local_index": local_index,
                    "timestamp": row.get("timestamp"),
                    "elapsed_seconds": row.get("elapsed_seconds"),
                    "value": row.get("value"),
                    "unit": row.get("unit"),
                }
            )
        if member_has_next or len(rows) > page_size:
            has_next = True
            break
        remaining_offset = 0
        global_index += channel_length
    if len(rows) > page_size:
        has_next = True
    return FileTablePage(
        path=str(metadata["path"]),
        kind="tdms_dataset_channel",
        columns=TDMS_DATASET_SAMPLE_COLUMNS,
        rows=rows[:page_size],
        page=page,
        page_size=page_size,
        has_next=has_next,
        row_count=_tdms_dataset_channel_length(metadata, group_name, channel_name),
    )


def tdms_channel_rows(
    path: Path,
    group_name: str,
    channel_name: str,
    offset: int,
    count: int,
) -> list[dict[str, Any]]:
    with tdms.open_tdms(path) as tdms_file:
        group, channel = tdms.find_channel(tdms_file, group_name, channel_name)
        values = tdms.channel_values(channel, offset, count)
        properties = tdms.combined_properties(group, channel)
        unit = tdms.unit_for(properties)
        elapsed_values, timestamp_values = tdms.time_values(properties, offset, len(values))
    return [
        {
            "sample_index": offset + index,
            "timestamp": timestamp_values[index] if timestamp_values else None,
            "elapsed_seconds": elapsed_values[index] if elapsed_values else None,
            "value": tdms.json_safe(value),
            "unit": unit,
        }
        for index, value in enumerate(values)
    ]


def write_dataset_metadata(workspace_root: Path, path: Path, dataset_kind: str) -> dict[str, Any]:
    registration = {
        "kind": "dataset",
        "path": _relative_source_path(workspace_root, path),
        "dataset_kind": dataset_kind,
    }
    target = source_metadata_path(workspace_root, str(registration["path"]))
    target.parent.mkdir(parents=True, exist_ok=True)
    next_text = json.dumps(registration, indent=2) + "\n"
    if not target.exists() or target.read_text(encoding="utf-8") != next_text:
        target.write_text(next_text, encoding="utf-8")
    return registration


def create_dataset_metadata(workspace_root: Path, relative_path: str) -> dict[str, Any]:
    path = safe_path(workspace_root, relative_path)
    metadata = describe_dataset(workspace_root, path)
    if metadata.get("status") != "ready":
        issues = [str(issue) for issue in metadata.get("issues", []) if str(issue).strip()]
        detail = "; ".join(issues) if issues else "Folder is not an analysis-ready dataset."
        raise ValueError(detail)
    write_dataset_metadata(workspace_root, path, str(metadata.get("dataset_kind") or "mixed"))
    return metadata


def describe_dataset(workspace_root: Path, path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(path.as_posix())
    if not is_data_source_path(workspace_root, path):
        raise ValueError("Only local or shared data folders can be datasets.")

    members = dataset_members(workspace_root, path)
    metadata: dict[str, Any] = {
        "kind": "dataset",
        "path": _relative_source_path(workspace_root, path),
        "size": sum(int(member["size"]) for member in members),
        "member_count": len(members),
        "members": members,
    }
    metadata.update(classify_dataset(workspace_root, members))
    return metadata


def list_dataset_metadata(workspace_root: Path) -> list[dict[str, Any]]:
    manifests_root = workspace_root / "files" / "manifests"
    if not manifests_root.exists():
        return []
    rows: list[dict[str, Any]] = []
    for manifest in manifests_root.glob("*.json"):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("kind") == "dataset":
            rows.append(data)
    return rows


def classify_dataset(workspace_root: Path, members: list[dict[str, Any]]) -> dict[str, Any]:
    if not members:
        return {"dataset_kind": "mixed", "status": "invalid", "issues": ["Dataset folder has no supported data files."]}
    suffixes = {str(member["extension"]).lower() for member in members}
    if suffixes == {".tdms"}:
        return classify_tdms_dataset(workspace_root, members)
    if suffixes <= DATASET_CSV_EXTENSIONS:
        return classify_csv_dataset(workspace_root, members)
    return {
        "dataset_kind": "mixed",
        "status": "needs_review",
        "issues": ["Arc can store this folder, but analysis-ready validation supports sensor and tabular datasets only."],
    }


def classify_tdms_dataset(workspace_root: Path, members: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[str] = []
    channel_sets: list[list[dict[str, Any]]] = []
    for member in members:
        try:
            channels = tdms.scan_channels(safe_path(workspace_root, str(member["path"])))
        except Exception as exc:
            issues.append(f"{member['name']}: {exc}")
            channels = []
        member["channels"] = channels
        channel_sets.append(channels)
    if issues:
        return {"dataset_kind": "tdms", "status": "invalid", "issues": issues}
    expected = _channel_keys(channel_sets[0])
    for member, channels in zip(members[1:], channel_sets[1:]):
        if _channel_keys(channels) != expected:
            issues.append(f"{member['name']}: Sensor channels do not match the first file.")
    if issues:
        return {"dataset_kind": "tdms", "status": "invalid", "issues": issues}
    totals: list[dict[str, Any]] = []
    for base_channel in channel_sets[0]:
        key = _channel_key(base_channel)
        total_length = 0
        for channels in channel_sets:
            channel = next(item for item in channels if _channel_key(item) == key)
            total_length += int(channel.get("length") or 0)
        totals.append({**base_channel, "length": total_length, "files": len(members)})
    return {"dataset_kind": "tdms", "status": "ready", "issues": [], "channels": totals}


def classify_csv_dataset(workspace_root: Path, members: list[dict[str, Any]]) -> dict[str, Any]:
    issues: list[str] = []
    headers: list[list[str]] = []
    for member in members:
        try:
            header = csv_header(safe_path(workspace_root, str(member["path"])))
        except Exception as exc:
            issues.append(f"{member['name']}: {exc}")
            header = []
        member["columns"] = header
        headers.append(header)
    if issues:
        return {"dataset_kind": "csv", "status": "invalid", "issues": issues}
    expected = headers[0]
    for member, header in zip(members[1:], headers[1:]):
        if header != expected:
            issues.append(f"{member['name']}: Table columns do not match the first file.")
    if issues:
        return {"dataset_kind": "csv", "status": "invalid", "issues": issues}
    return {"dataset_kind": "csv", "status": "ready", "issues": [], "columns": expected}


def dataset_members(workspace_root: Path, path: Path, include_hash: bool = False) -> list[dict[str, Any]]:
    members: list[dict[str, Any]] = []
    for member_path in sorted(path.iterdir(), key=lambda item: item.name):
        if not member_path.is_file() or is_hidden_workspace_path(member_path):
            continue
        if member_path.suffix.lower() not in DATASET_MEMBER_EXTENSIONS:
            continue
        stat = member_path.stat()
        member = {
            "path": member_path.relative_to(workspace_root).as_posix(),
            "name": member_path.name,
            "extension": member_path.suffix.lower(),
            "size": stat.st_size,
        }
        if include_hash:
            member["sha256"] = duck.file_sha256(member_path)
        members.append(member)
    return members


def resolve_run_inputs(workspace_root: Path, input_paths: list[str]) -> dict[str, Any]:
    resolved: dict[str, Any] = {"input_paths": input_paths, "datasets": []}
    for input_path in input_paths:
        target = safe_path(workspace_root, input_path)
        if not target.exists() or not target.is_dir():
            continue
        metadata = describe_dataset(workspace_root, target)
        snapshotted_members = dataset_members(workspace_root, target, include_hash=True)
        resolved["datasets"].append(
            {
                "path": metadata["path"],
                "dataset_kind": metadata.get("dataset_kind"),
                "status": metadata.get("status"),
                "member_count": metadata.get("member_count"),
                "members": [
                    {
                        "path": member.get("path"),
                        "sha256": member.get("sha256"),
                        "size": member.get("size"),
                    }
                    for member in snapshotted_members
                    if isinstance(member, dict)
                ],
            }
        )
    return resolved


def data_root_for(destination: str) -> Path:
    if destination == "shared":
        return SHARED_DATA_ROOT
    if destination == "local":
        return LOCAL_DATA_ROOT
    raise ValueError("Choose Local or Shared as the upload destination.")


def safe_data_name(value: str, fallback: str) -> str:
    name = Path(value).name.strip()
    name = re.sub(r"[^A-Za-z0-9._ -]+", "_", name).strip(" .")
    return name or fallback


def common_dataset_name(uploads: list[UploadFile]) -> str:
    stems = [Path(upload.filename or "dataset").stem for upload in uploads]
    if not stems:
        return "dataset"
    prefix = stems[0]
    for stem in stems[1:]:
        while prefix and not stem.startswith(prefix):
            prefix = prefix[:-1]
    return prefix.rstrip(" _-.") or "dataset"


def source_metadata_path(workspace_root: Path, relative_path: str) -> Path:
    digest = hashlib.sha1(relative_path.encode("utf-8")).hexdigest()[:16]
    return workspace_root / "files" / "manifests" / f"{digest}.json"


def _relative_source_path(workspace_root: Path, path: Path) -> str:
    relative = _visible_relative_path(workspace_root, path)
    if path.is_dir() and not relative.endswith("/"):
        return f"{relative}/"
    return relative


def _is_inside_dataset(relative_path: str, dataset_paths: dict[str, Any]) -> bool:
    return any(relative_path != dataset_path and relative_path.startswith(str(dataset_path)) for dataset_path in dataset_paths)


def _dataset_member_rows(metadata: dict[str, Any]) -> list[dict[str, Any]]:
    issues = [str(issue) for issue in metadata.get("issues", []) if str(issue).strip()]
    issue_text = "; ".join(issues)
    rows: list[dict[str, Any]] = []
    for member in metadata.get("members", []):
        if not isinstance(member, dict):
            continue
        rows.append(
            {
                "file": member.get("name") or Path(str(member.get("path") or "")).name,
                "type": str(member.get("extension") or "").lstrip(".").lower(),
                "size": member.get("size"),
                "status": "Ready" if not issue_text else issue_text,
            }
        )
    return rows


def _tdms_dataset_catalog_row(channel: dict[str, Any]) -> dict[str, Any]:
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
        "files": channel.get("files"),
        "properties": properties_text,
    }


def _channel_key(channel: dict[str, Any]) -> tuple[str, str]:
    return (str(channel.get("group_name") or ""), str(channel.get("channel_name") or ""))


def _channel_keys(channels: list[dict[str, Any]]) -> list[tuple[str, str]]:
    return sorted(_channel_key(channel) for channel in channels)


def _member_channel_summary(member: dict[str, Any], group_name: str, channel_name: str) -> dict[str, Any]:
    for channel in member.get("channels", []):
        if not isinstance(channel, dict):
            continue
        if channel.get("group_name") == group_name and channel.get("channel_name") == channel_name:
            return channel
    return {}


def _tdms_dataset_channel_length(metadata: dict[str, Any], group_name: str, channel_name: str) -> int:
    total = 0
    for member in metadata.get("members", []):
        if isinstance(member, dict):
            total += int(_member_channel_summary(member, group_name, channel_name).get("length") or 0)
    return total


def csv_header(path: Path) -> list[str]:
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        return [value.strip() for value in next(reader)]


def _is_data_file_path(workspace_root: Path, path: Path) -> bool:
    return is_data_source_path(workspace_root, path)
