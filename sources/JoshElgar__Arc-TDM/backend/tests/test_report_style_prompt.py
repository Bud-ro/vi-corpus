from __future__ import annotations

import asyncio
import json

import pytest

from app.core import project_settings, step_generation


def test_report_shell_is_in_step_generation_prompt() -> None:
    prompt = step_generation._system_prompt()

    assert "arc-report-canvas" in prompt
    assert "arc-report-page" in prompt
    assert "arc-report-figure" in prompt
    assert "Avoid triple-quoted Python strings" not in prompt


def test_step_generation_prompt_enforces_a_narrow_independent_step() -> None:
    prompt = step_generation._system_prompt()

    assert "one clear responsibility" in prompt
    assert "one independently useful result" in prompt
    assert "Do not expand the step" in prompt
    assert "Read required Workbook Data directly" in prompt
    assert "Prefer a little repeated, obvious loading code" in prompt


def test_generated_python_error_includes_location_and_line() -> None:
    with pytest.raises(ValueError) as exc_info:
        step_generation._validate_python('html = """<html>\\n<body>\\n')

    message = str(exc_info.value)
    assert "line 1" in message
    assert "unterminated triple-quoted string literal" in message
    assert 'html = """<html>' in message


def test_invalid_generated_python_is_repaired_once(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict] = []

    async def fake_ask_model(system: str, user: str) -> str:
        calls.append({"system": system, "user": json.loads(user)})
        return json.dumps({"script": "html = '<html>\\n<body>\\n'"})

    monkeypatch.setattr(step_generation, "_ask_model", fake_ask_model)

    script = asyncio.run(step_generation._validate_or_repair_python('html = """<html>\\n<body>\\n'))

    assert script == "html = '<html>\\n<body>\\n'"
    assert len(calls) == 1
    assert "unterminated triple-quoted string literal" in calls[0]["user"]["syntax_error"]


def test_failed_python_repair_still_raises_syntax_error(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_ask_model(system: str, user: str) -> str:
        return json.dumps({"script": 'html = """still broken'})

    monkeypatch.setattr(step_generation, "_ask_model", fake_ask_model)

    with pytest.raises(ValueError, match="Generated Python has a syntax error"):
        asyncio.run(step_generation._validate_or_repair_python('html = """<html>\\n<body>\\n'))


def test_report_shell_is_in_agent_prompt() -> None:
    prompt = project_settings.DEFAULT_AGENT_SYSTEM_PROMPT

    assert "arc-report-canvas" in prompt
    assert "arc-report-page" in prompt
    assert "arc-report-figure" in prompt
