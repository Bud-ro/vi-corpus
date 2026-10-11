from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.api import routes
from app.core import control_db
from app.core import executions as executions_core
from app.core import reports
from app.main import app
from app.schemas.domain import ExecutionSummary


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


def test_first_run_creates_empty_workspace(isolated_app_root: Path) -> None:
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}

        workspace = _default_workspace(client)
        workspace_id = workspace["id"]

        project = _get_json(client, f"/api/workspaces/{workspace_id}/project")
        assert project["workspace"]["slug"] == "default"
        assert project["chat_available"] is False
        assert project["chat_setup_message"] == "Arc Chat is not configured."
        assert "sandbox_mode" not in project

        assets = _get_json(client, f"/api/workspaces/{workspace_id}/assets")
        assert assets == []

        runs = _get_json(client, f"/api/workspaces/{workspace_id}/runs")
        assert runs == []

        templates = _get_json(client, f"/api/workspaces/{workspace_id}/workbook-templates")
        assert {template["id"] for template in templates} == {"blank-workbook"}

        workbooks = _get_json(client, f"/api/workspaces/{workspace_id}/workbooks")
        assert workbooks == []

        executions = _get_json(client, f"/api/workspaces/{workspace_id}/executions")
        assert executions == []

        charts = _get_json(client, f"/api/workspaces/{workspace_id}/charts")
        assert charts == []

        reports = _get_json(client, f"/api/workspaces/{workspace_id}/reports")
        assert reports == []

        workspace_root = isolated_app_root / "data" / "workspaces" / "default"
        project_json = json.loads((workspace_root / "project.json").read_text(encoding="utf-8"))
        assert "starter_preset" not in project_json

    assert (isolated_app_root / "data" / "var" / "app.sqlite").exists()
    assert (isolated_app_root / "data" / "workspaces" / "default" / ".git").exists()


def test_workspace_api_uses_project_settings_name(isolated_app_root: Path) -> None:
    workspace_root = isolated_app_root / "data" / "workspaces" / "default"
    workspace_root.mkdir(parents=True)
    (workspace_root / "project.json").write_text(
        json.dumps({"name": "Custom Default Workspace"}) + "\n",
        encoding="utf-8",
    )

    with TestClient(app) as client:
        workspace = _default_workspace(client)
        project = _get_json(client, f"/api/workspaces/{workspace['id']}/project")
        settings = _get_json(client, f"/api/workspaces/{workspace['id']}/settings")

        assert workspace["name"] == "Custom Default Workspace"
        assert project["workspace"]["name"] == "Custom Default Workspace"
        assert settings["name"] == "Custom Default Workspace"


def test_settings_name_updates_workspace_list(isolated_app_root: Path) -> None:
    with TestClient(app) as client:
        workspace = _default_workspace(client)
        settings = _get_json(client, f"/api/workspaces/{workspace['id']}/settings")
        saved = _put_json(
            client,
            f"/api/workspaces/{workspace['id']}/settings",
            {**settings, "name": "Renamed Workspace"},
        )
        workspaces = _get_json(client, "/api/workspaces")

        assert saved["name"] == "Renamed Workspace"
        assert workspaces[0]["name"] == "Renamed Workspace"


def test_workbook_metadata_is_saved(isolated_app_root: Path) -> None:
    with TestClient(app) as client:
        workspace = _default_workspace(client)
        workbook = _create_minimal_workbook(client, workspace["id"])
        workbook_detail = _get_json(client, f"/api/workspaces/{workspace['id']}/workbooks/{workbook['id']}")
        workbook = workbook_detail["workbook"]

        saved = _put_json(
            client,
            f"/api/workspaces/{workspace['id']}/workbooks/{workbook['id']}",
            {
                "id": workbook["id"],
                "title": workbook["title"],
                "template_id": workbook["template_id"],
                "linked_asset_id": workbook["linked_asset_id"],
                "step_order": workbook["step_order"],
                "tags": ["baseline", "reviewed"],
                "properties": {"owner": "qa"},
                "status": "ready",
            },
        )

        assert saved["tags"] == ["baseline", "reviewed"]
        assert saved["properties"] == {"owner": "qa"}


def test_workbook_blocks_are_copied_from_templates_and_edited_locally(isolated_app_root: Path) -> None:
    with TestClient(app) as client:
        workspace = _default_workspace(client)
        workspace_id = workspace["id"]
        workbook = _create_workbook_with_template_block(client, workspace_id)

        detail = _get_json(client, f"/api/workspaces/{workspace_id}/workbooks/{workbook['id']}")
        assert detail["steps"][0]["script"] == "print('template step')\n"

        saved_block = _put_json(
            client,
            f"/api/workspaces/{workspace_id}/workbooks/{workbook['id']}/steps/signal-quality",
            {
                "id": "signal-quality",
                "title": "Signal quality",
                "prompt": "Check this workbook only.",
                "input_refs": [],
                "entrypoint": "main.py",
                "script": "print('workbook step')",
            },
        )

        template = _get_json(client, f"/api/workspaces/{workspace_id}/workbook-templates/qa-template")
        detail = _get_json(client, f"/api/workspaces/{workspace_id}/workbooks/{workbook['id']}")

        assert saved_block["script"] == "print('workbook step')\n"
        assert template["step_files"][0]["script"] == "print('template step')\n"
        assert detail["steps"][0]["script"] == "print('workbook step')\n"

        workspace_root = isolated_app_root / "data" / "workspaces" / "default"
        assert (workspace_root / "workbook_templates" / "workbook" / "qa-template" / "steps" / "signal-quality" / "main.py").read_text(encoding="utf-8") == "print('template step')\n"
        assert (workspace_root / "workbooks" / workbook["id"] / "steps" / "signal-quality" / "main.py").read_text(encoding="utf-8") == "print('workbook step')\n"


def test_asset_workbook_execution_context_includes_asset_runs(isolated_app_root: Path) -> None:
    with TestClient(app) as client:
        workspace = _default_workspace(client)
        workspace_id = workspace["id"]
        workbook = _create_workbook_with_template_block(client, workspace_id, execution_script=True)
        workspace_root = isolated_app_root / "data" / "workspaces" / "default"

        execution = executions_core.start_workbook_execution(
            workspace_id,
            workspace_root,
            workbook["id"],
            background=False,
        )
        detail = _get_json(client, f"/api/workspaces/{workspace_id}/workbooks/{workbook['id']}")

    target = json.loads((control_db.get_execution_path(execution.id) / "target.json").read_text(encoding="utf-8"))
    assert target["workbook"]["linked_asset_id"] == "headset-a014"
    assert target["asset"]["id"] == "headset-a014"
    assert len(detail["panels"]) == 1
    assert detail["panels"][0]["kind"] == "report"
    assert detail["panels"][0]["step_id"] == "signal-quality"
    assert [run["id"] for run in target["runs"]] == ["second-run", "baseline-run"]


def test_workspaces_are_scoped_to_principal(isolated_app_root: Path) -> None:
    alice_headers = {
        "x-clerk-user-id": "user_alice",
        "x-clerk-email": "alice@example.com",
    }

    with TestClient(app) as client:
        local_workspace = _default_workspace(client)
        alice_workspaces = _get_json(client, "/api/workspaces", headers=alice_headers)

        assert len(alice_workspaces) == 1
        assert alice_workspaces[0]["id"] != local_workspace["id"]
        assert alice_workspaces[0]["slug"] == "arc-workspace"

        response = client.get(
            f"/api/workspaces/{local_workspace['id']}/project",
            headers=alice_headers,
        )
        assert response.status_code == 404

        create_response = client.post(
            "/api/workspaces",
            json={"name": "Second workspace"},
            headers=alice_headers,
        )
        assert create_response.status_code == 200
        assert create_response.json()["id"] == alice_workspaces[0]["id"]


def test_workspace_create_handles_existing_name_column(isolated_app_root: Path) -> None:
    db_path = isolated_app_root / "data" / "var" / "app.sqlite"
    db_path.parent.mkdir(parents=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(
            """
            create table users (
              id text primary key,
              clerk_user_id text unique,
              email text,
              display_name text,
              created_at text not null
            );
            create table workspaces (
              id text primary key,
              owner_user_id text not null,
              slug text not null,
              name text not null,
              root_path text not null,
              created_at text not null,
              foreign key(owner_user_id) references users(id)
            );
            """
        )

    alice_headers = {
        "x-clerk-user-id": "user_alice",
        "x-clerk-email": "alice@example.com",
    }

    with TestClient(app) as client:
        alice_workspaces = _get_json(client, "/api/workspaces", headers=alice_headers)

    assert len(alice_workspaces) == 1
    assert alice_workspaces[0]["name"] == "Arc Workspace"


def test_chat_requires_openai_api_key_without_saving_messages(isolated_app_root: Path) -> None:
    with TestClient(app) as client:
        workspace = _default_workspace(client)
        workspace_id = workspace["id"]

        response = client.post(
            f"/api/workspaces/{workspace_id}/chat",
            json={"message": "Hello"},
        )

        assert response.status_code == 503
        assert response.json()["detail"] == "Arc Chat is not configured."
        assert _get_json(client, f"/api/workspaces/{workspace_id}/chats") == []


def test_chat_seed_messages_are_saved_before_first_user_message(
    isolated_app_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prompts: list[str] = []

    class FakeSandboxService:
        def __init__(self, workspace_root: Path, workspace_id: str):
            pass

        async def respond(self, prompt: str, timer=None) -> str:
            prompts.append(prompt)
            return "Sure, I can help with that."

    monkeypatch.setattr(routes.sandbox, "chat_setup_error", lambda: None)
    monkeypatch.setattr(routes.sandbox, "SandboxService", FakeSandboxService)

    with TestClient(app) as client:
        workspace = _default_workspace(client)
        workspace_id = workspace["id"]

        response = client.post(
            f"/api/workspaces/{workspace_id}/chat",
            json={
                "message": "Can you inspect my data?",
                "seed_messages": [
                    {"role": "user", "content": "What is this?"},
                    {"role": "assistant", "content": "Hi, welcome to Arc."},
                ],
            },
        )

        assert response.status_code == 200
        chat_id = response.json()["chat_id"]
        detail = _get_json(client, f"/api/workspaces/{workspace_id}/chat/{chat_id}")

    assert [(message["role"], message["content"]) for message in detail["messages"]] == [
        ("user", "What is this?"),
        ("assistant", "Hi, welcome to Arc."),
        ("user", "Can you inspect my data?"),
        ("assistant", "Sure, I can help with that."),
    ]
    assert prompts
    assert "USER:\nWhat is this?" in prompts[0]
    assert "ASSISTANT:\nHi, welcome to Arc." in prompts[0]
    assert "USER:\nCan you inspect my data?" in prompts[0]


def test_chat_saves_user_facing_activity_for_agent_tools(
    isolated_app_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeSandboxService:
        def __init__(self, workspace_root: Path, workspace_id: str):
            pass

        async def respond(self, prompt: str, timer=None) -> str:
            assert timer is not None
            with timer.span("tool.list_workbooks"):
                pass
            with timer.span("tool.compute_workbook", workbook_id="baseline-review"):
                pass
            return "Workbook computed."

    monkeypatch.setattr(routes.sandbox, "chat_setup_error", lambda: None)
    monkeypatch.setattr(routes.sandbox, "SandboxService", FakeSandboxService)

    with TestClient(app) as client:
        workspace = _default_workspace(client)
        workspace_id = workspace["id"]

        response = client.post(
            f"/api/workspaces/{workspace_id}/chat",
            json={"message": "Compute the workbook"},
        )

        assert response.status_code == 200
        body = response.json()
        detail = _get_json(client, f"/api/workspaces/{workspace_id}/chat/{body['chat_id']}")

    assert [
        {key: event[key] for key in ("label", "status", "detail")}
        for event in body["activity"]
    ] == [
        {"label": "Checked workbooks", "status": "ok", "detail": None},
        {"label": "Started workbook execution", "status": "ok", "detail": "baseline-review"},
    ]
    assert all(isinstance(event["duration_ms"], (int, float)) for event in body["activity"])
    assistant_message = detail["messages"][-1]
    assert assistant_message["content"] == "Workbook computed."
    assert assistant_message["activity"] == body["activity"]


def test_report_refresh_starts_linked_workbook(
    isolated_app_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    started: list[tuple[str, Path, str]] = []

    def fake_start_workbook_execution(
        workspace_id: str,
        workspace_root: Path,
        workbook_id: str,
        **kwargs,
    ) -> ExecutionSummary:
        started.append((workspace_id, workspace_root, workbook_id))
        return ExecutionSummary(
            id="refresh_execution",
            workspace_id=workspace_id,
            workbook_id=workbook_id,
            template_id="qa-template",
            target_type="asset",
            target_id="headset-a014",
            linked_asset_id="headset-a014",
            status="queued",
            started_at="2026-06-04T00:00:00+00:00",
        )

    with TestClient(app) as client:
        workspace = _default_workspace(client)
        _create_minimal_workbook(client, workspace["id"])
        reports.write_report(
            isolated_app_root / "data" / "workspaces" / "default",
            report_id="baseline_report",
            title="Baseline report",
            output_path="outputs/report.html",
            workbook_id="baseline-review",
            execution_id="previous_execution",
        )
        monkeypatch.setattr(routes.executions, "start_workbook_execution", fake_start_workbook_execution)
        response = client.post(
            f"/api/workspaces/{workspace['id']}/reports/baseline_report/refresh"
        )

    assert response.status_code == 200
    assert response.json()["id"] == "refresh_execution"
    assert response.json()["workbook_id"] == "baseline-review"
    assert started == [
        (
            workspace["id"],
            isolated_app_root / "data" / "workspaces" / "default",
            "baseline-review",
        )
    ]


def _create_minimal_workbook(client: TestClient, workspace_id: str) -> dict:
    _post_json(
        client,
        f"/api/workspaces/{workspace_id}/assets",
        {
            "id": "headset-a014",
            "name": "Headset A-014",
            "asset_type": "system",
            "tags": [],
            "properties": {},
        },
    )
    _post_json(
        client,
        f"/api/workspaces/{workspace_id}/runs",
        {
            "id": "baseline-run",
            "name": "Baseline run",
            "asset_id": "headset-a014",
            "start_time": "2026-06-09T10:00:00Z",
            "end_time": "2026-06-09T10:30:00Z",
            "tags": [],
            "properties": {},
        },
    )
    _post_json(
        client,
        f"/api/workspaces/{workspace_id}/workbook-templates",
        {
            "id": "qa-template",
            "name": "QA template",
            "description": "",
            "steps": [],
            "tags": [],
            "properties": {},
        },
    )
    return _post_json(
        client,
        f"/api/workspaces/{workspace_id}/workbooks",
        {
            "id": "baseline-review",
            "title": "Baseline review",
            "template_id": "qa-template",
            "linked_asset_id": "headset-a014",
            "step_order": [],
            "tags": [],
            "properties": {},
            "status": "ready",
        },
    )


def _create_workbook_with_template_block(client: TestClient, workspace_id: str, execution_script: bool = False) -> dict:
    _post_json(
        client,
        f"/api/workspaces/{workspace_id}/assets",
        {
            "id": "headset-a014",
            "name": "Headset A-014",
            "asset_type": "system",
            "tags": [],
            "properties": {},
        },
    )
    _post_json(
        client,
        f"/api/workspaces/{workspace_id}/runs",
        {
            "id": "baseline-run",
            "name": "Baseline run",
            "asset_id": "headset-a014",
            "start_time": "2026-06-09T10:00:00Z",
            "end_time": "2026-06-09T10:30:00Z",
            "tags": [],
            "properties": {},
        },
    )
    _post_json(
        client,
        f"/api/workspaces/{workspace_id}/runs",
        {
            "id": "second-run",
            "name": "Second run",
            "asset_id": "headset-a014",
            "start_time": "2026-06-10T10:00:00Z",
            "end_time": "2026-06-10T10:30:00Z",
            "tags": [],
            "properties": {},
        },
    )
    _post_json(
        client,
        f"/api/workspaces/{workspace_id}/workbook-templates",
        {
            "id": "qa-template",
            "name": "QA template",
            "description": "",
            "steps": [],
            "tags": [],
            "properties": {},
        },
    )
    script = "print('template step')"
    if execution_script:
        script = "\n".join(
            [
                "import argparse, json",
                "from pathlib import Path",
                "parser = argparse.ArgumentParser()",
                "parser.add_argument('--workspace')",
                "parser.add_argument('--execution')",
                "parser.add_argument('--duckdb')",
                "args = parser.parse_args()",
                "target = json.loads((Path(args.execution) / 'target.json').read_text())",
                "outputs = Path(args.execution) / 'outputs'",
                "outputs.mkdir(parents=True, exist_ok=True)",
                "(outputs / 'context.html').write_text(f\"{target['asset']['id']} {len(target['runs'])}\")",
            ]
        )
    _put_json(
        client,
        f"/api/workspaces/{workspace_id}/workbook-templates/qa-template/steps/signal-quality",
        {
            "id": "signal-quality",
            "title": "Signal quality",
            "prompt": "Check signal quality.",
            "input_refs": [],
            "entrypoint": "main.py",
            "script": script,
        },
    )
    return _post_json(
        client,
        f"/api/workspaces/{workspace_id}/workbooks",
        {
            "id": "asset-health" if execution_script else "baseline-review",
            "title": "Asset health" if execution_script else "Baseline review",
            "template_id": "qa-template",
            "linked_asset_id": "headset-a014",
            "step_order": ["signal-quality"],
            "tags": [],
            "properties": {},
            "status": "ready",
        },
    )


def _default_workspace(client: TestClient) -> dict[str, str]:
    workspaces = _get_json(client, "/api/workspaces")
    assert len(workspaces) == 1
    return workspaces[0]


def _get_json(client: TestClient, path: str, headers: dict[str, str] | None = None):
    response = client.get(path, headers=headers)
    assert response.status_code == 200
    return response.json()


def _put_json(client: TestClient, path: str, payload: dict):
    response = client.put(path, json=payload)
    assert response.status_code == 200
    return response.json()


def _post_json(client: TestClient, path: str, payload: dict):
    response = client.post(path, json=payload)
    assert response.status_code == 200
    return response.json()
