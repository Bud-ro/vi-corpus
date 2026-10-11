from __future__ import annotations

from collections import Counter
import os
from pathlib import Path

from app.config import settings
from app.core import control_db, project_settings
from app.core.agent_tools import build_workspace_tools
from app.core.timing import ChatTimer, optional_span


class SandboxService:
    """Agent boundary for the live workspace."""

    def __init__(self, workspace_root: Path, workspace_id: str = control_db.DEFAULT_WORKSPACE_ID):
        self.workspace_root = workspace_root
        self.workspace_id = workspace_id

    async def respond(self, prompt: str, timer: ChatTimer | None = None) -> str:
        with optional_span(timer, "sandbox.validate", mode=settings.sandbox_mode):
            setup_error = chat_setup_error()
            if setup_error:
                raise RuntimeError(setup_error)
        return await self._respond_with_openai_sandbox(prompt, timer)

    async def _respond_with_openai_sandbox(self, prompt: str, timer: ChatTimer | None = None) -> str:
        with optional_span(timer, "sandbox.imports"):
            from agents import Runner
            from agents.run import RunConfig
            from agents.sandbox import Manifest, SandboxAgent, SandboxRunConfig
            from agents.sandbox.sandboxes.unix_local import UnixLocalSandboxClient

        with optional_span(timer, "sandbox.agent_setup", workspace_root=self.workspace_root):
            manifest = Manifest(root=str(self.workspace_root))
            settings = project_settings.load_project_settings(self.workspace_root)
            agent = SandboxAgent(
                name="Arc Agent",
                tools=build_workspace_tools(self.workspace_root, workspace_id=self.workspace_id, timer=timer),
                instructions=(
                    f"{settings.agent_system_prompt}\n\n"
                    f"{project_settings.WORKBOOK_STEP_INSTRUCTION}\n\n"
                    f"{PRODUCT_LANGUAGE_INSTRUCTION}\n\n"
                    f"{FILE_DISPLAY_INSTRUCTION}"
                ),
                default_manifest=manifest,
            )
            run_config = RunConfig(
                sandbox=SandboxRunConfig(client=UnixLocalSandboxClient(), manifest=manifest),
            )

        with optional_span(timer, "sandbox.runner"):
            result = await Runner.run(
                agent,
                f"Work in the workspace root. User request:\n\n{prompt}",
                run_config=run_config,
            )
        if timer:
            timer.mark("sandbox.result", **_result_metadata(result))
        return str(result.final_output)


def _result_metadata(result) -> dict[str, object]:
    tool_calls = [
        item.tool_name
        for item in result.new_items
        if getattr(item, "type", None) == "tool_call_item" and getattr(item, "tool_name", None)
    ]
    item_counts = Counter(str(getattr(item, "type", type(item).__name__)) for item in result.new_items)
    return {
        "model_responses": len(result.raw_responses),
        "run_items": len(result.new_items),
        "tool_calls": len(tool_calls),
        "tools": ", ".join(tool_calls) or "none",
        "item_counts": ", ".join(f"{name}:{count}" for name, count in sorted(item_counts.items())) or "none",
        "last_response_id": result.last_response_id or "",
    }


def chat_setup_error() -> str | None:
    if settings.sandbox_mode != "openai":
        return "Arc Chat is not configured."
    if not os.getenv("OPENAI_API_KEY"):
        return "Arc Chat is not configured."
    return None


def chat_available() -> bool:
    return chat_setup_error() is None


FILE_DISPLAY_INSTRUCTION = """
File display:
- When the user asks to show, open, view, read, or display a workspace file,
  identify the workspace-relative path and answer briefly with that path.
- Do not paste the whole file contents into chat for display-only requests.
  Arc renders referenced workspace files in chat directly from the local filesystem.
- Read file contents only when you need to answer a question about what the file does.
""".strip()


PRODUCT_LANGUAGE_INSTRUCTION = """
Product language:
- Treat analytics, visualisations, and visualizations as requests for charts
  unless the user clearly asks for a report or workbook instead.
""".strip()
