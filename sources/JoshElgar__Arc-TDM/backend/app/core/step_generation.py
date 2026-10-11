from __future__ import annotations

import ast
import json
import os
from pathlib import Path
from typing import Any

from app.core import files, sandbox, workbooks
from app.core.report_style import REPORT_HTML_CONTRACT
from app.schemas.domain import WorkbookStep


async def generate_workbook_step(
    workspace_root: Path,
    workbook_id: str,
    title: str,
    prompt: str,
    input_refs: list[str],
    workspace_id: str | None = None,
) -> WorkbookStep:
    setup_error = sandbox.chat_setup_error()
    if setup_error:
        raise RuntimeError(setup_error)

    workbook = workbooks.get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)
    selected_sources = _selected_sources(workbook, input_refs)

    response = await _ask_model(
        system=_system_prompt(),
        user=_user_prompt(
            workspace_root=workspace_root,
            workbook_title=workbook.title,
            requested_title=title,
            requested_prompt=prompt,
            data_sources=[source.model_dump() for source in selected_sources],
        ),
    )
    payload = _parse_json_object(response)
    generated_title = str(payload.get("title") or title or "").strip()
    generated_prompt = str(payload.get("prompt") or prompt or "").strip()
    script = str(payload.get("script") or "").strip()
    if not generated_title:
        raise ValueError("Generated step did not include a title.")
    if not script:
        raise ValueError("Generated step did not include Python.")
    script = await _validate_or_repair_python(script)
    step_id = workbooks.slugify(generated_title)
    if not step_id:
        raise ValueError("Generated step title could not be converted to an id.")
    return WorkbookStep(
        id=step_id,
        title=generated_title,
        prompt=generated_prompt,
        input_refs=input_refs,
        entrypoint="main.py",
        script=script,
        active=False,
    )


async def revise_workbook_step(
    workspace_root: Path,
    workbook_id: str,
    step_id: str,
    instruction: str,
    input_refs: list[str],
    workspace_id: str | None = None,
) -> WorkbookStep:
    setup_error = sandbox.chat_setup_error()
    if setup_error:
        raise RuntimeError(setup_error)

    clean_instruction = instruction.strip()
    if not clean_instruction:
        raise ValueError("Describe what should change before revising the step.")

    workbook = workbooks.get_workbook(workspace_root, workbook_id, workspace_id=workspace_id)
    current_step = _workbook_step(workspace_root, workbook_id, step_id)
    next_input_refs = input_refs or current_step.input_refs
    selected_sources = _selected_sources(workbook, next_input_refs)

    response = await _ask_model(
        system=_system_prompt(),
        user=_revision_user_prompt(
            workspace_root=workspace_root,
            workbook_title=workbook.title,
            instruction=clean_instruction,
            current_step=current_step,
            data_sources=[source.model_dump() for source in selected_sources],
        ),
    )
    payload = _parse_json_object(response)
    revised_title = str(payload.get("title") or current_step.title or "").strip()
    revised_prompt = str(payload.get("prompt") or current_step.prompt or clean_instruction).strip()
    script = str(payload.get("script") or "").strip()
    if not revised_title:
        raise ValueError("Revised step did not include a title.")
    if not script:
        raise ValueError("Revised step did not include Python.")
    script = await _validate_or_repair_python(script)
    return current_step.model_copy(
        update={
            "title": revised_title,
            "prompt": revised_prompt,
            "input_refs": next_input_refs,
            "script": script,
        }
    )


async def _ask_model(system: str, user: str) -> str:
    from openai import AsyncOpenAI

    client = AsyncOpenAI()
    model = os.getenv("ARC_STEP_GENERATION_MODEL", os.getenv("OPENAI_MODEL", "gpt-4.1"))
    completion = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
    )
    content = completion.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty response.")
    return content


def _system_prompt() -> str:
    return f"""
You generate real Arc workbook steps. Return only JSON with:
{{
  "title": "short user-facing step title",
  "prompt": "short user-facing description of what the step does",
  "script": "complete Python source for main.py"
}}

The Python script must be specific to the user's requested work.
It must not be a generic starter or placeholder.

Step boundary:
- Generate one conceptually coherent, independently runnable unit of work.
- The step must have one clear responsibility and one independently useful result.
- Include only the loading, validation, and transformation needed for that result.
- Do not expand the step to also create unrelated checks, charts, reports, metrics, or cleaned datasets.
- Read required Workbook Data directly. Do not rely on temporary state or outputs from another step.
- Prefer a little repeated, obvious loading code over hidden coupling to another step.
- Keep the title and description narrow enough to state the step's single purpose.

Runtime contract:
- The script is run as: python main.py --workspace <workspace-root> --execution <execution-dir> --duckdb <duckdb-path>
- Read execution context from <execution-dir>/target.json.
- Workbook Data, when selected, is in target["data_sources"].
- Prefer selected Workbook Data when the requested work needs data. Do not invent or hardcode absolute local paths.
- Steps may do useful workspace work without selected data.
- If the step writes files, write them under <execution-dir>/outputs and create parent directories first.

Optional panel contract:
- A Plotly chart panel is created by writing outputs/<name>.figure.json containing a Plotly figure dict.
- A report panel is created by writing outputs/<name>.html.
- A check panel is created by writing outputs/checks/<name>.json with id, name, status, severity, and message.
- Only create panel outputs when the requested work calls for visible workbook panels.
- Some valid steps do not create charts, reports, checks, or other outputs.

When a step writes an HTML report:
{REPORT_HTML_CONTRACT}

Available libraries include pandas, numpy, duckdb, plotly, and nptdms.
Keep code readable, defensive, and small. Raise clear errors for missing selected data.
""".strip()


async def _validate_or_repair_python(script: str) -> str:
    try:
        _validate_python(script)
        return script
    except ValueError as exc:
        repaired = await _repair_python(script, str(exc))
        _validate_python(repaired)
        return repaired


async def _repair_python(script: str, error: str) -> str:
    response = await _ask_model(
        system=_repair_system_prompt(),
        user=json.dumps({"syntax_error": error, "script": script}, indent=2),
    )
    payload = _parse_json_object(response)
    repaired = str(payload.get("script") or "").strip()
    if not repaired:
        raise ValueError("Python repair did not return a script.")
    return repaired


def _repair_system_prompt() -> str:
    return """
You repair Python syntax errors in Arc workbook step scripts. Return only JSON with:
{
  "script": "complete corrected Python source for main.py"
}

Rules:
- Preserve the script's behavior and outputs.
- Fix only syntax problems.
- Do not introduce placeholder code.
""".strip()


def _user_prompt(
    workspace_root: Path,
    workbook_title: str,
    requested_title: str,
    requested_prompt: str,
    data_sources: list[dict[str, Any]],
) -> str:
    return json.dumps(
        {
            "workbook_title": workbook_title,
            "requested_title": requested_title,
            "requested_description": requested_prompt,
            "selected_workbook_data": [
                {
                    **source,
                    "preview": _preview_source(workspace_root, str(source.get("path") or "")),
                }
                for source in data_sources
            ],
        },
        indent=2,
    )


def _revision_user_prompt(
    workspace_root: Path,
    workbook_title: str,
    instruction: str,
    current_step: WorkbookStep,
    data_sources: list[dict[str, Any]],
) -> str:
    return json.dumps(
        {
            "task": "Revise the current Arc workbook step. Return the complete revised step content, not a patch.",
            "workbook_title": workbook_title,
            "change_instruction": instruction,
            "current_step": current_step.model_dump(),
            "selected_workbook_data": [
                {
                    **source,
                    "preview": _preview_source(workspace_root, str(source.get("path") or "")),
                }
                for source in data_sources
            ],
        },
        indent=2,
    )


def _selected_sources(workbook, input_refs: list[str]):
    selected_ids = set(input_refs)
    return [source for source in workbook.data_sources if source.id in selected_ids]


def _workbook_step(workspace_root: Path, workbook_id: str, step_id: str) -> WorkbookStep:
    for step in workbooks.list_workbook_steps(workspace_root, workbook_id):
        if step.id == step_id:
            return step
    raise FileNotFoundError(step_id)


def _preview_source(workspace_root: Path, path: str) -> dict[str, Any]:
    if not path:
        return {"error": "No path"}
    try:
        preview = files.preview_file(workspace_root, path)
    except Exception as exc:
        return {"error": str(exc)}
    rows = preview.rows[:5]
    text = preview.text[:2000] if preview.text else None
    return {
        "kind": preview.kind,
        "columns": preview.columns[:50],
        "rows": rows,
        "text": text,
    }


def _parse_json_object(content: str) -> dict[str, Any]:
    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("The model did not return valid JSON.") from exc
    if not isinstance(payload, dict):
        raise ValueError("The model response must be a JSON object.")
    return payload


def _validate_python(script: str) -> None:
    try:
        ast.parse(script)
    except SyntaxError as exc:
        location = f"line {exc.lineno}"
        if exc.offset:
            location += f", column {exc.offset}"
        line = _script_line(script, exc.lineno)
        detail = f" near: {line.strip()}" if line else ""
        raise ValueError(f"Generated Python has a syntax error at {location}: {exc.msg}{detail}") from exc


def _script_line(script: str, line_number: int | None) -> str:
    if not line_number:
        return ""
    lines = script.splitlines()
    if line_number < 1 or line_number > len(lines):
        return ""
    return lines[line_number - 1]
