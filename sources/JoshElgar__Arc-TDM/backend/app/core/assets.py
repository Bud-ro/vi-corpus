from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from app.schemas.domain import AssetSummary, AssetWrite

MAX_ASSET_TAGS = 10


def list_assets(workspace_root: Path) -> list[AssetSummary]:
    workspace_root = workspace_root.resolve()
    summaries: list[AssetSummary] = []
    for asset_json in sorted((workspace_root / "assets").glob("*/asset.json")):
        summaries.append(_summary_from_json(workspace_root, asset_json))
    return summaries


def get_asset(workspace_root: Path, asset_id: str) -> AssetSummary:
    workspace_root = workspace_root.resolve()
    asset_json = _asset_json_path(workspace_root, asset_id)
    if not asset_json.exists():
        raise FileNotFoundError(asset_id)
    return _summary_from_json(workspace_root, asset_json)


def save_asset(workspace_root: Path, asset: AssetWrite) -> AssetSummary:
    workspace_root = workspace_root.resolve()
    asset_id = slugify(asset.id or asset.name)
    if not asset_id:
        raise ValueError("Asset id or name is required.")
    tags = _clean_tags(asset.tags)
    if len(tags) > MAX_ASSET_TAGS:
        raise ValueError(f"Asset can have at most {MAX_ASSET_TAGS} labels.")
    _validate_relationships(workspace_root, asset_id, asset)
    clean = asset.model_copy(update={"id": asset_id, "tags": tags})
    asset_dir = workspace_root / "assets" / asset_id
    asset_dir.mkdir(parents=True, exist_ok=True)
    (asset_dir / "asset.json").write_text(clean.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return _summary_from_json(workspace_root, asset_dir / "asset.json")


def delete_asset(workspace_root: Path, asset_id: str) -> None:
    workspace_root = workspace_root.resolve()
    asset_dir = _safe_child_dir(workspace_root / "assets", asset_id)
    if not asset_dir.exists():
        raise FileNotFoundError(asset_id)
    if not asset_dir.is_dir():
        raise ValueError(f"Asset is not a directory: {asset_id}")
    if _count_components_for_asset(workspace_root, asset_id):
        raise ValueError("Remove or reassign this system's components before deleting it.")
    shutil.rmtree(asset_dir)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def _summary_from_json(workspace_root: Path, asset_json: Path) -> AssetSummary:
    asset_dir = asset_json.parent
    data = json.loads(asset_json.read_text(encoding="utf-8"))
    asset_id = str(data.get("id") or asset_dir.name)
    return AssetSummary(
        id=asset_id,
        name=str(data.get("name") or asset_id),
        asset_type=data["asset_type"],
        parent_asset_id=data.get("parent_asset_id"),
        component_model_id=data.get("component_model_id"),
        tags=_clean_tags(data.get("tags") if isinstance(data.get("tags"), list) else []),
        properties=_clean_properties(data.get("properties")),
        archived_at=data.get("archived_at") if isinstance(data.get("archived_at"), str) else None,
        path=asset_dir.relative_to(workspace_root).as_posix(),
        run_count=_count_runs_for_asset(workspace_root, asset_id),
        workbook_count=_count_workbooks_for_asset(workspace_root, asset_id),
        component_count=_count_components_for_asset(workspace_root, asset_id),
    )


def _validate_relationships(workspace_root: Path, asset_id: str, asset: AssetWrite) -> None:
    if asset.asset_type == "system":
        if asset.parent_asset_id:
            raise ValueError("System assets cannot have a parent asset.")
        if asset.component_model_id:
            raise ValueError("System assets cannot have a component model.")
        return

    if _count_components_for_asset(workspace_root, asset_id):
        raise ValueError("An asset with linked components must remain a system.")
    if asset.parent_asset_id == asset_id:
        raise ValueError("A component asset cannot be its own parent.")
    if not asset.parent_asset_id:
        return
    try:
        parent = get_asset(workspace_root, asset.parent_asset_id)
    except FileNotFoundError as exc:
        raise ValueError("Parent asset not found.") from exc
    if parent.asset_type != "system":
        raise ValueError("A component parent must be a system asset.")


def _asset_json_path(workspace_root: Path, asset_id: str) -> Path:
    return _safe_child_dir(workspace_root / "assets", asset_id) / "asset.json"


def _safe_child_dir(parent: Path, child_id: str) -> Path:
    parent = parent.resolve()
    target = (parent / child_id).resolve()
    if target.parent != parent:
        raise ValueError(f"Invalid id: {child_id}")
    return target


def _clean_tags(tags: object) -> list[str]:
    if not isinstance(tags, list):
        return []
    clean: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        value = str(tag).strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        clean.append(value)
    return clean


def _clean_properties(properties: object) -> dict[str, str]:
    if not isinstance(properties, dict):
        return {}
    return {str(key): str(value) for key, value in properties.items() if str(key).strip()}


def _count_runs_for_asset(workspace_root: Path, asset_id: str) -> int:
    count = 0
    for run_json in (workspace_root / "runs").glob("*/run.json"):
        try:
            data = json.loads(run_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("asset_id") == asset_id:
            count += 1
    return count


def _count_workbooks_for_asset(workspace_root: Path, asset_id: str) -> int:
    count = 0
    for workbook_json in (workspace_root / "workbooks").glob("*/workbook.json"):
        try:
            data = json.loads(workbook_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        linked_asset_id = str(data.get("linked_asset_id") or "").strip()
        if linked_asset_id == asset_id:
            count += 1
    return count


def _count_components_for_asset(workspace_root: Path, asset_id: str) -> int:
    count = 0
    for asset_json in (workspace_root / "assets").glob("*/asset.json"):
        try:
            data = json.loads(asset_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("asset_type") == "component" and data.get("parent_asset_id") == asset_id:
            count += 1
    return count


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
