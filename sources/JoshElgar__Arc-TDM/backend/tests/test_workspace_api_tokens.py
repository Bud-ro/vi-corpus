from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.core import control_db
from app.main import app


@pytest.fixture()
def isolated_app_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    original_root = settings.root_dir
    original_sandbox_mode = settings.sandbox_mode
    object.__setattr__(settings, "root_dir", tmp_path)
    object.__setattr__(settings, "sandbox_mode", "openai")
    monkeypatch.delenv("VITE_CLERK_PUBLISHABLE_KEY", raising=False)
    monkeypatch.delenv("CLERK_SECRET_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    try:
        yield tmp_path
    finally:
        object.__setattr__(settings, "root_dir", original_root)
        object.__setattr__(settings, "sandbox_mode", original_sandbox_mode)


def test_workspace_api_token_authorizes_only_its_workspace(isolated_app_root: Path) -> None:
    with TestClient(app) as client:
        workspace = _default_workspace(client)
        workspace_id = workspace["id"]

        initial_status = _get_json(client, f"/api/workspaces/{workspace_id}/api-token")
        assert initial_status == {
            "token_prefix": None,
            "created_at": None,
            "last_used_at": None,
        }

        created = _post_json(client, f"/api/workspaces/{workspace_id}/api-token")
        token = created["token"]
        assert token.startswith(f"{control_db.WORKSPACE_API_TOKEN_PREFIX}{workspace_id[:8]}_")
        assert created["token_prefix"]
        assert token.startswith(created["token_prefix"])
        assert created["created_at"]
        assert created["last_used_at"] is None

        token_headers = {"Authorization": f"Bearer {token}"}
        project = _get_json(client, f"/api/workspaces/{workspace_id}/project", headers=token_headers)
        assert project["workspace"]["id"] == workspace_id

        used_status = _get_json(client, f"/api/workspaces/{workspace_id}/api-token")
        assert used_status["last_used_at"]

        token_workspaces = _get_json(client, "/api/workspaces", headers=token_headers)
        assert [item["id"] for item in token_workspaces] == [workspace_id]

        other_workspace = control_db.create_workspace(control_db.LOCAL_USER_ID, "Other Workspace")
        wrong_workspace = client.get(
            f"/api/workspaces/{other_workspace.id}/project",
            headers=token_headers,
        )
        assert wrong_workspace.status_code == 403

        deleted = client.delete(f"/api/workspaces/{workspace_id}/api-token")
        assert deleted.status_code == 200
        assert deleted.json() == {"status": "deleted"}

        revoked = client.get(f"/api/workspaces/{workspace_id}/project", headers=token_headers)
        assert revoked.status_code == 401


def _default_workspace(client: TestClient) -> dict[str, str]:
    workspaces = _get_json(client, "/api/workspaces")
    assert len(workspaces) == 1
    return workspaces[0]


def _get_json(client: TestClient, path: str, headers: dict[str, str] | None = None):
    response = client.get(path, headers=headers)
    assert response.status_code == 200
    return response.json()


def _post_json(client: TestClient, path: str):
    response = client.post(path)
    assert response.status_code == 200
    return response.json()
