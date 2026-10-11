from __future__ import annotations

import asyncio
import io
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from app.core import files


def test_user_file_listing_hides_tdms_index_files(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    local_root = workspace_root / "files" / "local"
    shared_root = workspace_root / "files" / "shared"
    local_root.mkdir(parents=True)
    shared_root.mkdir(parents=True)
    (local_root / "line_quality.csv").write_text("line,failures\nA,3\n", encoding="utf-8")
    (local_root / "line_quality.tdms_index").write_text("generated index", encoding="utf-8")
    (local_root / "Line_Quality_TDMS_INDEX.json").write_text("{}", encoding="utf-8")
    (shared_root / "shared_quality.csv").write_text("line,failures\nB,1\n", encoding="utf-8")

    entries = files.list_user_files(workspace_root)

    assert [entry.path for entry in entries] == [
        "files/local/line_quality.csv",
        "files/shared/shared_quality.csv",
    ]


def test_user_file_listing_keeps_known_formats_and_hides_tmp_files(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    local_root = workspace_root / "files" / "local"
    local_root.mkdir(parents=True)
    (local_root / "line_quality.csv").write_text("line,failures\nA,3\n", encoding="utf-8")
    (local_root / "metadata.jsonl").write_text('{"line":"A"}\n', encoding="utf-8")
    (local_root / "preview.html").write_text("<h1>Preview</h1>\n", encoding="utf-8")
    (local_root / "samples.parquet").write_bytes(b"not real parquet")
    (local_root / ".line_quality.csv.tmp").write_text("temporary", encoding="utf-8")
    (local_root / "scratch.tmp").write_text("temporary", encoding="utf-8")
    (local_root / "script.py").write_text("print('not data')\n", encoding="utf-8")

    entries = files.list_user_files(workspace_root)

    assert [entry.path for entry in entries] == [
        "files/local/line_quality.csv",
        "files/local/metadata.jsonl",
        "files/local/preview.html",
        "files/local/samples.parquet",
        "files/local/script.py",
    ]


def test_user_file_listing_only_uses_local_and_shared_roots(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    local_root = workspace_root / "files" / "local"
    local_root.mkdir(parents=True)
    (local_root / "line_quality.csv").write_text("line,failures\nA,3\n", encoding="utf-8")
    code_path = workspace_root / "backend" / "app" / "core" / "workbooks.py"
    code_path.parent.mkdir(parents=True)
    code_path.write_text("print('workbook')\n", encoding="utf-8")

    entries = files.list_user_files(workspace_root)

    assert [entry.path for entry in entries] == ["files/local/line_quality.csv"]


def test_html_data_file_path_is_limited_to_visible_data_roots(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    html_path = workspace_root / "files" / "local" / "preview.html"
    html_path.parent.mkdir(parents=True)
    html_path.write_text("<h1>Preview</h1>\n", encoding="utf-8")
    outside_data_path = workspace_root / "reports" / "preview.html"
    outside_data_path.parent.mkdir(parents=True)
    outside_data_path.write_text("<h1>Report</h1>\n", encoding="utf-8")

    assert files.data_file_path(workspace_root, "files/local/preview.html") == html_path.resolve()
    assert files.data_file_media_type(html_path) == "text/html; charset=utf-8"
    with pytest.raises(ValueError, match="Only local or shared data files"):
        files.data_file_path(workspace_root, "reports/preview.html")
    with pytest.raises(FileNotFoundError):
        files.data_file_path(workspace_root, "files/local/scratch.tmp")


def test_workspace_file_listing_hides_tdms_index_files(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    (workspace_root / "notes.txt").write_text("keep", encoding="utf-8")
    (workspace_root / "line_quality.tdms_index").write_text("generated index", encoding="utf-8")

    entries = files.list_files(workspace_root)

    assert [entry.path for entry in entries] == ["notes.txt"]


def test_workspace_file_listing_skips_dependency_directories(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    (workspace_root / "notes.txt").write_text("keep", encoding="utf-8")
    dependency_file = workspace_root / "node_modules" / "package" / "index.js"
    dependency_file.parent.mkdir(parents=True)
    dependency_file.write_text("console.log('skip')\n", encoding="utf-8")

    entries = files.list_files(workspace_root)

    assert [entry.path for entry in entries] == ["notes.txt"]


def test_hidden_tdms_index_files_are_not_readable_as_workspace_text(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    hidden_path = workspace_root / "files" / "local" / "line_quality.tdms_index"
    hidden_path.parent.mkdir(parents=True)
    hidden_path.write_text("generated index", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        files.read_workspace_text_file(workspace_root, "files/local/line_quality.tdms_index")
    with pytest.raises(FileNotFoundError):
        files.preview_file(workspace_root, "files/local/line_quality.tdms_index")
    with pytest.raises(FileNotFoundError):
        files.table_file(workspace_root, "files/local/line_quality.tdms_index")


def test_tdms_file_lists_channel_catalog_from_source_file(
    tmp_path: Path,
    monkeypatch,
) -> None:
    workspace_root = tmp_path / "workspace"
    tdms_path = workspace_root / "files" / "local" / "line_quality.tdms"
    tdms_path.parent.mkdir(parents=True)
    tdms_path.write_bytes(b"tdms placeholder")
    monkeypatch.setitem(sys.modules, "nptdms", SimpleNamespace(TdmsFile=FakeTdmsFile))

    page = files.table_file(workspace_root, "files/local/line_quality.tdms", page=0, page_size=20)

    assert page.kind == "tdms"
    assert page.columns == [
        "group_name",
        "channel_name",
        "length",
        "dtype",
        "unit",
        "time_basis",
        "sample_rate_hz",
        "properties",
    ]
    assert page.rows == [
        {
            "group_name": "Station A",
            "channel_name": "Temperature",
            "length": 3,
            "dtype": "float64",
            "unit": "C",
            "time_basis": "elapsed_seconds",
            "sample_rate_hz": 2.0,
            "properties": '{"group.line": "A", "unit": "C", "wf_increment": "0.5"}',
        }
    ]


def test_tdms_channel_samples_are_read_on_demand(
    tmp_path: Path,
    monkeypatch,
) -> None:
    workspace_root = tmp_path / "workspace"
    tdms_path = workspace_root / "files" / "local" / "line_quality.tdms"
    tdms_path.parent.mkdir(parents=True)
    tdms_path.write_bytes(b"tdms placeholder")
    monkeypatch.setitem(sys.modules, "nptdms", SimpleNamespace(TdmsFile=FakeTdmsFile))

    page = files.table_file(
        workspace_root,
        "files/local/line_quality.tdms",
        page=0,
        page_size=2,
        tdms_group="Station A",
        tdms_channel="Temperature",
    )

    assert page.kind == "tdms_channel"
    assert page.columns == ["sample_index", "timestamp", "elapsed_seconds", "value", "unit"]
    assert page.has_next is True
    assert page.rows == [
        {
            "sample_index": 0,
            "timestamp": None,
            "elapsed_seconds": 0.0,
            "value": 21.0,
            "unit": "C",
        },
        {
            "sample_index": 1,
            "timestamp": None,
            "elapsed_seconds": 0.5,
            "value": 22.0,
            "unit": "C",
        },
    ]


def test_upload_writes_to_local_data_folder(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    upload = SimpleNamespace(
        filename="line_quality.csv",
        file=io.BytesIO(b"line,failures\nA,3\n"),
    )

    result = asyncio.run(files.upload_file(workspace_root, upload))

    assert result.path == "files/local/line_quality.csv"
    assert (workspace_root / result.path).exists()


def test_upload_accepts_chat_context_file_types(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    filenames = [
        "notes.md",
        "query.sql",
        "script.py",
        "app.tsx",
        "config.yaml",
        "settings.toml",
        "run.log",
        "manual.pdf",
        "brief.docx",
    ]

    for filename in filenames:
        upload = SimpleNamespace(
            filename=filename,
            file=io.BytesIO(b"saved for chat context"),
        )

        result = asyncio.run(files.upload_file(workspace_root, upload))

        assert result.path == f"files/local/{filename}"
        assert (workspace_root / result.path).exists()


def test_upload_rejects_unknown_data_extensions(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    upload = SimpleNamespace(
        filename="scratch.tmp",
        file=io.BytesIO(b"temporary"),
    )

    with pytest.raises(ValueError, match="supported data file"):
        asyncio.run(files.upload_file(workspace_root, upload))
    assert not (workspace_root / "files" / "local" / "scratch.tmp").exists()


def test_delete_data_file_rejects_non_data_paths(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    note = workspace_root / "notes.csv"
    note.parent.mkdir(parents=True)
    note.write_text("line,failures\nA,3\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Only local or shared data sources"):
        files.delete_data_file(workspace_root, "notes.csv")


def test_upload_multiple_csv_files_creates_dataset_folder(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    uploads = [
        SimpleNamespace(filename="run_0001.csv", file=io.BytesIO(b"time,temp\n0,21\n")),
        SimpleNamespace(filename="run_0002.csv", file=io.BytesIO(b"time,temp\n1,22\n")),
    ]

    result = asyncio.run(files.upload_data_source(workspace_root, uploads, "shared", "brake_run"))

    assert result.kind == "dataset"
    assert result.path == "files/shared/brake_run/"
    assert result.dataset_kind == "csv"
    assert result.status == "ready"
    assert result.member_count == 2
    assert (workspace_root / "files" / "shared" / "brake_run" / "run_0001.csv").exists()

    entries = files.list_user_files(workspace_root)
    assert [entry.path for entry in entries] == ["files/shared/brake_run/"]
    assert entries[0].source_kind == "dataset"
    assert entries[0].dataset_kind == "csv"
    manifests = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in (workspace_root / "files" / "manifests").glob("*.json")
    ]
    assert manifests == [
        {
            "kind": "dataset",
            "path": "files/shared/brake_run/",
            "dataset_kind": "csv",
        }
    ]

    page = files.table_file(workspace_root, "files/shared/brake_run/", page=0, page_size=20)
    assert page.kind == "csv_dataset"
    assert page.columns == ["column_name", "files"]
    assert page.rows == [
        {"column_name": "time", "files": 2},
        {"column_name": "temp", "files": 2},
    ]


def test_upload_multiple_csv_files_flags_column_mismatch(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    uploads = [
        SimpleNamespace(filename="run_0001.csv", file=io.BytesIO(b"time,temp\n0,21\n")),
        SimpleNamespace(filename="run_0002.csv", file=io.BytesIO(b"time,pressure\n1,9\n")),
    ]

    result = asyncio.run(files.upload_data_source(workspace_root, uploads, "local", "mixed_columns"))

    assert result.kind == "dataset"
    assert result.dataset_kind == "csv"
    assert result.status == "invalid"
    assert not (workspace_root / "files" / "manifests").exists()
    page = files.table_file(workspace_root, "files/local/mixed_columns/", page=0, page_size=20)
    assert page.kind == "csv_dataset"
    assert page.columns == ["file", "type", "size", "status"]
    assert "columns do not match" in (page.text or "")


def test_create_dataset_metadata_from_existing_folder_requires_ready_dataset(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    ready_dir = workspace_root / "files" / "local" / "ready"
    ready_dir.mkdir(parents=True)
    (ready_dir / "part_0001.csv").write_text("time,temp\n0,21\n", encoding="utf-8")
    (ready_dir / "part_0002.csv").write_text("time,temp\n1,22\n", encoding="utf-8")
    invalid_dir = workspace_root / "files" / "local" / "invalid"
    invalid_dir.mkdir(parents=True)
    (invalid_dir / "part_0001.csv").write_text("time,temp\n0,21\n", encoding="utf-8")
    (invalid_dir / "part_0002.csv").write_text("time,pressure\n1,9\n", encoding="utf-8")

    metadata = files.create_dataset_metadata(workspace_root, "files/local/ready/")

    assert metadata["path"] == "files/local/ready/"
    assert metadata["dataset_kind"] == "csv"
    assert metadata["status"] == "ready"
    entries = files.list_user_files(workspace_root)
    assert "files/local/ready/" in [entry.path for entry in entries]
    assert "files/local/invalid/" not in [entry.path for entry in entries]
    with pytest.raises(ValueError, match="columns do not match"):
        files.create_dataset_metadata(workspace_root, "files/local/invalid/")
    entries = files.list_user_files(workspace_root)
    assert "files/local/ready/" in [entry.path for entry in entries]
    assert "files/local/invalid/" not in [entry.path for entry in entries]


def test_table_file_reingests_changed_csv_on_open(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    csv_path = workspace_root / "files" / "local" / "line_quality.csv"
    csv_path.parent.mkdir(parents=True)
    csv_path.write_text("line,failures\nA,3\n", encoding="utf-8")

    first_page = files.table_file(workspace_root, "files/local/line_quality.csv", page=0, page_size=20)
    csv_path.write_text("line,failures\nA,9\n", encoding="utf-8")
    future_mtime = csv_path.stat().st_mtime + 5
    os.utime(csv_path, (future_mtime, future_mtime))

    second_page = files.table_file(workspace_root, "files/local/line_quality.csv", page=0, page_size=20)

    assert first_page.rows == [{"line": "A", "failures": 3}]
    assert second_page.rows == [{"line": "A", "failures": 9}]


class FakeTdmsFile:
    @staticmethod
    def read(path: Path) -> "FakeTdmsFile":
        assert path.name == "line_quality.tdms"
        return FakeTdmsFile()

    def groups(self) -> list["FakeGroup"]:
        return [FakeGroup()]


class FakeGroup:
    name = "Station A"
    properties = {"line": "A"}

    def channels(self) -> list["FakeChannel"]:
        return [FakeChannel()]


class FakeChannel:
    name = "Temperature"
    dtype = "float64"
    properties = {"unit": "C", "wf_increment": 0.5}
    values = [21.0, 22.0, 23.0]

    def __len__(self) -> int:
        return 3

    def __getitem__(self, item):
        return self.values[item]
