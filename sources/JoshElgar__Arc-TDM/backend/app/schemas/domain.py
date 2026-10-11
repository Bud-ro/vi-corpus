from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class Principal(BaseModel):
    user_id: str
    clerk_user_id: str | None = None
    api_workspace_id: str | None = None


class WorkspaceSummary(BaseModel):
    id: str
    name: str
    slug: str
    root_path: str


class WorkspaceCreateRequest(BaseModel):
    name: str


class ProjectSummary(BaseModel):
    workspace: WorkspaceSummary
    chat_available: bool
    chat_setup_message: str | None = None
    tabs: list[str]


class ProjectSettings(BaseModel):
    name: str
    agent_system_prompt: str


class WorkspaceApiTokenStatus(BaseModel):
    token_prefix: str | None = None
    created_at: str | None = None
    last_used_at: str | None = None


class WorkspaceApiTokenCreateResponse(WorkspaceApiTokenStatus):
    token: str


class FileEntry(BaseModel):
    path: str
    name: str
    kind: Literal["file", "directory"]
    size: int | None = None
    modified_at: str | None = None
    source_kind: Literal["file", "dataset"] = "file"
    dataset_kind: str | None = None
    status: str | None = None
    member_count: int | None = None


class FilePreview(BaseModel):
    path: str
    kind: str
    columns: list[str] = Field(default_factory=list)
    rows: list[dict[str, Any]] = Field(default_factory=list)
    text: str | None = None


class FileTablePage(BaseModel):
    path: str
    kind: str
    columns: list[str] = Field(default_factory=list)
    rows: list[dict[str, Any]] = Field(default_factory=list)
    page: int
    page_size: int
    has_next: bool = False
    row_count: int | None = None
    text: str | None = None


class WorkspaceFileRead(BaseModel):
    path: str
    name: str
    language: str | None = None
    size: int
    modified_at: str | None = None
    text: str
    truncated: bool = False


class UploadResponse(BaseModel):
    path: str
    sha256: str | None = None
    size: int
    duckdb_table: str | None = None
    kind: Literal["file", "dataset"] = "file"
    dataset_kind: str | None = None
    status: str | None = None
    member_count: int | None = None


class DatasetCreateRequest(BaseModel):
    path: str


class ComponentDocLink(BaseModel):
    label: str
    url: str
    kind: str = "link"


class ComponentChannel(BaseModel):
    id: str
    label: str
    unit: str


class ComponentModelDefinition(BaseModel):
    id: str
    name: str
    vendor: str
    kind: str
    description: str = ""
    default_sample_rate_hz: int
    channels: list[ComponentChannel] = Field(default_factory=list)
    docs: list[ComponentDocLink] = Field(default_factory=list)
    notes: str = ""


class ComponentSample(BaseModel):
    timestamp: str
    asset_id: str
    component_model_id: str
    sequence: int
    ax_g: float
    ay_g: float
    az_g: float
    temperature_c: float
    event: str | None = None


class ComponentRecordingStartRequest(BaseModel):
    sample_rate_hz: int | None = None


class ComponentRecordingStartResponse(BaseModel):
    id: str
    asset_id: str
    component_model_id: str
    sample_rate_hz: int
    started_at: str
    status: Literal["recording"] = "recording"


class ComponentEventRequest(BaseModel):
    label: str


class ComponentRecordingStopResponse(BaseModel):
    id: str
    asset_id: str
    component_model_id: str
    sample_rate_hz: int
    started_at: str
    stopped_at: str
    sample_count: int
    event_count: int
    file_path: str
    run_id: str


class ComponentWorkbookCreateRequest(BaseModel):
    recording_id: str
    title: str | None = None


class AssetWrite(BaseModel):
    id: str
    name: str
    asset_type: Literal["system", "component"]
    parent_asset_id: str | None = None
    component_model_id: str | None = None
    tags: list[str] = Field(default_factory=list)
    properties: dict[str, str] = Field(default_factory=dict)
    archived_at: str | None = None


class AssetSummary(AssetWrite):
    path: str | None = None
    run_count: int = 0
    workbook_count: int = 0
    component_count: int = 0


class TestRunWrite(BaseModel):
    id: str
    name: str
    asset_id: str
    start_time: str
    end_time: str
    notes: str = ""
    tags: list[str] = Field(default_factory=list)
    properties: dict[str, str] = Field(default_factory=dict)


class TestRunSummary(TestRunWrite):
    path: str | None = None
    asset_name: str | None = None
    workbook_count: int = 0
    execution_count: int = 0


class WorkbookStep(BaseModel):
    id: str
    title: str
    prompt: str = ""
    input_refs: list[str] = Field(default_factory=list)
    entrypoint: str = "main.py"
    script: str | None = None
    active: bool = True


class WorkbookStepGenerateRequest(BaseModel):
    title: str = ""
    prompt: str
    input_refs: list[str] = Field(default_factory=list)


class WorkbookStepReviseRequest(BaseModel):
    instruction: str
    input_refs: list[str] = Field(default_factory=list)


class WorkbookTemplateWrite(BaseModel):
    id: str
    name: str
    description: str = ""
    steps: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    properties: dict[str, str] = Field(default_factory=dict)


class WorkbookTemplateSummary(WorkbookTemplateWrite):
    path: str | None = None
    step_files: list[WorkbookStep] = Field(default_factory=list)
    workbook_count: int = 0


class WorkbookDataSource(BaseModel):
    id: str
    name: str
    path: str
    kind: str = "file"
    notes: str = ""


class WorkbookWrite(BaseModel):
    id: str
    title: str
    template_id: str
    linked_asset_id: str
    step_order: list[str] = Field(default_factory=list)
    data_sources: list[WorkbookDataSource] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    properties: dict[str, str] = Field(default_factory=dict)
    status: Literal["draft", "ready", "computing", "failed", "locked", "archived"] = "ready"


class WorkbookSummary(WorkbookWrite):
    path: str | None = None
    template_name: str | None = None
    linked_asset_name: str | None = None
    latest_execution_id: str | None = None
    latest_execution_status: str | None = None
    latest_execution_started_at: str | None = None
    updated_at: str | None = None


class PanelSummary(BaseModel):
    id: str
    title: str
    kind: Literal["chart", "report", "check"]
    step_id: str | None = None
    execution_id: str | None = None
    source_output_path: str | None = None
    status: str | None = None


class WorkbookDetail(BaseModel):
    workbook: WorkbookSummary
    template: WorkbookTemplateSummary
    steps: list[WorkbookStep] = Field(default_factory=list)
    panels: list[PanelSummary] = Field(default_factory=list)
    executions: list["ExecutionSummary"] = Field(default_factory=list)
    charts: list["ChartSummary"] = Field(default_factory=list)
    reports: list["ReportSummary"] = Field(default_factory=list)
    checks: list["CheckResult"] = Field(default_factory=list)


class WorkbookComputeRequest(BaseModel):
    step_ids: list[str] = Field(default_factory=list)


class WorkbookDuplicateRequest(BaseModel):
    id: str | None = None
    title: str | None = None
    linked_asset_id: str | None = None
    data_sources: list[WorkbookDataSource] | None = None


class CheckResult(BaseModel):
    id: str
    name: str
    status: Literal["pass", "warn", "fail"]
    step_id: str | None = None
    severity: Literal["info", "warning", "critical"] | None = None
    value: Any | None = None
    threshold: Any | None = None
    unit: str | None = None
    message: str = ""
    output_path: str | None = None

    @field_validator("severity", mode="before")
    @classmethod
    def normalize_empty_severity(cls, value: Any) -> Any:
        if isinstance(value, str) and value.strip().lower() in {"", "none", "null"}:
            return None
        return value


class ExecutionChecks(BaseModel):
    execution_id: str
    checks: list[CheckResult] = Field(default_factory=list)


class ExecutionSummary(BaseModel):
    id: str
    workspace_id: str | None = None
    workbook_id: str
    template_id: str
    target_type: str
    target_id: str
    linked_asset_id: str | None = None
    status: str
    started_at: str
    completed_at: str | None = None
    error: str | None = None
    workbook_git_commit: str | None = None
    log_count: int = 0
    check_counts: dict[str, int] = Field(default_factory=dict)


class ExecutionLogEntry(BaseModel):
    seq: int
    timestamp: str
    level: str
    source: Literal["runner", "stdout", "stderr"]
    message: str
    step_id: str | None = None


class ExecutionOutput(BaseModel):
    path: str
    name: str
    kind: str
    size: int


class ExecutionOutputPreview(BaseModel):
    path: str
    kind: str
    text: str | None = None
    json_value: Any | None = None


class ExecutionLogs(BaseModel):
    execution_id: str
    entries: list[ExecutionLogEntry] = Field(default_factory=list)
    text: str = ""


class ChatAttachment(BaseModel):
    type: Literal["workspace_file"]
    path: str
    title: str | None = None
    language: str | None = None
    label: str | None = None


class ChatActivityEvent(BaseModel):
    label: str
    status: Literal["ok", "error"] = "ok"
    detail: str | None = None
    duration_ms: float | None = None


class ChatSeedMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    chat_id: str | None = None
    message: str
    seed_messages: list[ChatSeedMessage] = Field(default_factory=list)
    mentions: list[ChatAttachment] = Field(default_factory=list)


class ChatResponse(BaseModel):
    chat_id: str
    assistant_message: str
    attachments: list[ChatAttachment] = Field(default_factory=list)
    activity: list[ChatActivityEvent] = Field(default_factory=list)


class ChatSummary(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int = 0


class Message(BaseModel):
    id: str
    role: str
    content: str
    created_at: str
    attachments: list[ChatAttachment] = Field(default_factory=list)
    activity: list[ChatActivityEvent] = Field(default_factory=list)


class ChatDetail(BaseModel):
    id: str
    messages: list[Message]


class DuckQueryRequest(BaseModel):
    sql: str


class DuckQueryResponse(BaseModel):
    columns: list[str]
    rows: list[dict[str, Any]]


class GitStatus(BaseModel):
    branch: str
    porcelain: list[str]
    diff: str


class CommitRequest(BaseModel):
    message: str


class DiscardRequest(BaseModel):
    confirm: bool = False
    include_untracked: bool = False
    paths: list[str] = Field(default_factory=list)


class DiscardResponse(BaseModel):
    discarded_tracked: list[str]
    discarded_untracked: list[str]
    skipped_untracked: list[str]
    backup_path: str


class ChartSummary(BaseModel):
    id: str
    title: str
    path: str
    figure: dict[str, Any]
    renderer: str = "plotly"
    workbook_id: str | None = None
    step_id: str | None = None
    execution_id: str | None = None
    source_output_path: str | None = None
    updated_at: str | None = None


class ReportSummary(BaseModel):
    id: str
    title: str
    path: str
    format: str
    workbook_id: str | None = None
    step_id: str | None = None
    execution_id: str | None = None
    source_output_path: str | None = None
    created_at: str | None = None
    chart_ids: list[str] = Field(default_factory=list)
