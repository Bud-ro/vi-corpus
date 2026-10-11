from __future__ import annotations

import json
from pathlib import Path

from app.config import settings
from app.core import duck, git_service, project_settings


WORKSPACE_GITIGNORE_LINES = [
    "*.duckdb",
    "*.sqlite",
    ".DS_Store",
    "files/local/",
    "files/shared/",
]


def default_workspace_root() -> Path:
    return settings.workspace_root


def ensure_workspace(root: Path, name: str = "Arc Default Workspace") -> Path:
    for path in [
        root / "files" / "local",
        root / "files" / "shared",
        root / "files" / "manifests",
        root / "mappings",
        root / "assets",
        root / "runs",
        root / "workbook_templates",
        root / "workbooks",
        root / "executions",
        root / "charts",
        root / "reports",
    ]:
        path.mkdir(parents=True, exist_ok=True)

    project_json = root / "project.json"
    if not project_json.exists():
        project_json.write_text(
            json.dumps(
                {
                    "name": name,
                    "description": "Sandbox-owned workspace for assets, runs, workbooks, data, charts, and reports.",
                    "agent_system_prompt": project_settings.DEFAULT_AGENT_SYSTEM_PROMPT,
                    "version": 1,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    ensure_default_workbook_templates(root)
    ensure_gitignore(root)

    git_service.init_git(root)
    duck.init_duckdb(root)
    duck.prune_missing_source_files(root)
    return root


def ensure_default_workbook_templates(root: Path) -> None:
    template_dir = root / "workbook_templates" / "workbook" / "blank-workbook"
    template_json = template_dir / "template.json"
    if template_json.exists():
        return
    template_dir.mkdir(parents=True, exist_ok=True)
    template_json.write_text(
        json.dumps(
            {
                "id": "blank-workbook",
                "name": "Blank Workbook",
                "description": "Starter workbook for assets, runs, and data.",
                "steps": [],
                "tags": [],
                "properties": {},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def ensure_default_workspace() -> Path:
    return ensure_workspace(default_workspace_root())


def ensure_gitignore(root: Path) -> None:
    gitignore = root / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8").splitlines() if gitignore.exists() else []
    next_lines = existing[:]
    changed = False
    for line in WORKSPACE_GITIGNORE_LINES:
        if line not in existing:
            next_lines.append(line)
            changed = True
    if changed or not gitignore.exists():
        gitignore.write_text("\n".join(next_lines).rstrip() + "\n", encoding="utf-8")
