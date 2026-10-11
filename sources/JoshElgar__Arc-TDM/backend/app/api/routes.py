from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, Body, Depends, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

from app.core import (
    assets,
    auth as auth_core,
    components,
    control_db,
    duck,
    executions,
    execution_outputs as execution_output_core,
    files,
    git_service,
    project_settings,
    real_runs,
    reports,
    sandbox,
    charts,
    step_generation,
    workbooks,
)
from app.core import workspace as workspace_core
from app.core.timing import ChatTimer, activity_from_trace
from app.schemas.domain import (
    ChatDetail,
    ChatAttachment,
    ChatRequest,
    ChatResponse,
    ChatSeedMessage,
    ChatSummary,
    CommitRequest,
    ComponentModelDefinition,
    ComponentEventRequest,
    ComponentRecordingStartRequest,
    ComponentRecordingStartResponse,
    ComponentRecordingStopResponse,
    ComponentWorkbookCreateRequest,
    DatasetCreateRequest,
    DiscardRequest,
    DiscardResponse,
    DuckQueryRequest,
    DuckQueryResponse,
    ExecutionSummary,
    FileEntry,
    FilePreview,
    FileTablePage,
    GitStatus,
    Message,
    Principal,
    ProjectSettings,
    ProjectSummary,
    AssetSummary,
    AssetWrite,
    ExecutionChecks,
    ExecutionLogs,
    ReportSummary,
    ExecutionOutput,
    ExecutionOutputPreview,
    TestRunSummary,
    TestRunWrite,
    UploadResponse,
    ChartSummary,
    WorkbookComputeRequest,
    WorkbookDuplicateRequest,
    WorkbookStep,
    WorkbookStepGenerateRequest,
    WorkbookStepReviseRequest,
    WorkbookDetail,
    WorkbookSummary,
    WorkbookTemplateSummary,
    WorkbookTemplateWrite,
    WorkbookWrite,
    WorkspaceApiTokenCreateResponse,
    WorkspaceApiTokenStatus,
    WorkspaceFileRead,
    WorkspaceCreateRequest,
    WorkspaceSummary,
)

router = APIRouter(prefix="/api")

CHAT_CONTEXT_MESSAGE_LIMIT = 12
CHAT_CONTEXT_CONTENT_LIMIT = 4000
MAX_CHAT_FILE_ATTACHMENTS = 3


def current_principal(
    request: Request,
    x_clerk_user_id: str | None = Header(default=None),
    x_clerk_email: str | None = Header(default=None),
) -> Principal:
    return auth_core.principal_from_request(request, x_clerk_user_id, x_clerk_email)


def workspace_with_project_name(
    workspace: WorkspaceSummary,
    workspace_root: Path | None = None,
) -> WorkspaceSummary:
    root = workspace_root or Path(workspace.root_path)
    settings = project_settings.load_project_settings(root)
    return workspace.model_copy(update={"name": settings.name})


def ensure_bootstrapped_workspace(workspace: WorkspaceSummary) -> WorkspaceSummary:
    workspace_root = workspace_core.ensure_workspace(Path(workspace.root_path), workspace.name)
    return workspace_with_project_name(workspace, workspace_root)


def current_workspace(
    workspace_id: str,
    principal: Principal = Depends(current_principal),
) -> WorkspaceSummary:
    if principal.api_workspace_id:
        if principal.api_workspace_id != workspace_id:
            raise HTTPException(status_code=403, detail="Workspace access token cannot access this workspace")
        try:
            workspace = control_db.get_workspace(workspace_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail="Workspace not found") from exc
        workspace_root = workspace_core.ensure_workspace(Path(workspace.root_path), workspace.name)
        return workspace_with_project_name(workspace, workspace_root)

    try:
        workspace = control_db.get_workspace(workspace_id, user_id=principal.user_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Workspace not found") from exc
    workspace_root = workspace_core.ensure_workspace(Path(workspace.root_path), workspace.name)
    return workspace_with_project_name(workspace, workspace_root)


def current_workspace_root(workspace: WorkspaceSummary = Depends(current_workspace)) -> Path:
    return Path(workspace.root_path)


@router.get("/workspaces", response_model=list[WorkspaceSummary])
def workspace_list(principal: Principal = Depends(current_principal)) -> list[WorkspaceSummary]:
    if principal.api_workspace_id:
        return [ensure_bootstrapped_workspace(control_db.get_workspace(principal.api_workspace_id))]
    control_db.ensure_personal_workspace(principal.user_id)
    return [ensure_bootstrapped_workspace(workspace) for workspace in control_db.list_workspaces(principal.user_id)]


@router.post("/workspaces", response_model=WorkspaceSummary)
def workspace_create(
    request: WorkspaceCreateRequest,
    principal: Principal = Depends(current_principal),
) -> WorkspaceSummary:
    if principal.api_workspace_id:
        return ensure_bootstrapped_workspace(control_db.get_workspace(principal.api_workspace_id))
    existing = control_db.list_workspaces(principal.user_id)
    if existing:
        return ensure_bootstrapped_workspace(existing[0])
    workspace = control_db.create_workspace(principal.user_id, request.name)
    return ensure_bootstrapped_workspace(workspace)


@router.get("/workspaces/{workspace_id}/project", response_model=ProjectSummary)
def project(workspace: WorkspaceSummary = Depends(current_workspace)) -> ProjectSummary:
    chat_setup_message = sandbox.chat_setup_error()
    return ProjectSummary(
        workspace=workspace,
        chat_available=chat_setup_message is None,
        chat_setup_message=chat_setup_message,
        tabs=["Assets", "Runs", "Workbooks", "Chat", "Data", "Settings"],
    )


@router.get("/workspaces/{workspace_id}/settings", response_model=ProjectSettings)
def settings_detail(workspace_root: Path = Depends(current_workspace_root)) -> ProjectSettings:
    return project_settings.load_project_settings(workspace_root)


@router.put("/workspaces/{workspace_id}/settings", response_model=ProjectSettings)
def settings_update(
    request: ProjectSettings,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> ProjectSettings:
    saved = project_settings.save_project_settings(workspace_root, request)
    git_service.commit_paths_if_dirty(workspace_root, ["project.json"], "Update project settings")
    return saved


@router.get("/workspaces/{workspace_id}/api-token", response_model=WorkspaceApiTokenStatus)
def workspace_api_token_status(
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> WorkspaceApiTokenStatus:
    try:
        return control_db.get_workspace_api_token_status(workspace.id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Workspace not found") from exc


@router.post("/workspaces/{workspace_id}/api-token", response_model=WorkspaceApiTokenCreateResponse)
def workspace_api_token_create(
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> WorkspaceApiTokenCreateResponse:
    try:
        return control_db.replace_workspace_api_token(workspace.id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Workspace not found") from exc


@router.delete("/workspaces/{workspace_id}/api-token")
def workspace_api_token_delete(
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> dict[str, str]:
    try:
        control_db.delete_workspace_api_token(workspace.id)
        return {"status": "deleted"}
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Workspace not found") from exc


@router.get("/workspaces/{workspace_id}/files", response_model=list[FileEntry])
def file_list(workspace_root: Path = Depends(current_workspace_root)) -> list[FileEntry]:
    return files.list_user_files(workspace_root)


@router.post("/workspaces/{workspace_id}/files/upload", response_model=UploadResponse)
async def file_upload(
    upload: UploadFile = File(...),
    workspace_root: Path = Depends(current_workspace_root),
) -> UploadResponse:
    try:
        result = await files.upload_file(workspace_root, upload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_paths_if_dirty(
        workspace_root,
        [result.path, "files/manifests"],
        f"Upload file manifest: {result.path}",
    )
    return result


@router.post("/workspaces/{workspace_id}/files/upload-wizard", response_model=UploadResponse)
async def file_upload_wizard(
    uploads: list[UploadFile] = File(...),
    destination: str = Form("local"),
    name: str | None = Form(default=None),
    workspace_root: Path = Depends(current_workspace_root),
) -> UploadResponse:
    try:
        result = await files.upload_data_source(workspace_root, uploads, destination, name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_paths_if_dirty(
        workspace_root,
        [result.path, "files/manifests"],
        f"Upload data source: {result.path}",
    )
    return result


@router.post("/workspaces/{workspace_id}/files/datasets", response_model=UploadResponse)
def file_dataset_create(
    request: DatasetCreateRequest,
    workspace_root: Path = Depends(current_workspace_root),
) -> UploadResponse:
    try:
        metadata = files.create_dataset_metadata(workspace_root, request.path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Folder not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_paths_if_dirty(
        workspace_root,
        ["files/manifests"],
        f"Create dataset: {metadata['path']}",
    )
    return UploadResponse(
        path=str(metadata["path"]),
        size=int(metadata.get("size") or 0),
        kind="dataset",
        dataset_kind=str(metadata.get("dataset_kind") or "mixed"),
        status=str(metadata.get("status") or "ready"),
        member_count=int(metadata.get("member_count") or 0),
    )


@router.delete("/workspaces/{workspace_id}/files")
def file_delete(path: str, workspace_root: Path = Depends(current_workspace_root)) -> dict[str, str]:
    try:
        files.delete_data_file(workspace_root, path)
        git_service.commit_if_dirty(workspace_root, f"Delete file: {path}")
        return {"status": "deleted"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/files/preview", response_model=FilePreview)
def file_preview(path: str, workspace_root: Path = Depends(current_workspace_root)) -> FilePreview:
    try:
        return files.preview_file(workspace_root, path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/files/read", response_model=WorkspaceFileRead)
def file_read(path: str, workspace_root: Path = Depends(current_workspace_root)) -> WorkspaceFileRead:
    try:
        return files.read_workspace_text_file(workspace_root, path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/files/html")
def file_html(path: str, workspace_root: Path = Depends(current_workspace_root)) -> FileResponse:
    try:
        file_path = files.data_file_path(workspace_root, path)
        if file_path.suffix.lower() not in files.HTML_DATA_EXTENSIONS:
            raise ValueError("Only web data files can be previewed inline.")
        return FileResponse(
            file_path,
            media_type=files.data_file_media_type(file_path),
            filename=file_path.name,
            content_disposition_type="inline",
            headers=html_response_headers(),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/files/table", response_model=FileTablePage)
def file_table(
    path: str,
    page: int = 0,
    page_size: int = 100,
    group: str | None = None,
    channel: str | None = None,
    workspace_root: Path = Depends(current_workspace_root),
) -> FileTablePage:
    try:
        return files.table_file(
            workspace_root,
            path,
            page=page,
            page_size=page_size,
            tdms_group=group,
            tdms_channel=channel,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/component-models", response_model=list[ComponentModelDefinition])
def component_model_list() -> list[ComponentModelDefinition]:
    return components.list_component_models()


@router.get("/workspaces/{workspace_id}/assets/{asset_id}/component/stream")
def component_stream(
    asset_id: str,
    sample_rate_hz: int | None = None,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> StreamingResponse:
    try:
        stream = components.stream_samples(
            workspace.id,
            workspace_root,
            asset_id,
            sample_rate_hz=sample_rate_hz,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return StreamingResponse(stream, media_type="text/event-stream")


@router.post(
    "/workspaces/{workspace_id}/assets/{asset_id}/component/recordings/start",
    response_model=ComponentRecordingStartResponse,
)
def component_recording_start(
    asset_id: str,
    request: ComponentRecordingStartRequest,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> ComponentRecordingStartResponse:
    try:
        return components.start_recording(workspace.id, workspace_root, asset_id, request.sample_rate_hz)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    "/workspaces/{workspace_id}/assets/{asset_id}/component/recordings/{recording_id}/marker",
)
def component_recording_marker(
    asset_id: str,
    recording_id: str,
    request: ComponentEventRequest,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> dict[str, str]:
    try:
        components.add_event(workspace.id, workspace_root, asset_id, request.label)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "queued", "recording_id": recording_id}


@router.post(
    "/workspaces/{workspace_id}/assets/{asset_id}/component/recordings/{recording_id}/stop",
    response_model=ComponentRecordingStopResponse,
)
def component_recording_stop(
    asset_id: str,
    recording_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> ComponentRecordingStopResponse:
    try:
        result = components.stop_recording(workspace.id, workspace_root, asset_id, recording_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Recording not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_paths_if_dirty(
        workspace_root,
        [
            result.file_path,
            "files/manifests",
            f"assets/{result.asset_id}",
            f"runs/{result.run_id}",
        ],
        f"Record component data: {result.asset_id}",
    )
    return result


@router.post(
    "/workspaces/{workspace_id}/assets/{asset_id}/component/recordings/workbook",
    response_model=WorkbookSummary,
)
def component_recording_workbook_create(
    asset_id: str,
    request: ComponentWorkbookCreateRequest,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookSummary:
    try:
        workbook = components.create_workbook_from_recording(workspace.id, workspace_root, asset_id, request)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Recording not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Create component workbook: {workbook.title}")
    return workbook


@router.get("/workspaces/{workspace_id}/assets", response_model=list[AssetSummary])
def asset_list(workspace_root: Path = Depends(current_workspace_root)) -> list[AssetSummary]:
    return assets.list_assets(workspace_root)


@router.post("/workspaces/{workspace_id}/assets", response_model=AssetSummary)
def asset_create(
    request: AssetWrite,
    workspace_root: Path = Depends(current_workspace_root),
) -> AssetSummary:
    try:
        saved = assets.save_asset(workspace_root, request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Save asset: {saved.name}")
    return saved


@router.get("/workspaces/{workspace_id}/assets/{asset_id}", response_model=AssetSummary)
def asset_detail(asset_id: str, workspace_root: Path = Depends(current_workspace_root)) -> AssetSummary:
    try:
        return assets.get_asset(workspace_root, asset_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/workspaces/{workspace_id}/assets/{asset_id}", response_model=AssetSummary)
def asset_update(
    asset_id: str,
    request: AssetWrite,
    workspace_root: Path = Depends(current_workspace_root),
) -> AssetSummary:
    if request.id != asset_id:
        raise HTTPException(status_code=400, detail="Asset id mismatch")
    try:
        saved = assets.save_asset(workspace_root, request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Update asset: {saved.name}")
    return saved


@router.delete("/workspaces/{workspace_id}/assets/{asset_id}")
def asset_delete(asset_id: str, workspace_root: Path = Depends(current_workspace_root)) -> dict[str, str]:
    try:
        assets.delete_asset(workspace_root, asset_id)
        git_service.commit_if_dirty(workspace_root, f"Delete asset: {asset_id}")
        return {"status": "deleted"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/runs", response_model=list[TestRunSummary])
def test_run_list(
    asset_id: str | None = None,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> list[TestRunSummary]:
    return real_runs.list_runs(workspace_root, workspace_id=workspace.id, asset_id=asset_id)


@router.post("/workspaces/{workspace_id}/runs", response_model=TestRunSummary)
def test_run_create(
    request: TestRunWrite,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> TestRunSummary:
    try:
        saved = real_runs.save_run(workspace_root, request, workspace_id=workspace.id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Save run: {saved.name}")
    return saved


@router.get("/workspaces/{workspace_id}/runs/{run_id}", response_model=TestRunSummary)
def test_run_detail(
    run_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> TestRunSummary:
    try:
        return real_runs.get_run(workspace_root, run_id, workspace_id=workspace.id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Run not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/workspaces/{workspace_id}/runs/{run_id}", response_model=TestRunSummary)
def test_run_update(
    run_id: str,
    request: TestRunWrite,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> TestRunSummary:
    if request.id != run_id:
        raise HTTPException(status_code=400, detail="Run id mismatch")
    try:
        saved = real_runs.save_run(workspace_root, request, workspace_id=workspace.id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Asset not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Update run: {saved.name}")
    return saved


@router.delete("/workspaces/{workspace_id}/runs/{run_id}")
def test_run_delete(run_id: str, workspace_root: Path = Depends(current_workspace_root)) -> dict[str, str]:
    try:
        real_runs.delete_run(workspace_root, run_id)
        git_service.commit_if_dirty(workspace_root, f"Delete run: {run_id}")
        return {"status": "deleted"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Run not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/workbook-templates", response_model=list[WorkbookTemplateSummary])
def workbook_template_list(workspace_root: Path = Depends(current_workspace_root)) -> list[WorkbookTemplateSummary]:
    return workbooks.list_templates(workspace_root)


@router.post("/workspaces/{workspace_id}/workbook-templates", response_model=WorkbookTemplateSummary)
def workbook_template_create(
    request: WorkbookTemplateWrite,
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookTemplateSummary:
    try:
        saved = workbooks.save_template(workspace_root, request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Save workbook template: {saved.name}")
    return saved


@router.get("/workspaces/{workspace_id}/workbook-templates/{template_id}", response_model=WorkbookTemplateSummary)
def workbook_template_detail(
    template_id: str,
    kind: str | None = None,
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookTemplateSummary:
    try:
        return workbooks.get_template(workspace_root, template_id, kind=kind)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook template not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/workspaces/{workspace_id}/workbook-templates/{template_id}/steps/{step_id}", response_model=WorkbookStep)
def workbook_template_step_save(
    template_id: str,
    step_id: str,
    request: WorkbookStep,
    kind: str | None = None,
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookStep:
    if request.id != step_id:
        raise HTTPException(status_code=400, detail="Step id mismatch")
    try:
        saved = workbooks.save_template_step(workspace_root, template_id, request, kind=kind)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook template not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Save workbook step: {saved.title}")
    return saved


@router.get("/workspaces/{workspace_id}/workbooks", response_model=list[WorkbookSummary])
def workbook_list(
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> list[WorkbookSummary]:
    return workbooks.list_workbooks(workspace_root, workspace_id=workspace.id)


@router.post("/workspaces/{workspace_id}/workbooks", response_model=WorkbookSummary)
def workbook_create(
    request: WorkbookWrite,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookSummary:
    try:
        saved = workbooks.save_workbook(workspace_root, request, workspace_id=workspace.id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook target or template not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Save workbook: {saved.title}")
    return saved


@router.get("/workspaces/{workspace_id}/workbooks/{workbook_id}", response_model=WorkbookDetail)
def workbook_detail(
    workbook_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookDetail:
    try:
        return workbooks.get_workbook_detail(
            workspace_root,
            workbook_id,
            workspace_id=workspace.id,
            charts=charts.list_charts(workspace_root),
            reports=reports.list_reports(workspace_root),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/workspaces/{workspace_id}/workbooks/{workbook_id}", response_model=WorkbookSummary)
def workbook_update(
    workbook_id: str,
    request: WorkbookWrite,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookSummary:
    if request.id != workbook_id:
        raise HTTPException(status_code=400, detail="Workbook id mismatch")
    try:
        saved = workbooks.save_workbook(workspace_root, request, workspace_id=workspace.id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook target or template not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Update workbook: {saved.title}")
    return saved


@router.post("/workspaces/{workspace_id}/workbooks/{workbook_id}/duplicate", response_model=WorkbookSummary)
def workbook_duplicate(
    workbook_id: str,
    request: WorkbookDuplicateRequest,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookSummary:
    try:
        saved = workbooks.duplicate_workbook(
            workspace_root,
            workbook_id,
            new_id=request.id,
            title=request.title,
            linked_asset_id=request.linked_asset_id,
            data_sources=request.data_sources,
            workspace_id=workspace.id,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Duplicate workbook: {saved.title}")
    return saved


@router.post("/workspaces/{workspace_id}/workbooks/{workbook_id}/steps/generate", response_model=WorkbookStep)
async def workbook_step_generate(
    workbook_id: str,
    request: WorkbookStepGenerateRequest,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookStep:
    try:
        return await step_generation.generate_workbook_step(
            workspace_root=workspace_root,
            workbook_id=workbook_id,
            title=request.title,
            prompt=request.prompt,
            input_refs=request.input_refs,
            workspace_id=workspace.id,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/workbooks/{workbook_id}/steps/{step_id}/revise", response_model=WorkbookStep)
async def workbook_step_revise(
    workbook_id: str,
    step_id: str,
    request: WorkbookStepReviseRequest,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookStep:
    try:
        return await step_generation.revise_workbook_step(
            workspace_root=workspace_root,
            workbook_id=workbook_id,
            step_id=step_id,
            instruction=request.instruction,
            input_refs=request.input_refs,
            workspace_id=workspace.id,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Step not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.put("/workspaces/{workspace_id}/workbooks/{workbook_id}/steps/{step_id}", response_model=WorkbookStep)
def workbook_step_save(
    workbook_id: str,
    step_id: str,
    request: WorkbookStep,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> WorkbookStep:
    if request.id != step_id:
        raise HTTPException(status_code=400, detail="Step id mismatch")
    try:
        saved = workbooks.save_workbook_step(workspace_root, workbook_id, request, workspace_id=workspace.id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    git_service.commit_if_dirty(workspace_root, f"Save workbook step: {saved.title}")
    return saved


@router.delete("/workspaces/{workspace_id}/workbooks/{workbook_id}/steps/{step_id}")
def workbook_step_delete(
    workbook_id: str,
    step_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> dict[str, str]:
    try:
        workbooks.delete_workbook_step(workspace_root, workbook_id, step_id, workspace_id=workspace.id)
        git_service.commit_if_dirty(workspace_root, f"Delete workbook step: {step_id}")
        return {"status": "deleted"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Step not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/workspaces/{workspace_id}/workbooks/{workbook_id}")
def workbook_delete(workbook_id: str, workspace_root: Path = Depends(current_workspace_root)) -> dict[str, str]:
    try:
        workbooks.delete_workbook(workspace_root, workbook_id)
        git_service.commit_if_dirty(workspace_root, f"Delete workbook: {workbook_id}")
        return {"status": "deleted"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/workbooks/{workbook_id}/compute", response_model=ExecutionSummary)
def workbook_compute(
    workbook_id: str,
    request: WorkbookComputeRequest | None = Body(default=None),
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> ExecutionSummary:
    try:
        return executions.start_workbook_execution(
            workspace.id,
            workspace_root,
            workbook_id,
            step_ids=request.step_ids if request else [],
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Workbook not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/executions", response_model=list[ExecutionSummary])
def execution_list(
    workbook_id: str | None = None,
    target_type: str | None = None,
    target_id: str | None = None,
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> list[ExecutionSummary]:
    return control_db.list_executions(workspace.id, workbook_id=workbook_id, target_type=target_type, target_id=target_id)


@router.get("/workspaces/{workspace_id}/executions/{execution_id}", response_model=ExecutionSummary)
def execution_detail(
    execution_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> ExecutionSummary:
    try:
        return control_db.get_execution_for_workspace(workspace.id, execution_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Execution not found") from exc


@router.get("/workspaces/{workspace_id}/executions/{execution_id}/logs/stream")
def execution_log_stream(
    execution_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> StreamingResponse:
    try:
        execution_dir = control_db.get_execution_path_for_workspace(workspace.id, execution_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Execution not found") from exc
    if not execution_dir.exists():
        raise HTTPException(status_code=404, detail="Execution logs not found")
    return StreamingResponse(execution_output_core.stream_logs(execution_dir), media_type="text/event-stream")


@router.get("/workspaces/{workspace_id}/executions/{execution_id}/logs", response_model=ExecutionLogs)
def execution_logs(
    execution_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> ExecutionLogs:
    try:
        execution_dir = control_db.get_execution_path_for_workspace(workspace.id, execution_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Execution not found") from exc
    return execution_output_core.read_logs(execution_dir, execution_id)


@router.get("/workspaces/{workspace_id}/executions/{execution_id}/checks", response_model=ExecutionChecks)
def execution_checks(
    execution_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> ExecutionChecks:
    try:
        execution_dir = control_db.get_execution_path_for_workspace(workspace.id, execution_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Execution not found") from exc
    return execution_output_core.read_checks(execution_dir, execution_id)


@router.get("/workspaces/{workspace_id}/executions/{execution_id}/outputs", response_model=list[ExecutionOutput])
def execution_output_list(
    execution_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> list[ExecutionOutput]:
    try:
        execution_dir = control_db.get_execution_path_for_workspace(workspace.id, execution_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Execution not found") from exc
    return execution_output_core.list_outputs(execution_dir)


@router.get("/workspaces/{workspace_id}/executions/{execution_id}/outputs/preview", response_model=ExecutionOutputPreview)
def execution_output_preview(
    execution_id: str,
    path: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> ExecutionOutputPreview:
    try:
        execution_dir = control_db.get_execution_path_for_workspace(workspace.id, execution_id)
        return execution_output_core.preview_output(execution_dir, path)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Execution not found") from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Execution output not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/workspaces/{workspace_id}/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    principal: Principal = Depends(current_principal),
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> ChatResponse:
    timer = ChatTimer()
    with timer.span("chat.resolve_chat", has_existing_chat=bool(request.chat_id)):
        chat_id = request.chat_id
        existing_messages: list[Message] = []
        if request.chat_id:
            try:
                control_db.ensure_chat_in_workspace(request.chat_id, workspace.id)
            except KeyError as exc:
                raise HTTPException(status_code=404, detail="Chat not found") from exc
            existing_messages = control_db.list_messages(request.chat_id, workspace.id)

    with timer.span("chat.resolve_user_mentions"):
        user_mentions = _validated_chat_mentions(workspace_root, request.mentions, request.message)
    with timer.span("chat.resolve_file_attachment"):
        direct_attachments = _direct_file_attachments(
            workspace_root,
            [*existing_messages, _pending_user_message(request.message, user_mentions)],
        )
    if direct_attachments:
        if chat_id is None:
            chat_id = control_db.create_chat(
                workspace.id,
                principal.user_id,
                request.message[:60] or "New chat",
            )
            _save_seed_messages(chat_id, request.seed_messages)
        with timer.span("chat.save_user_message"):
            control_db.add_message(chat_id, "user", request.message, attachments=user_mentions)
        assistant_message = _file_attachment_message(direct_attachments)
        with timer.span("chat.save_assistant_message"):
            control_db.add_message(chat_id, "assistant", assistant_message, attachments=direct_attachments)
        return ChatResponse(
            chat_id=chat_id,
            assistant_message=assistant_message,
            attachments=direct_attachments,
        )

    chat_setup_message = sandbox.chat_setup_error()
    if chat_setup_message:
        raise HTTPException(status_code=503, detail=chat_setup_message)

    if chat_id is None:
        chat_id = control_db.create_chat(
            workspace.id,
            principal.user_id,
            request.message[:60] or "New chat",
        )
        _save_seed_messages(chat_id, request.seed_messages)
    with timer.span("chat.save_user_message"):
        control_db.add_message(chat_id, "user", request.message, attachments=user_mentions)
    with timer.span("chat.load_context"):
        chat_messages = control_db.list_messages(chat_id, workspace.id)

    try:
        with timer.span("chat.sandbox_respond"):
            assistant_message = await sandbox.SandboxService(
                workspace_root,
                workspace_id=workspace.id,
            ).respond(_sandbox_chat_prompt(chat_messages), timer=timer)
    except Exception as exc:
        assistant_message = f"Arc Agent could not complete the request. {_safe_sandbox_error(exc)}"
    if not assistant_message:
        assistant_message = "Arc Agent could not complete the request."
    with timer.span("chat.extract_file_attachments"):
        attachments = (
            _workspace_file_attachments_from_text(workspace_root, assistant_message)
            if _is_file_view_request(request.message)
            else []
        )
    activity = activity_from_trace(timer.finish())
    with timer.span("chat.save_assistant_message"):
        control_db.add_message(chat_id, "assistant", assistant_message, attachments=attachments, activity=activity)
    return ChatResponse(
        chat_id=chat_id,
        assistant_message=assistant_message,
        attachments=attachments,
        activity=activity,
    )


@router.get("/workspaces/{workspace_id}/chats", response_model=list[ChatSummary])
def chat_history(
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> list[ChatSummary]:
    return control_db.list_chats(workspace.id)


@router.get("/workspaces/{workspace_id}/chat/{chat_id}", response_model=ChatDetail)
def chat_detail(
    chat_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
) -> ChatDetail:
    try:
        messages = control_db.list_messages(chat_id, workspace.id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Chat not found") from exc
    return ChatDetail(id=chat_id, messages=messages)


def _pending_user_message(
    content: str,
    attachments: list[ChatAttachment] | None = None,
) -> Message:
    return Message(id="pending", role="user", content=content, attachments=attachments or [], created_at="")


def _save_seed_messages(chat_id: str, seed_messages: list[ChatSeedMessage]) -> None:
    for message in seed_messages:
        control_db.add_message(chat_id, message.role, message.content)


def _validated_chat_mentions(
    workspace_root: Path,
    mentions: list[ChatAttachment],
    message: str,
) -> list[ChatAttachment]:
    clean_mentions: list[ChatAttachment] = []
    seen: set[tuple[str, str | None]] = set()
    for mention in mentions:
        attachment = _workspace_file_attachment(workspace_root, mention.path)
        if not attachment:
            continue
        label = _clean_mention_label(mention.label)
        if mention.label and (not label or label not in message):
            continue
        key = (attachment.path, label)
        if key in seen:
            continue
        seen.add(key)
        clean_mentions.append(attachment.model_copy(update={"label": label}))
    return clean_mentions


def _clean_mention_label(label: str | None) -> str | None:
    if not label:
        return None
    clean = label.strip()
    if not clean.startswith("@") or any(character.isspace() for character in clean):
        return None
    if len(clean) > 260:
        return None
    return clean


def _direct_file_attachments(workspace_root: Path, messages: list[Message]) -> list[ChatAttachment]:
    if not messages:
        return []

    latest_message = messages[-1]
    latest = latest_message.content
    is_confirmation = _is_short_confirmation(latest)
    if not _is_file_view_request(latest) and not is_confirmation:
        return []

    direct = _workspace_file_attachments_from_text(workspace_root, latest)
    if direct:
        return direct[:1]
    if latest_message.attachments:
        return [
            attachment
            for attachment in latest_message.attachments
            if attachment.type == "workspace_file"
        ][:1]

    if not _is_file_followup(latest) and not is_confirmation:
        return []

    for message in reversed(messages[:-1]):
        attachments = [
            attachment for attachment in message.attachments if attachment.type == "workspace_file"
        ]
        if attachments:
            return attachments[:1]
        mentions = _workspace_file_attachments_from_text(workspace_root, message.content)
        if mentions:
            return mentions[:1]
    return []


def _is_short_confirmation(message: str) -> bool:
    return message.strip().lower() in {"yes", "yep", "yeah", "please", "do it", "that", "show it"}


def _is_file_followup(message: str) -> bool:
    lower = message.lower()
    return any(phrase in lower for phrase in ("whole script", "full script", "the script", "the file"))


def _is_file_view_request(message: str) -> bool:
    lower = message.lower()
    action = any(
        phrase in lower
        for phrase in (
            "show",
            "open",
            "view",
            "display",
            "give me",
            "read",
            "whole",
            "full",
        )
    )
    target = any(phrase in lower for phrase in ("file", "script", "main.py", ".py", ".sql", ".json", ".md"))
    return action and target


def _workspace_file_attachments_from_text(workspace_root: Path, text: str) -> list[ChatAttachment]:
    attachments: list[ChatAttachment] = []
    seen: set[str] = set()
    for raw_candidate in _path_candidates(text):
        attachment = _workspace_file_attachment(workspace_root, raw_candidate)
        if not attachment or attachment.path in seen:
            continue
        seen.add(attachment.path)
        attachments.append(attachment)
        if len(attachments) >= MAX_CHAT_FILE_ATTACHMENTS:
            break
    return attachments


def _path_candidates(text: str) -> list[str]:
    candidates: list[str] = []
    for quoted in re.findall(r"`([^`]+)`", text):
        candidates.append(quoted)
    for token in re.findall(r"[A-Za-z0-9_./~:-]+", text):
        if "/" in token or "." in token:
            candidates.append(token)
    return candidates


def _workspace_file_attachment(workspace_root: Path, raw_path: str) -> ChatAttachment | None:
    candidate = raw_path.strip().strip("'\".,;()[]{}")
    candidate = re.sub(r":\d+(?::\d+)?$", "", candidate)
    candidate = candidate.removeprefix("./")
    workspace_root_resolved = workspace_root.resolve()
    workspace_prefix = workspace_root_resolved.as_posix().rstrip("/") + "/"
    if candidate.startswith(workspace_prefix):
        candidate = candidate[len(workspace_prefix) :]
    if candidate.startswith("workspace/"):
        candidate = candidate[len("workspace/") :]
    if not candidate or candidate.endswith("/"):
        return None

    try:
        target = files.safe_path(workspace_root, candidate)
    except ValueError:
        return None
    if not target.exists() or not target.is_file():
        return None

    relative_path = target.relative_to(workspace_root_resolved).as_posix()
    if files.is_hidden_workspace_path(relative_path):
        return None
    return ChatAttachment(
        type="workspace_file",
        path=relative_path,
        title=target.name,
        language=files.language_for_path(target),
    )


def _file_attachment_message(attachments: list[ChatAttachment]) -> str:
    if len(attachments) == 1:
        return f"Here’s `{attachments[0].path}`."
    lines = "\n".join(f"- `{attachment.path}`" for attachment in attachments)
    return f"I found these files:\n{lines}"


@router.post("/workspaces/{workspace_id}/duckdb/query", response_model=DuckQueryResponse)
def duckdb_query(
    request: DuckQueryRequest,
    workspace_root: Path = Depends(current_workspace_root),
) -> DuckQueryResponse:
    try:
        return duck.query(workspace_root, request.sql)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/git/status", response_model=GitStatus)
def git_status(workspace_root: Path = Depends(current_workspace_root)) -> GitStatus:
    return GitStatus(
        branch=git_service.branch(workspace_root),
        porcelain=git_service.status(workspace_root),
        diff=git_service.diff(workspace_root),
    )


@router.post("/workspaces/{workspace_id}/git/commit")
def git_commit(
    request: CommitRequest,
    workspace_root: Path = Depends(current_workspace_root),
) -> dict[str, str]:
    return {"output": git_service.commit_all(workspace_root, request.message)}


@router.post("/workspaces/{workspace_id}/git/discard", response_model=DiscardResponse)
def git_discard(
    request: DiscardRequest,
    workspace_root: Path = Depends(current_workspace_root),
) -> DiscardResponse:
    if not request.confirm:
        raise HTTPException(status_code=400, detail="Discard requires confirm=true.")
    try:
        return git_service.discard_changes(
            workspace_root,
            paths=request.paths,
            include_untracked=request.include_untracked,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/charts", response_model=list[ChartSummary])
def chart_list(workspace_root: Path = Depends(current_workspace_root)) -> list[ChartSummary]:
    return charts.list_charts(workspace_root)


@router.delete("/workspaces/{workspace_id}/charts/{chart_id}")
def chart_delete(
    chart_id: str,
    workspace_root: Path = Depends(current_workspace_root),
) -> dict[str, str]:
    try:
        charts.delete_chart(workspace_root, chart_id)
        git_service.commit_if_dirty(workspace_root, f"Delete chart: {chart_id}")
        return {"status": "deleted"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Chart not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/reports", response_model=list[ReportSummary])
def report_list(workspace_root: Path = Depends(current_workspace_root)) -> list[ReportSummary]:
    return reports.list_reports(workspace_root)


@router.get("/workspaces/{workspace_id}/reports/{report_id}/file")
def report_file(report_id: str, workspace_root: Path = Depends(current_workspace_root)) -> FileResponse:
    try:
        path = reports.report_file_path(workspace_root, report_id)
        return FileResponse(
            path,
            media_type=reports.report_media_type(path),
            filename=path.name,
            content_disposition_type="inline",
            headers=report_response_headers(path),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Report file not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/workspaces/{workspace_id}/reports/{report_id}/download")
def report_download(report_id: str, workspace_root: Path = Depends(current_workspace_root)) -> FileResponse:
    try:
        path = reports.report_file_path(workspace_root, report_id)
        return FileResponse(
            path,
            media_type=reports.report_media_type(path),
            filename=path.name,
            headers=report_response_headers(path),
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Report file not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def report_response_headers(path: Path) -> dict[str, str]:
    if reports.report_media_type(path).startswith("text/html"):
        return html_response_headers()
    return {}


def html_response_headers() -> dict[str, str]:
    return {
        "Content-Security-Policy": (
            "default-src 'none'; "
            "style-src 'unsafe-inline'; "
            "img-src data:; "
            "font-src data:; "
            "base-uri 'none'; "
            "form-action 'none'; "
            "frame-ancestors 'self'"
        ),
        "X-Content-Type-Options": "nosniff",
    }


@router.post("/workspaces/{workspace_id}/reports/{report_id}/refresh", response_model=ExecutionSummary)
def report_refresh(
    report_id: str,
    workspace: WorkspaceSummary = Depends(current_workspace),
    workspace_root: Path = Depends(current_workspace_root),
) -> ExecutionSummary:
    try:
        report = reports.get_report(workspace_root, report_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Report not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not report.workbook_id:
        raise HTTPException(status_code=400, detail="Report is not linked to a workbook.")
    return executions.start_workbook_execution(workspace.id, workspace_root, report.workbook_id)


@router.delete("/workspaces/{workspace_id}/reports/{report_id}")
def report_delete(
    report_id: str,
    workspace_root: Path = Depends(current_workspace_root),
) -> dict[str, str]:
    try:
        reports.delete_report(workspace_root, report_id)
        git_service.commit_if_dirty(workspace_root, f"Delete report: {report_id}")
        return {"status": "deleted"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Report not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _safe_sandbox_error(exc: Exception) -> str:
    return "Check the app logs for details."


def _sandbox_chat_prompt(messages: list[Message]) -> str:
    recent_messages = messages[-CHAT_CONTEXT_MESSAGE_LIMIT:]
    transcript = "\n\n".join(
        f"{message.role.upper()}:\n{_chat_message_prompt_content(message)}" for message in recent_messages
    )
    return (
        "Use the recent chat transcript to interpret the user's latest request. "
        "If the latest user message is a short confirmation like 'yes', 'do that', or 'please do', "
        "resolve it against the immediately previous assistant offer and act on that request.\n\n"
        "Recent transcript, oldest to newest:\n"
        f"{transcript}\n\n"
        "Act on the latest user message."
    )


def _chat_message_prompt_content(message: Message) -> str:
    content = _truncate_chat_content(message.content)
    mentions = [
        attachment
        for attachment in message.attachments
        if attachment.type == "workspace_file" and attachment.path
    ]
    if not mentions:
        return content
    mention_lines = "\n".join(
        f"- {(attachment.label or attachment.title or attachment.path)} -> {attachment.path}"
        for attachment in mentions
    )
    return f"{content}\n\nMentioned workspace files:\n{mention_lines}"


def _truncate_chat_content(content: str) -> str:
    stripped = content.strip()
    if len(stripped) <= CHAT_CONTEXT_CONTENT_LIMIT:
        return stripped
    return f"{stripped[:CHAT_CONTEXT_CONTENT_LIMIT].rstrip()}\n[truncated]"
