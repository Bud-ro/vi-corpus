from __future__ import annotations

from pathlib import Path

from app.api import routes
from app.schemas.domain import ChatAttachment, Message


def test_chat_file_attachments_ignore_tdms_index_files(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    data_root = workspace_root / "files" / "local"
    data_root.mkdir(parents=True)
    (data_root / "line_quality.csv").write_text("line,failures\nA,3\n", encoding="utf-8")
    (data_root / "line_quality.tdms_index").write_text("generated index", encoding="utf-8")

    attachments = routes._workspace_file_attachments_from_text(
        workspace_root,
        "Show `files/local/line_quality.tdms_index` and `files/local/line_quality.csv`.",
    )

    assert [attachment.path for attachment in attachments] == ["files/local/line_quality.csv"]


def test_validated_chat_mentions_keep_resolved_path_and_label(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    target = workspace_root / "backend" / "app" / "core" / "workbooks.py"
    target.parent.mkdir(parents=True)
    target.write_text("print('workbook')\n", encoding="utf-8")

    mentions = routes._validated_chat_mentions(
        workspace_root,
        [
            ChatAttachment(
                type="workspace_file",
                path="backend/app/core/workbooks.py",
                label="@workbooks.py",
            )
        ],
        "Can you explain @workbooks.py?",
    )

    assert len(mentions) == 1
    assert mentions[0].path == "backend/app/core/workbooks.py"
    assert mentions[0].label == "@workbooks.py"
    assert mentions[0].title == "workbooks.py"
    assert mentions[0].language == "python"


def test_validated_chat_mentions_allow_unlabeled_uploaded_files(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    target = workspace_root / "files" / "local" / "sales.csv"
    target.parent.mkdir(parents=True)
    target.write_text("region,revenue\nNorth,42\n", encoding="utf-8")

    mentions = routes._validated_chat_mentions(
        workspace_root,
        [
            ChatAttachment(
                type="workspace_file",
                path="files/local/sales.csv",
                title="sales.csv",
            )
        ],
        "Compare this to last week.",
    )

    assert len(mentions) == 1
    assert mentions[0].path == "files/local/sales.csv"
    assert mentions[0].label is None
    assert mentions[0].title == "sales.csv"


def test_direct_file_attachments_use_selected_mentions(tmp_path: Path) -> None:
    workspace_root = tmp_path / "workspace"
    target = workspace_root / "backend" / "app" / "core" / "workbooks.py"
    target.parent.mkdir(parents=True)
    target.write_text("print('workbook')\n", encoding="utf-8")
    mention = ChatAttachment(
        type="workspace_file",
        path="backend/app/core/workbooks.py",
        title="workbooks.py",
        label="@workbooks.py",
    )

    attachments = routes._direct_file_attachments(
        workspace_root,
        [
            Message(
                id="pending",
                role="user",
                content="Show @workbooks.py",
                attachments=[mention],
                created_at="",
            )
        ],
    )

    assert [attachment.path for attachment in attachments] == ["backend/app/core/workbooks.py"]


def test_sandbox_prompt_includes_selected_mention_paths() -> None:
    prompt = routes._sandbox_chat_prompt(
        [
            Message(
                id="message",
                role="user",
                content="Can you explain @workbooks.py?",
                attachments=[
                    ChatAttachment(
                        type="workspace_file",
                        path="backend/app/core/workbooks.py",
                        title="workbooks.py",
                        label="@workbooks.py",
                    )
                ],
                created_at="",
            )
        ]
    )

    assert "Mentioned workspace files" in prompt
    assert "@workbooks.py -> backend/app/core/workbooks.py" in prompt
