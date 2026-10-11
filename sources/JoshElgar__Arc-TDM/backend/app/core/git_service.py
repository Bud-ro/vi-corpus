from __future__ import annotations

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from app.config import settings
from app.schemas.domain import DiscardResponse


def _git(workspace_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=workspace_root,
        text=True,
        capture_output=True,
        check=False,
    )


def _check(workspace_root: Path, args: list[str]) -> str:
    result = _git(workspace_root, args)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def init_git(workspace_root: Path) -> None:
    if not (workspace_root / ".git").exists():
        _git(workspace_root, ["init"])
    _git(workspace_root, ["config", "user.name", "Arc Workspace"])
    _git(workspace_root, ["config", "user.email", "workspace@arc.local"])


def branch(workspace_root: Path) -> str:
    result = _git(workspace_root, ["branch", "--show-current"])
    return result.stdout.strip() or "main"


def status(workspace_root: Path) -> list[str]:
    result = _git(workspace_root, ["status", "--short"])
    return [line for line in result.stdout.splitlines() if line.strip()]


def is_dirty(workspace_root: Path) -> bool:
    return bool(status(workspace_root))


def head_commit(workspace_root: Path) -> str | None:
    result = _git(workspace_root, ["rev-parse", "HEAD"])
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def latest_commit_for_path(workspace_root: Path, relative_path: str) -> str | None:
    result = _git(workspace_root, ["log", "-n", "1", "--format=%H", "--", relative_path])
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def status_entries(workspace_root: Path) -> dict[str, str]:
    result = _git(workspace_root, ["status", "--porcelain"])
    entries: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        code = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        entries[path] = code
    return entries


def diff(workspace_root: Path) -> str:
    unstaged = _git(workspace_root, ["diff", "--", "."]).stdout
    staged = _git(workspace_root, ["diff", "--cached", "--", "."]).stdout
    return "\n".join(part for part in [staged, unstaged] if part.strip())


def commit_all(workspace_root: Path, message: str) -> str:
    _git(workspace_root, ["add", "."])
    result = _git(workspace_root, ["commit", "-m", message])
    if result.returncode != 0:
        return result.stderr.strip() or result.stdout.strip() or "Nothing to commit."
    return result.stdout.strip()


def commit_if_dirty(workspace_root: Path, message: str) -> str | None:
    if not is_dirty(workspace_root):
        return head_commit(workspace_root)
    _check(workspace_root, ["add", "."])
    _check(workspace_root, ["commit", "-m", message])
    commit = head_commit(workspace_root)
    if not commit:
        raise RuntimeError("Workspace git commit failed.")
    return commit


def commit_paths_if_dirty(workspace_root: Path, paths: list[str], message: str) -> str | None:
    clean_paths = [path for path in paths if path.strip()]
    if not clean_paths:
        return head_commit(workspace_root)
    _check(workspace_root, ["add", "-f", "--", *clean_paths])
    staged = _git(workspace_root, ["diff", "--cached", "--quiet", "--", *clean_paths])
    if staged.returncode == 0:
        return head_commit(workspace_root)
    _check(workspace_root, ["commit", "-m", message, "--", *clean_paths])
    commit = head_commit(workspace_root)
    if not commit:
        raise RuntimeError("Workspace git commit failed.")
    return commit


def ensure_committed(workspace_root: Path, message: str) -> str:
    commit = commit_if_dirty(workspace_root, message)
    if commit:
        return commit
    _check(workspace_root, ["commit", "--allow-empty", "-m", message])
    commit = head_commit(workspace_root)
    if not commit:
        raise RuntimeError("Workspace git has no commit.")
    return commit


def discard_changes(
    workspace_root: Path,
    paths: list[str],
    include_untracked: bool,
) -> DiscardResponse:
    entries = status_entries(workspace_root)
    requested = paths or sorted(entries)
    unknown = [path for path in requested if path not in entries]
    if unknown:
        raise ValueError(f"No visible git changes for: {', '.join(unknown)}")

    tracked = [path for path in requested if entries[path] != "??"]
    untracked = [path for path in requested if entries[path] == "??"]
    discarded_untracked = untracked if include_untracked else []
    skipped_untracked = [] if include_untracked else untracked
    backup_dir = _backup_before_discard(workspace_root, tracked, discarded_untracked)

    if tracked:
        result = _git(workspace_root, ["restore", "--staged", "--worktree", "--", *tracked])
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Failed to restore tracked changes.")

    for relative_path in discarded_untracked:
        target = _safe_workspace_path(workspace_root, relative_path)
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()

    return DiscardResponse(
        discarded_tracked=tracked,
        discarded_untracked=discarded_untracked,
        skipped_untracked=skipped_untracked,
        backup_path=str(backup_dir),
    )


def _backup_before_discard(
    workspace_root: Path,
    tracked: list[str],
    untracked: list[str],
) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_dir = settings.var_dir / "discards" / stamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "workspace": str(workspace_root),
        "tracked": tracked,
        "untracked": untracked,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (backup_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    if tracked:
        (backup_dir / "unstaged.patch").write_text(
            _git(workspace_root, ["diff", "--binary", "--", *tracked]).stdout,
            encoding="utf-8",
        )
        (backup_dir / "staged.patch").write_text(
            _git(workspace_root, ["diff", "--binary", "--cached", "--", *tracked]).stdout,
            encoding="utf-8",
        )
    for relative_path in untracked:
        source = _safe_workspace_path(workspace_root, relative_path)
        destination = backup_dir / "untracked" / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, destination, dirs_exist_ok=True)
        elif source.exists():
            shutil.copy2(source, destination)
    return backup_dir


def _safe_workspace_path(workspace_root: Path, relative_path: str) -> Path:
    target = (workspace_root / relative_path).resolve()
    if not str(target).startswith(str(workspace_root.resolve())):
        raise ValueError(f"Path escapes workspace: {relative_path}")
    return target
