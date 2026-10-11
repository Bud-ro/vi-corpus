from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from app.core import output_kinds
from app.schemas.domain import (
    CheckResult,
    ExecutionChecks,
    ExecutionLogEntry,
    ExecutionLogs,
    ExecutionOutput,
    ExecutionOutputPreview,
)

CHECK_OUTPUT_ROOT = "outputs/checks"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_path(execution_dir: Path) -> Path:
    return execution_dir / "logs.jsonl"


def append_log(
    execution_dir: Path,
    message: str,
    level: str = "info",
    step_id: str | None = None,
    source: str = "runner",
) -> None:
    execution_dir.mkdir(parents=True, exist_ok=True)
    next_seq = log_count(execution_dir) + 1
    entry = ExecutionLogEntry(
        seq=next_seq,
        timestamp=utc_now(),
        level=level,
        message=message,
        step_id=step_id,
        source=source,
    )
    with log_path(execution_dir).open("a", encoding="utf-8") as handle:
        handle.write(entry.model_dump_json() + "\n")


def read_log_entries(execution_dir: Path) -> list[ExecutionLogEntry]:
    path = log_path(execution_dir)
    if not path.exists():
        return []
    return [
        ExecutionLogEntry.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def read_logs(execution_dir: Path, execution_id: str, limit: int = 20000) -> ExecutionLogs:
    entries = read_log_entries(execution_dir)
    text = "\n".join(_render_log_entry(entry) for entry in entries)
    if len(text) > limit:
        text = text[-limit:]
    return ExecutionLogs(execution_id=execution_id, entries=entries, text=text)


async def stream_logs(execution_dir: Path):
    seen = 0
    while True:
        entries = read_log_entries(execution_dir)
        for entry in entries[seen:]:
            yield f"data: {entry.model_dump_json()}\n\n"
        seen = len(entries)
        if entries and entries[-1].source == "runner" and entries[-1].message in {"Execution completed."}:
            break
        if entries and entries[-1].source == "runner" and entries[-1].message.startswith("Execution failed:"):
            break
        await asyncio.sleep(0.75)


def list_outputs(execution_dir: Path) -> list[ExecutionOutput]:
    outputs_dir = execution_dir / "outputs"
    if not outputs_dir.exists():
        return []
    outputs: list[ExecutionOutput] = []
    for path in sorted(outputs_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(execution_dir).as_posix()
        outputs.append(
            ExecutionOutput(
                path=relative,
                name=path.name,
                kind=output_kinds.infer_output_kind(relative),
                size=path.stat().st_size,
            )
        )
    return outputs


def preview_output(execution_dir: Path, relative_path: str) -> ExecutionOutputPreview:
    target = (execution_dir / relative_path).resolve()
    if not str(target).startswith(str(execution_dir.resolve())) or not target.exists() or target.is_dir():
        raise FileNotFoundError(relative_path)
    kind = output_kinds.infer_output_kind(relative_path)
    text = target.read_text(encoding="utf-8", errors="replace")
    if target.suffix.lower() == ".json":
        return ExecutionOutputPreview(path=relative_path, kind=kind, json_value=json.loads(text))
    return ExecutionOutputPreview(path=relative_path, kind=kind, text=text[:20000])


def read_check_results(execution_dir: Path) -> list[CheckResult]:
    summary_path = execution_dir / "outputs" / "summary.json"
    if summary_path.exists():
        data = json.loads(summary_path.read_text(encoding="utf-8"))
        checks = data.get("checks") if isinstance(data, dict) else []
        return [CheckResult.model_validate(check) for check in checks if isinstance(check, dict)]
    checks_dir = execution_dir / CHECK_OUTPUT_ROOT
    if not checks_dir.exists():
        return []
    results: list[CheckResult] = []
    for path in sorted(checks_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            data["output_path"] = path.relative_to(execution_dir).as_posix()
            results.append(CheckResult.model_validate(data))
    return results


def read_checks(execution_dir: Path, execution_id: str) -> ExecutionChecks:
    return ExecutionChecks(execution_id=execution_id, checks=read_check_results(execution_dir))


def log_count(execution_dir: Path) -> int:
    path = log_path(execution_dir)
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def check_counts(execution_dir: Path) -> dict[str, int]:
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for result in read_check_results(execution_dir):
        counts[result.status] += 1
    return counts


def _render_log_entry(entry: ExecutionLogEntry) -> str:
    step = f" {entry.step_id}" if entry.step_id else ""
    return f"{entry.timestamp} {entry.level} {entry.source}{step} {entry.message}"
