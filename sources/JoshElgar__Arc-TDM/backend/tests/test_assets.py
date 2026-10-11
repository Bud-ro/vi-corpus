from __future__ import annotations

from pathlib import Path

import pytest

from app.core import assets
from app.schemas.domain import AssetWrite


def test_save_asset_rejects_more_than_ten_labels(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()

    with pytest.raises(ValueError, match="at most 10 labels"):
        assets.save_asset(
            workspace_root,
            AssetWrite(
                id="headset-01",
                name="Headset 01",
                asset_type="system",
                tags=[f"label-{index}" for index in range(11)],
            ),
        )


def test_save_asset_allows_ten_labels(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()

    saved = assets.save_asset(
        workspace_root,
        AssetWrite(
            id="headset-01",
            name="Headset 01",
            asset_type="system",
            tags=[f"label-{index}" for index in range(10)],
        ),
    )

    assert len(saved.tags) == 10


def test_component_must_link_to_a_system_asset(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    assets.save_asset(
        workspace_root,
        AssetWrite(id="sensor-a", name="Sensor A", asset_type="component"),
    )

    with pytest.raises(ValueError, match="parent must be a system"):
        assets.save_asset(
            workspace_root,
            AssetWrite(
                id="sensor-b",
                name="Sensor B",
                asset_type="component",
                parent_asset_id="sensor-a",
            ),
        )


def test_system_summary_counts_linked_components(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()
    assets.save_asset(workspace_root, AssetWrite(id="headset", name="Headset", asset_type="system"))
    assets.save_asset(
        workspace_root,
        AssetWrite(
            id="headset-imu",
            name="Headset IMU",
            asset_type="component",
            parent_asset_id="headset",
        ),
    )

    assert assets.get_asset(workspace_root, "headset").component_count == 1

    with pytest.raises(ValueError, match="before deleting"):
        assets.delete_asset(workspace_root, "headset")

    with pytest.raises(ValueError, match="must remain a system"):
        assets.save_asset(
            workspace_root,
            AssetWrite(id="headset", name="Headset", asset_type="component"),
        )
