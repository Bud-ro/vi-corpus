from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
import re
from typing import Iterator

from app.config import settings
from app.core import execution_outputs
from app.schemas.domain import (
    ChatActivityEvent,
    ChatAttachment,
    ChatSummary,
    ExecutionSummary,
    Message,
    Principal,
    WorkspaceApiTokenCreateResponse,
    WorkspaceApiTokenStatus,
    WorkspaceSummary,
)

LOCAL_USER_ID = str(uuid.uuid5(uuid.NAMESPACE_URL, "arc.local-user"))
DEFAULT_WORKSPACE_ID = str(uuid.uuid5(uuid.NAMESPACE_URL, "arc.default-workspace"))
WORKSPACE_API_TOKEN_PREFIX = "arc_ws_"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    settings.var_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(settings.sqlite_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_control_db() -> None:
    with connect() as conn:
        conn.executescript(
            """
            create table if not exists users (
              id text primary key,
              clerk_user_id text unique,
              email text,
              display_name text,
              created_at text not null
            );

            create table if not exists workspaces (
              id text primary key,
              owner_user_id text not null,
              slug text not null,
              name text not null,
              root_path text not null,
              created_at text not null,
              foreign key(owner_user_id) references users(id)
            );

            create table if not exists chats (
              id text primary key,
              workspace_id text not null,
              user_id text not null,
              title text not null,
              created_at text not null
            );

            create table if not exists messages (
              id text primary key,
              chat_id text not null,
              role text not null,
              content text not null,
              created_at text not null,
              foreign key(chat_id) references chats(id)
            );

            create table if not exists executions (
              id text primary key,
              workspace_id text not null,
              workbook_id text not null,
              template_id text not null,
              target_type text not null,
              target_id text not null,
              status text not null,
              started_at text not null,
              completed_at text,
              execution_path text not null,
              workbook_git_commit text,
              error text
            );

            """
        )
        _ensure_column(conn, "workspaces", "name", "text")
        _ensure_column(conn, "workspaces", "api_token_hash", "text")
        _ensure_column(conn, "workspaces", "api_token_prefix", "text")
        _ensure_column(conn, "workspaces", "api_token_created_at", "text")
        _ensure_column(conn, "workspaces", "api_token_last_used_at", "text")
        _ensure_column(conn, "executions", "workbook_git_commit", "text")
        _ensure_column(conn, "messages", "attachments_json", "text")
        _ensure_column(conn, "messages", "activity_json", "text")
        conn.execute(
            """
            insert or ignore into users (id, clerk_user_id, email, display_name, created_at)
            values (?, null, ?, ?, ?)
            """,
            (LOCAL_USER_ID, "local@arc.dev", "Local User", utc_now()),
        )
        conn.execute(
            """
            insert or ignore into workspaces (id, owner_user_id, slug, name, root_path, created_at)
            values (?, ?, ?, ?, ?, ?)
            """,
            (
                DEFAULT_WORKSPACE_ID,
                LOCAL_USER_ID,
                "default",
                "Default Workspace",
                str(settings.workspace_root),
                utc_now(),
            ),
        )
        conn.execute(
            """
            update workspaces
            set owner_user_id = ?, slug = ?, name = ?, root_path = ?
            where id = ?
            """,
            (
                LOCAL_USER_ID,
                "default",
                "Default Workspace",
                str(settings.workspace_root),
                DEFAULT_WORKSPACE_ID,
            ),
        )


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
    columns = {row["name"] for row in conn.execute(f"pragma table_info({table})").fetchall()}
    if column not in columns:
        conn.execute(f"alter table {table} add column {column} {definition}")


def principal_from_headers(clerk_user_id: str | None = None, email: str | None = None) -> Principal:
    if not clerk_user_id:
        return Principal(user_id=LOCAL_USER_ID)

    return principal_from_clerk_user_id(clerk_user_id, email)


def principal_from_clerk_user_id(clerk_user_id: str, email: str | None = None) -> Principal:
    with connect() as conn:
        user = conn.execute(
            "select * from users where clerk_user_id = ?", (clerk_user_id,)
        ).fetchone()
        if user:
            user_id = user["id"]
            if email and user["email"] != email:
                conn.execute("update users set email = ? where id = ?", (email, user_id))
        else:
            user_id = str(uuid.uuid4())
            conn.execute(
                """
                insert into users (id, clerk_user_id, email, display_name, created_at)
                values (?, ?, ?, ?, ?)
                """,
                (user_id, clerk_user_id, email, email or "Clerk User", utc_now()),
            )
        return Principal(user_id=user_id, clerk_user_id=clerk_user_id)


def principal_from_workspace_api_token(token: str) -> Principal:
    token_hash = _hash_workspace_api_token(token)
    now = utc_now()
    with connect() as conn:
        row = conn.execute(
            """
            select id, owner_user_id
            from workspaces
            where api_token_hash = ?
            """,
            (token_hash,),
        ).fetchone()
        if row is None:
            raise KeyError("Workspace access token not found")
        conn.execute(
            "update workspaces set api_token_last_used_at = ? where id = ?",
            (now, row["id"]),
        )
    return Principal(user_id=row["owner_user_id"], api_workspace_id=row["id"])


def get_workspace_api_token_status(workspace_id: str) -> WorkspaceApiTokenStatus:
    with connect() as conn:
        row = conn.execute(
            """
            select api_token_prefix, api_token_created_at, api_token_last_used_at
            from workspaces
            where id = ?
            """,
            (workspace_id,),
        ).fetchone()
    if row is None:
        raise KeyError(f"Workspace not found: {workspace_id}")
    return WorkspaceApiTokenStatus(
        token_prefix=row["api_token_prefix"],
        created_at=row["api_token_created_at"],
        last_used_at=row["api_token_last_used_at"],
    )


def replace_workspace_api_token(workspace_id: str) -> WorkspaceApiTokenCreateResponse:
    token = _new_workspace_api_token(workspace_id)
    token_prefix = _workspace_api_token_display_prefix(token)
    now = utc_now()
    with connect() as conn:
        result = conn.execute(
            """
            update workspaces
            set api_token_hash = ?,
                api_token_prefix = ?,
                api_token_created_at = ?,
                api_token_last_used_at = null
            where id = ?
            """,
            (_hash_workspace_api_token(token), token_prefix, now, workspace_id),
        )
        if result.rowcount == 0:
            raise KeyError(f"Workspace not found: {workspace_id}")
    return WorkspaceApiTokenCreateResponse(
        token=token,
        token_prefix=token_prefix,
        created_at=now,
        last_used_at=None,
    )


def delete_workspace_api_token(workspace_id: str) -> None:
    with connect() as conn:
        result = conn.execute(
            """
            update workspaces
            set api_token_hash = null,
                api_token_prefix = null,
                api_token_created_at = null,
                api_token_last_used_at = null
            where id = ?
            """,
            (workspace_id,),
        )
        if result.rowcount == 0:
            raise KeyError(f"Workspace not found: {workspace_id}")


def list_all_workspaces() -> list[WorkspaceSummary]:
    with connect() as conn:
        rows = conn.execute("select * from workspaces order by created_at").fetchall()
    return [_workspace_from_row(row) for row in rows]


def list_workspaces(user_id: str) -> list[WorkspaceSummary]:
    with connect() as conn:
        rows = conn.execute(
            "select * from workspaces where owner_user_id = ? order by created_at",
            (user_id,),
        ).fetchall()
    return [_workspace_from_row(row) for row in rows]


def ensure_personal_workspace(user_id: str) -> WorkspaceSummary:
    existing = list_workspaces(user_id)
    if existing:
        return existing[0]
    return create_workspace(user_id, "Arc Workspace")


def create_workspace(owner_user_id: str, name: str) -> WorkspaceSummary:
    workspace_id = str(uuid.uuid4())
    clean_name = name.strip() or "Untitled Workspace"
    slug = _unique_workspace_slug(slugify(clean_name) or f"workspace-{workspace_id[:8]}")
    root_path = settings.workspaces_root / slug
    with connect() as conn:
        conn.execute(
            """
            insert into workspaces (id, owner_user_id, slug, name, root_path, created_at)
            values (?, ?, ?, ?, ?, ?)
            """,
            (workspace_id, owner_user_id, slug, clean_name, str(root_path), utc_now()),
        )
    return WorkspaceSummary(id=workspace_id, name=clean_name, slug=slug, root_path=str(root_path))


def get_workspace(workspace_id: str, user_id: str | None = None) -> WorkspaceSummary:
    sql = "select * from workspaces where id = ?"
    params = [workspace_id]
    if user_id is not None:
        sql += " and owner_user_id = ?"
        params.append(user_id)
    with connect() as conn:
        row = conn.execute(sql, params).fetchone()
    if row is None:
        raise KeyError(f"Workspace not found: {workspace_id}")
    return _workspace_from_row(row)


def get_workspace_owner_email(workspace_id: str) -> str | None:
    with connect() as conn:
        row = conn.execute(
            """
            select users.email
            from workspaces
            join users on users.id = workspaces.owner_user_id
            where workspaces.id = ?
            """,
            (workspace_id,),
        ).fetchone()
    if row is None:
        raise KeyError(f"Workspace not found: {workspace_id}")
    email = row["email"]
    return email.strip() if isinstance(email, str) and email.strip() else None


def _workspace_from_row(row: sqlite3.Row) -> WorkspaceSummary:
    row_keys = row.keys()
    name = row["name"] if "name" in row_keys and row["name"] else workspace_name_seed(row["slug"])
    return WorkspaceSummary(
        id=row["id"],
        name=name,
        slug=row["slug"],
        root_path=row["root_path"],
    )


def _new_workspace_api_token(workspace_id: str) -> str:
    return f"{WORKSPACE_API_TOKEN_PREFIX}{workspace_id[:8]}_{secrets.token_urlsafe(32)}"


def _hash_workspace_api_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _workspace_api_token_display_prefix(token: str) -> str:
    return token[:18]


def workspace_name_seed(slug: str) -> str:
    if slug == "default":
        return "Default Workspace"
    return slug.replace("-", " ").strip().title() or "Workspace"


def _unique_workspace_slug(base_slug: str) -> str:
    slug = base_slug
    index = 2
    with connect() as conn:
        while conn.execute("select 1 from workspaces where slug = ?", (slug,)).fetchone():
            slug = f"{base_slug}-{index}"
            index += 1
    return slug


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def create_chat(workspace_id: str, user_id: str, title: str) -> str:
    chat_id = str(uuid.uuid4())
    with connect() as conn:
        conn.execute(
            """
            insert into chats (id, workspace_id, user_id, title, created_at)
            values (?, ?, ?, ?, ?)
            """,
            (chat_id, workspace_id, user_id, title, utc_now()),
        )
    return chat_id


def add_message(
    chat_id: str,
    role: str,
    content: str,
    attachments: list[ChatAttachment] | None = None,
    activity: list[ChatActivityEvent] | None = None,
) -> Message:
    clean_attachments = attachments or []
    clean_activity = activity or []
    message = Message(
        id=str(uuid.uuid4()),
        role=role,
        content=content,
        attachments=clean_attachments,
        activity=clean_activity,
        created_at=utc_now(),
    )
    with connect() as conn:
        conn.execute(
            """
            insert into messages (id, chat_id, role, content, created_at, attachments_json, activity_json)
            values (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message.id,
                chat_id,
                role,
                content,
                message.created_at,
                json.dumps([attachment.model_dump() for attachment in clean_attachments]),
                json.dumps([event.model_dump() for event in clean_activity]),
            ),
        )
    return message


def list_chats(workspace_id: str) -> list[ChatSummary]:
    with connect() as conn:
        rows = conn.execute(
            """
            select
              chats.id,
              chats.title,
              chats.created_at,
              coalesce(max(messages.created_at), chats.created_at) as updated_at,
              count(messages.id) as message_count
            from chats
            left join messages on messages.chat_id = chats.id
            where chats.workspace_id = ?
            group by chats.id
            order by updated_at desc
            """,
            (workspace_id,),
        ).fetchall()
    return [
        ChatSummary(
            id=row["id"],
            title=row["title"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            message_count=row["message_count"],
        )
        for row in rows
    ]


def ensure_chat_in_workspace(chat_id: str, workspace_id: str) -> None:
    with connect() as conn:
        row = conn.execute(
            "select 1 from chats where id = ? and workspace_id = ?",
            (chat_id, workspace_id),
        ).fetchone()
    if row is None:
        raise KeyError(f"Chat not found: {chat_id}")


def list_messages(chat_id: str, workspace_id: str) -> list[Message]:
    with connect() as conn:
        rows = conn.execute(
            """
            select messages.*
            from messages
            join chats on chats.id = messages.chat_id
            where messages.chat_id = ? and chats.workspace_id = ?
            order by messages.created_at
            """,
            (chat_id, workspace_id),
        ).fetchall()
    return [_message_from_row(row) for row in rows]


def _message_from_row(row: sqlite3.Row) -> Message:
    raw_attachments = row["attachments_json"] if "attachments_json" in row.keys() else None
    raw_activity = row["activity_json"] if "activity_json" in row.keys() else None
    attachments: list[ChatAttachment] = []
    activity: list[ChatActivityEvent] = []
    if raw_attachments:
        try:
            attachments = [
                ChatAttachment.model_validate(item)
                for item in json.loads(raw_attachments)
                if isinstance(item, dict)
            ]
        except (TypeError, ValueError):
            attachments = []
    if raw_activity:
        try:
            activity = [
                ChatActivityEvent.model_validate(item)
                for item in json.loads(raw_activity)
                if isinstance(item, dict)
            ]
        except (TypeError, ValueError):
            activity = []
    return Message(
        id=row["id"],
        role=row["role"],
        content=row["content"],
        created_at=row["created_at"],
        attachments=attachments,
        activity=activity,
    )


def create_execution(
    workspace_id: str,
    workbook_id: str,
    template_id: str,
    target_type: str,
    target_id: str,
    executions_root: Path,
    workbook_git_commit: str | None = None,
) -> ExecutionSummary:
    execution_id = str(uuid.uuid4())
    execution_path = executions_root / execution_id
    clean_target_type = target_type.strip() if target_type and target_type.strip() else "workbook"
    execution = ExecutionSummary(
        id=execution_id,
        workspace_id=workspace_id,
        workbook_id=workbook_id,
        template_id=template_id,
        target_type=clean_target_type,
        target_id=target_id,
        linked_asset_id=target_id if clean_target_type == "asset" else None,
        status="queued",
        started_at=utc_now(),
        workbook_git_commit=workbook_git_commit,
    )
    with connect() as conn:
        conn.execute(
            """
            insert into executions (
              id,
              workspace_id,
              workbook_id,
              template_id,
              target_type,
              target_id,
              status,
              started_at,
              execution_path,
              workbook_git_commit
            )
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                execution.id,
                workspace_id,
                workbook_id,
                template_id,
                clean_target_type,
                target_id,
                execution.status,
                execution.started_at,
                str(execution_path),
                workbook_git_commit,
            ),
        )
    return execution


def update_execution(execution_id: str, status: str, error: str | None = None) -> None:
    completed_at = utc_now() if status in {"succeeded", "failed", "canceled"} else None
    with connect() as conn:
        conn.execute(
            """
            update executions
            set status = ?, completed_at = coalesce(?, completed_at), error = coalesce(?, error)
            where id = ?
            """,
            (status, completed_at, error, execution_id),
        )


def get_execution(execution_id: str) -> ExecutionSummary:
    with connect() as conn:
        row = conn.execute("select * from executions where id = ?", (execution_id,)).fetchone()
    if row is None:
        raise KeyError(f"Execution not found: {execution_id}")
    return _execution_from_row(row)


def get_execution_for_workspace(workspace_id: str, execution_id: str) -> ExecutionSummary:
    execution = get_execution(execution_id)
    if execution.workspace_id != workspace_id:
        raise KeyError(f"Execution not found: {execution_id}")
    return execution


def get_execution_path(execution_id: str) -> Path:
    with connect() as conn:
        row = conn.execute("select execution_path from executions where id = ?", (execution_id,)).fetchone()
    if row is None:
        raise KeyError(f"Execution not found: {execution_id}")
    return Path(row["execution_path"])


def get_execution_path_for_workspace(workspace_id: str, execution_id: str) -> Path:
    get_execution_for_workspace(workspace_id, execution_id)
    return get_execution_path(execution_id)


def list_executions(
    workspace_id: str,
    workbook_id: str | None = None,
    target_type: str | None = None,
    target_id: str | None = None,
) -> list[ExecutionSummary]:
    sql = "select * from executions where workspace_id = ?"
    params: list[str] = [workspace_id]
    if workbook_id:
        sql += " and workbook_id = ?"
        params.append(workbook_id)
    if target_type:
        sql += " and target_type = ?"
        params.append(target_type)
    if target_id:
        sql += " and target_id = ?"
        params.append(target_id)
    sql += " order by started_at desc"
    with connect() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_execution_from_row(row) for row in rows]


def _execution_from_row(row: sqlite3.Row) -> ExecutionSummary:
    execution_path = Path(row["execution_path"])
    target_type = row["target_type"] if isinstance(row["target_type"], str) and row["target_type"].strip() else "workbook"
    return ExecutionSummary(
        id=row["id"],
        workspace_id=row["workspace_id"],
        workbook_id=row["workbook_id"],
        template_id=row["template_id"],
        target_type=target_type,
        target_id=row["target_id"],
        linked_asset_id=row["target_id"] if target_type == "asset" else None,
        status=row["status"],
        started_at=row["started_at"],
        completed_at=row["completed_at"],
        error=row["error"],
        workbook_git_commit=row["workbook_git_commit"],
        log_count=execution_outputs.log_count(execution_path),
        check_counts=execution_outputs.check_counts(execution_path),
    )
