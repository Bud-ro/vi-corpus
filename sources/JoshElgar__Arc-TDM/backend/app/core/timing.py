from __future__ import annotations

from contextlib import contextmanager, nullcontext
from time import perf_counter
from typing import Iterator

from app.schemas.domain import ChatActivityEvent


class ChatTimer:
    """Small request timer for understanding SandboxAgent latency."""

    def __init__(self) -> None:
        self._started_at = perf_counter()
        self._spans: list[dict] = []

    @contextmanager
    def span(self, name: str, **metadata: object) -> Iterator[None]:
        started_at = perf_counter()
        status = "ok"
        error_name: str | None = None
        try:
            yield
        except Exception as exc:
            status = "error"
            error_name = type(exc).__name__
            raise
        finally:
            finished_at = perf_counter()
            clean_metadata = {
                key: str(value)
                for key, value in metadata.items()
                if value is not None
            }
            if error_name:
                clean_metadata["error"] = error_name
            self._spans.append(
                {
                    "name": name,
                    "started_ms": self._ms(started_at - self._started_at),
                    "duration_ms": self._ms(finished_at - started_at),
                    "status": status,
                    "metadata": clean_metadata,
                }
            )

    def finish(self) -> dict:
        return {
            "total_ms": self._ms(perf_counter() - self._started_at),
            "spans": list(self._spans),
        }

    def mark(self, name: str, **metadata: object) -> None:
        elapsed = self._ms(perf_counter() - self._started_at)
        self._spans.append(
            {
                "name": name,
                "started_ms": elapsed,
                "duration_ms": 0,
                "status": "ok",
                "metadata": {
                    key: str(value)
                    for key, value in metadata.items()
                    if value is not None
                },
            }
        )

    @staticmethod
    def _ms(seconds: float) -> float:
        return round(seconds * 1000, 2)


def optional_span(timer: ChatTimer | None, name: str, **metadata: object):
    if timer is None:
        return nullcontext()
    return timer.span(name, **metadata)


ACTIVITY_LABELS = {
    "tool.list_workspace_files": "Checked workspace files",
    "tool.read_workspace_file": "Read a file",
    "tool.list_assets": "Checked assets",
    "tool.save_asset": "Saved asset",
    "tool.list_runs": "Checked runs",
    "tool.save_run": "Saved run",
    "tool.list_workbook_templates": "Checked workbook templates",
    "tool.save_workbook_template": "Saved workbook template",
    "tool.save_workbook_step": "Saved workbook step",
    "tool.list_workbooks": "Checked workbooks",
    "tool.save_workbook": "Saved workbook",
    "tool.compute_workbook": "Started workbook execution",
    "tool.list_execution_outputs": "Checked execution outputs",
    "tool.preview_execution_output": "Previewed execution output",
    "tool.get_git_status": "Checked workspace status",
}

ACTIVITY_DETAIL_FIELDS = {
    "tool.read_workspace_file": "path",
    "tool.save_asset": "asset_id",
    "tool.save_run": "run_id",
    "tool.save_workbook_template": "template_id",
    "tool.save_workbook_step": "template_id",
    "tool.save_workbook": "workbook_id",
    "tool.compute_workbook": "workbook_id",
    "tool.preview_execution_output": "path",
}


def activity_from_trace(trace: dict) -> list[ChatActivityEvent]:
    events: list[ChatActivityEvent] = []
    for span in trace.get("spans", []):
        if not isinstance(span, dict):
            continue
        name = str(span.get("name") or "")
        label = ACTIVITY_LABELS.get(name)
        if not label:
            continue
        metadata = span.get("metadata") if isinstance(span.get("metadata"), dict) else {}
        detail_field = ACTIVITY_DETAIL_FIELDS.get(name)
        detail = str(metadata.get(detail_field)) if detail_field and metadata.get(detail_field) else None
        events.append(
            ChatActivityEvent(
                label=label,
                status="error" if span.get("status") == "error" else "ok",
                detail=detail,
                duration_ms=span.get("duration_ms") if isinstance(span.get("duration_ms"), (int, float)) else None,
            )
        )
    return events
