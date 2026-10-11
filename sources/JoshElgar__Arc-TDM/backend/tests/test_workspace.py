from __future__ import annotations

from pathlib import Path

from app.core import workspace


def test_ensure_gitignore_ignores_data_folders(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()

    workspace.ensure_gitignore(workspace_root)

    assert (workspace_root / ".gitignore").read_text(encoding="utf-8") == (
        "*.duckdb\n"
        "*.sqlite\n"
        ".DS_Store\n"
        "files/local/\n"
        "files/shared/\n"
    )


def test_ensure_gitignore_preserves_existing_entries(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    gitignore = workspace_root / ".gitignore"
    gitignore.write_text("custom-cache/\n*.duckdb\n", encoding="utf-8")

    workspace.ensure_gitignore(workspace_root)

    assert gitignore.read_text(encoding="utf-8") == (
        "custom-cache/\n"
        "*.duckdb\n"
        "*.sqlite\n"
        ".DS_Store\n"
        "files/local/\n"
        "files/shared/\n"
    )
