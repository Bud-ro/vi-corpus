from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path
from typing import Any

import duckdb

from app.schemas.domain import DuckQueryResponse


def db_path(workspace_root: Path) -> Path:
    return workspace_root / "workspace.duckdb"


def connect(workspace_root: Path) -> duckdb.DuckDBPyConnection:
    workspace_root.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(db_path(workspace_root)))


def init_duckdb(workspace_root: Path) -> None:
    with connect(workspace_root) as conn:
        _ensure_source_files_table(conn)


def prune_missing_source_files(workspace_root: Path) -> None:
    with connect(workspace_root) as conn:
        _ensure_source_files_table(conn)
        rows = conn.execute("select path from source_files").fetchall()
        missing = [
            row[0]
            for row in rows
            if not (workspace_root / str(row[0])).exists()
        ]
        if missing:
            conn.executemany("delete from source_files where path = ?", [(path,) for path in missing])


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def table_name_for(path: Path, sha256: str) -> str:
    stem = re.sub(r"[^a-zA-Z0-9_]+", "_", path.stem).strip("_").lower() or "file"
    return f"src_{stem}_{sha256[:8]}"


def quote_ident(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def ingest_file(path: Path, workspace_root: Path) -> str | None:
    workspace_root = workspace_root.resolve()
    path = path.resolve()
    sha = file_sha256(path)
    stat = path.stat()
    kind = path.suffix.lower().lstrip(".") or "file"
    relative_path = path.relative_to(workspace_root).as_posix()
    table_name: str | None = None
    with connect(workspace_root) as conn:
        _ensure_source_files_table(conn)
        if kind in {"csv", "tsv"}:
            table_name = table_name_for(path, sha)
            escaped_path = str(path).replace("'", "''")
            conn.execute(
                f"create or replace table {quote_ident(table_name)} as "
                f"select * from read_csv_auto('{escaped_path}')"
            )
        elif kind in {"json", "jsonl", "ndjson"}:
            table_name = table_name_for(path, sha)
            escaped_path = str(path).replace("'", "''")
            conn.execute(
                f"create or replace table {quote_ident(table_name)} as "
                f"select * from read_json_auto('{escaped_path}')"
            )
        elif kind in {"parquet", "pq"}:
            table_name = table_name_for(path, sha)
            escaped_path = str(path).replace("'", "''")
            conn.execute(
                f"create or replace table {quote_ident(table_name)} as "
                f"select * from read_parquet('{escaped_path}')"
            )
        conn.execute("delete from source_files where path = ?", (relative_path,))
        conn.execute(
            """
            insert or replace into source_files
            (path, sha256, kind, table_name, source_size, source_mtime)
            values (?, ?, ?, ?, ?, ?)
            """,
            (relative_path, sha, kind, table_name, stat.st_size, stat.st_mtime),
        )
    return table_name


def query(workspace_root: Path, sql: str, limit: int = 200) -> DuckQueryResponse:
    lowered = sql.strip().lower()
    if not lowered.startswith(("select", "with", "show", "describe")):
        raise ValueError("Only read-only DuckDB queries are allowed from the UI.")
    with connect(workspace_root) as conn:
        result = conn.execute(sql)
        columns = [desc[0] for desc in result.description or []]
        rows = [dict(zip(columns, row, strict=False)) for row in result.fetchmany(limit)]
    return DuckQueryResponse(columns=columns, rows=rows)


def preview_tabular_file(path: Path) -> tuple[list[str], list[dict[str, Any]]]:
    if path.suffix.lower() in {".csv", ".tsv"}:
        with path.open(newline="", encoding="utf-8", errors="replace") as handle:
            dialect = "excel-tab" if path.suffix.lower() == ".tsv" else "excel"
            reader = csv.DictReader(handle, dialect=dialect)
            rows = [row for _, row in zip(range(20), reader, strict=False)]
            return list(reader.fieldnames or []), rows
    return [], []


def table_page_for_file(
    workspace_root: Path,
    path: Path,
    page: int,
    page_size: int,
) -> tuple[list[str], list[dict[str, Any]], bool]:
    workspace_root = workspace_root.resolve()
    path = path.resolve()
    relative_path = path.relative_to(workspace_root).as_posix()
    table_name = _table_for_file(workspace_root, path, relative_path)
    if not table_name:
        return [], [], False

    offset = page * page_size
    with connect(workspace_root) as conn:
        result = conn.execute(
            f"select * from {quote_ident(table_name)} limit ? offset ?",
            (page_size + 1, offset),
        )
        columns = [desc[0] for desc in result.description or []]
        raw_rows = result.fetchall()
    rows = [dict(zip(columns, (_json_safe(value) for value in row), strict=False)) for row in raw_rows[:page_size]]
    return columns, rows, len(raw_rows) > page_size


def csv_page(path: Path, page: int, page_size: int) -> tuple[list[str], list[dict[str, Any]], bool]:
    offset = page * page_size
    with path.open(newline="", encoding="utf-8", errors="replace") as handle:
        dialect = "excel-tab" if path.suffix.lower() == ".tsv" else "excel"
        reader = csv.DictReader(handle, dialect=dialect)
        columns = list(reader.fieldnames or [])
        rows: list[dict[str, Any]] = []
        has_next = False
        for index, row in enumerate(reader):
            if index < offset:
                continue
            if len(rows) >= page_size:
                has_next = True
                break
            rows.append(dict(row))
    return columns, rows, has_next


def _table_for_file(workspace_root: Path, path: Path, relative_path: str) -> str | None:
    workspace_root = workspace_root.resolve()
    path = path.resolve()
    suffix = path.suffix.lower().lstrip(".")
    if suffix not in {"csv", "json", "jsonl", "ndjson", "parquet", "pq", "tsv"}:
        return None

    with connect(workspace_root) as conn:
        _ensure_source_files_table(conn)
        row = conn.execute(
            """
            select table_name, source_size, source_mtime from source_files
            where path = ? and table_name is not null
            order by imported_at desc
            limit 1
            """,
            (relative_path,),
        ).fetchone()
    if row and row[0] and _cache_is_fresh(path, row[1], row[2]):
        return str(row[0])
    return ingest_file(path, workspace_root)


def _ensure_source_files_table(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute(
        """
        create table if not exists source_files (
          path varchar primary key,
          sha256 varchar not null,
          kind varchar not null,
          table_name varchar,
          source_size ubigint,
          source_mtime double,
          imported_at timestamp default current_timestamp
        )
        """
    )
    conn.execute("alter table source_files add column if not exists source_size ubigint")
    conn.execute("alter table source_files add column if not exists source_mtime double")


def _cache_is_fresh(path: Path, source_size: Any, source_mtime: Any) -> bool:
    if source_size is None or source_mtime is None:
        return False
    try:
        cached_size = int(source_size)
        cached_mtime = float(source_mtime)
    except (TypeError, ValueError):
        return False
    stat = path.stat()
    return stat.st_size == cached_size and stat.st_mtime <= cached_mtime


def _json_safe(value: Any) -> Any:
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    return value


def _stringify_property(value: Any) -> str:
    safe_value = _json_safe(value)
    if isinstance(safe_value, (dict, list)):
        return json.dumps(safe_value, sort_keys=True)
    return str(safe_value)
