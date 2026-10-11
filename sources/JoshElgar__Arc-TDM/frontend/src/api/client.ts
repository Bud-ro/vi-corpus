import type {
  AssetSummary,
  AssetInput,
  ChatAttachment,
  ChatResponse,
  ChatDetail,
  ChatSeedMessage,
  ChatSummary,
  ComponentModelDefinition,
  ComponentRecordingStartResponse,
  ComponentRecordingStopResponse,
  ExecutionChecks,
  ExecutionLogs,
  ExecutionOutput,
  ExecutionOutputPreview,
  ExecutionSummary,
  FileEntry,
  FilePreview,
  FileTablePage,
  GitStatus,
  ProjectSettings,
  ProjectSummary,
  ReportSummary,
  TestRunSummary,
  TestRunInput,
  UploadResponse,
  ChartSummary,
  WorkbookStep,
  WorkbookStepGenerateInput,
  WorkbookStepReviseInput,
  WorkbookDetail,
  WorkbookDuplicateInput,
  WorkbookSummary,
  WorkbookInput,
  WorkbookTemplateInput,
  WorkbookTemplateSummary,
  WorkspaceApiTokenCreateResponse,
  WorkspaceApiTokenStatus,
  WorkspaceFileRead,
  WorkspaceSummary
} from "./types";

type AuthTokenProvider = () => Promise<string | null>;

let authTokenProvider: AuthTokenProvider | null = null;

export function setAuthTokenProvider(provider: AuthTokenProvider | null) {
  authTokenProvider = provider;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const tokenHeaders = await authHeaders();
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...tokenHeaders,
      ...(options?.headers ?? {})
    },
    ...options
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(body.detail ?? response.statusText);
  }
  return response.json() as Promise<T>;
}

function workspacePath(workspaceId: string, path: string) {
  return `/api/workspaces/${encodeURIComponent(workspaceId)}${path}`;
}

async function authHeaders(): Promise<Record<string, string>> {
  const token = authTokenProvider ? await authTokenProvider() : null;
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export const api = {
  workspaces: () => request<WorkspaceSummary[]>("/api/workspaces"),
  createWorkspace: (name: string) =>
    request<WorkspaceSummary>("/api/workspaces", {
      method: "POST",
      body: JSON.stringify({ name })
    }),
  project: (workspaceId: string) => request<ProjectSummary>(workspacePath(workspaceId, "/project")),
  settings: (workspaceId: string) => request<ProjectSettings>(workspacePath(workspaceId, "/settings")),
  saveSettings: (workspaceId: string, settings: ProjectSettings) =>
    request<ProjectSettings>(workspacePath(workspaceId, "/settings"), {
      method: "PUT",
      body: JSON.stringify(settings)
    }),
  workspaceApiToken: (workspaceId: string) =>
    request<WorkspaceApiTokenStatus>(workspacePath(workspaceId, "/api-token")),
  generateWorkspaceApiToken: (workspaceId: string) =>
    request<WorkspaceApiTokenCreateResponse>(workspacePath(workspaceId, "/api-token"), {
      method: "POST"
    }),
  deleteWorkspaceApiToken: (workspaceId: string) =>
    request<{ status: string }>(workspacePath(workspaceId, "/api-token"), {
      method: "DELETE"
    }),
  files: (workspaceId: string) => request<FileEntry[]>(workspacePath(workspaceId, "/files")),
  previewFile: (workspaceId: string, path: string) =>
    request<FilePreview>(workspacePath(workspaceId, `/files/preview?path=${encodeURIComponent(path)}`)),
  readWorkspaceFile: (workspaceId: string, path: string) =>
    request<WorkspaceFileRead>(workspacePath(workspaceId, `/files/read?path=${encodeURIComponent(path)}`)),
  fileHtmlUrl: (workspaceId: string, path: string) =>
    workspacePath(workspaceId, `/files/html?path=${encodeURIComponent(path)}`),
  fileTable: (
    workspaceId: string,
    path: string,
    page = 0,
    pageSize = 100,
    tdmsChannel?: { group_name: string; channel_name: string }
  ) => {
    const channelParams = tdmsChannel
      ? `&group=${encodeURIComponent(tdmsChannel.group_name)}&channel=${encodeURIComponent(tdmsChannel.channel_name)}`
      : "";
    return request<FileTablePage>(
      workspacePath(
        workspaceId,
        `/files/table?path=${encodeURIComponent(path)}&page=${page}&page_size=${pageSize}${channelParams}`
      )
    );
  },
  uploadFile: async (workspaceId: string, file: File) => {
    const form = new FormData();
    form.append("upload", file);
    const response = await fetch(workspacePath(workspaceId, "/files/upload"), {
      method: "POST",
      headers: await authHeaders(),
      body: form
    });
    if (!response.ok) throw new Error((await response.json()).detail ?? "Upload failed");
    return response.json() as Promise<UploadResponse>;
  },
  uploadDataSource: async (workspaceId: string, files: File[], destination: "local" | "shared", name?: string) => {
    const form = new FormData();
    files.forEach((file) => form.append("uploads", file));
    form.append("destination", destination);
    if (name?.trim()) form.append("name", name.trim());
    const response = await fetch(workspacePath(workspaceId, "/files/upload-wizard"), {
      method: "POST",
      headers: await authHeaders(),
      body: form
    });
    if (!response.ok) throw new Error((await response.json()).detail ?? "Upload failed");
    return response.json() as Promise<UploadResponse>;
  },
  createDataset: (workspaceId: string, path: string) =>
    request<UploadResponse>(workspacePath(workspaceId, "/files/datasets"), {
      method: "POST",
      body: JSON.stringify({ path })
    }),
  deleteFile: (workspaceId: string, path: string) =>
    request<{ status: string }>(workspacePath(workspaceId, `/files?path=${encodeURIComponent(path)}`), {
      method: "DELETE"
    }),
  componentModels: (workspaceId: string) =>
    request<ComponentModelDefinition[]>(workspacePath(workspaceId, "/component-models")),
  componentStreamUrl: (workspaceId: string, assetId: string, sampleRateHz?: number) =>
    workspacePath(
      workspaceId,
      `/assets/${encodeURIComponent(assetId)}/component/stream${
        sampleRateHz ? `?sample_rate_hz=${encodeURIComponent(sampleRateHz)}` : ""
      }`
    ),
  startComponentRecording: (workspaceId: string, assetId: string, sampleRateHz?: number) =>
    request<ComponentRecordingStartResponse>(
      workspacePath(workspaceId, `/assets/${encodeURIComponent(assetId)}/component/recordings/start`),
      {
        method: "POST",
        body: JSON.stringify({ sample_rate_hz: sampleRateHz })
      }
    ),
  markComponentRecording: (workspaceId: string, assetId: string, recordingId: string, label: string) =>
    request<{ status: string; recording_id: string }>(
      workspacePath(
        workspaceId,
        `/assets/${encodeURIComponent(assetId)}/component/recordings/${encodeURIComponent(recordingId)}/marker`
      ),
      {
        method: "POST",
        body: JSON.stringify({ label })
      }
    ),
  stopComponentRecording: (workspaceId: string, assetId: string, recordingId: string) =>
    request<ComponentRecordingStopResponse>(
      workspacePath(
        workspaceId,
        `/assets/${encodeURIComponent(assetId)}/component/recordings/${encodeURIComponent(recordingId)}/stop`
      ),
      {
        method: "POST"
      }
    ),
  createComponentWorkbook: (workspaceId: string, assetId: string, recordingId: string, title?: string) =>
    request<WorkbookSummary>(
      workspacePath(workspaceId, `/assets/${encodeURIComponent(assetId)}/component/recordings/workbook`),
      {
      method: "POST",
      body: JSON.stringify({ recording_id: recordingId, title })
      }
    ),
  assets: (workspaceId: string) => request<AssetSummary[]>(workspacePath(workspaceId, "/assets")),
  asset: (workspaceId: string, id: string) =>
    request<AssetSummary>(workspacePath(workspaceId, `/assets/${encodeURIComponent(id)}`)),
  saveAsset: (workspaceId: string, asset: AssetInput) =>
    request<AssetSummary>(workspacePath(workspaceId, `/assets/${encodeURIComponent(asset.id)}`), {
      method: "PUT",
      body: JSON.stringify(asset)
    }),
  deleteAsset: (workspaceId: string, id: string) =>
    request<{ status: string }>(workspacePath(workspaceId, `/assets/${encodeURIComponent(id)}`), {
      method: "DELETE"
    }),
  runs: (workspaceId: string, assetId?: string) =>
    request<TestRunSummary[]>(
      workspacePath(workspaceId, assetId ? `/runs?asset_id=${encodeURIComponent(assetId)}` : "/runs")
    ),
  run: (workspaceId: string, id: string) =>
    request<TestRunSummary>(workspacePath(workspaceId, `/runs/${encodeURIComponent(id)}`)),
  saveRun: (workspaceId: string, run: TestRunInput) =>
    request<TestRunSummary>(workspacePath(workspaceId, `/runs/${encodeURIComponent(run.id)}`), {
      method: "PUT",
      body: JSON.stringify(run)
    }),
  workbookTemplates: (workspaceId: string) =>
    request<WorkbookTemplateSummary[]>(workspacePath(workspaceId, "/workbook-templates")),
  saveWorkbookTemplate: (workspaceId: string, template: WorkbookTemplateInput) =>
    request<WorkbookTemplateSummary>(workspacePath(workspaceId, "/workbook-templates"), {
      method: "POST",
      body: JSON.stringify(template)
    }),
  saveWorkbookStep: (workspaceId: string, workbookId: string, step: WorkbookStep) =>
    request<WorkbookStep>(
      workspacePath(
        workspaceId,
        `/workbooks/${encodeURIComponent(workbookId)}/steps/${encodeURIComponent(step.id)}`
      ),
      {
        method: "PUT",
        body: JSON.stringify(step)
      }
    ),
  deleteWorkbookStep: (workspaceId: string, workbookId: string, stepId: string) =>
    request<{ status: string }>(
      workspacePath(workspaceId, `/workbooks/${encodeURIComponent(workbookId)}/steps/${encodeURIComponent(stepId)}`),
      { method: "DELETE" }
    ),
  generateWorkbookStep: (workspaceId: string, workbookId: string, input: WorkbookStepGenerateInput) =>
    request<WorkbookStep>(workspacePath(workspaceId, `/workbooks/${encodeURIComponent(workbookId)}/steps/generate`), {
      method: "POST",
      body: JSON.stringify(input)
    }),
  reviseWorkbookStep: (workspaceId: string, workbookId: string, stepId: string, input: WorkbookStepReviseInput) =>
    request<WorkbookStep>(
      workspacePath(
        workspaceId,
        `/workbooks/${encodeURIComponent(workbookId)}/steps/${encodeURIComponent(stepId)}/revise`
      ),
      {
        method: "POST",
        body: JSON.stringify(input)
      }
    ),
  workbooks: (workspaceId: string) => request<WorkbookSummary[]>(workspacePath(workspaceId, "/workbooks")),
  workbook: (workspaceId: string, id: string) =>
    request<WorkbookDetail>(workspacePath(workspaceId, `/workbooks/${encodeURIComponent(id)}`)),
  saveWorkbook: (workspaceId: string, workbook: WorkbookInput) =>
    request<WorkbookSummary>(workspacePath(workspaceId, `/workbooks/${encodeURIComponent(workbook.id)}`), {
      method: "PUT",
      body: JSON.stringify(workbook)
    }),
  duplicateWorkbook: (workspaceId: string, workbookId: string, duplicate: WorkbookDuplicateInput) =>
    request<WorkbookSummary>(workspacePath(workspaceId, `/workbooks/${encodeURIComponent(workbookId)}/duplicate`), {
      method: "POST",
      body: JSON.stringify(duplicate)
    }),
  computeWorkbook: (workspaceId: string, id: string, stepIds: string[] = []) =>
    request<ExecutionSummary>(workspacePath(workspaceId, `/workbooks/${encodeURIComponent(id)}/compute`), {
      method: "POST",
      body: JSON.stringify({ step_ids: stepIds })
    }),
  executions: (workspaceId: string, workbookId?: string) =>
    request<ExecutionSummary[]>(
      workspacePath(
        workspaceId,
        workbookId ? `/executions?workbook_id=${encodeURIComponent(workbookId)}` : "/executions"
      )
    ),
  executionOutputs: (workspaceId: string, executionId: string) =>
    request<ExecutionOutput[]>(workspacePath(workspaceId, `/executions/${encodeURIComponent(executionId)}/outputs`)),
  previewExecutionOutput: (workspaceId: string, executionId: string, path: string) =>
    request<ExecutionOutputPreview>(
      workspacePath(
        workspaceId,
        `/executions/${encodeURIComponent(executionId)}/outputs/preview?path=${encodeURIComponent(path)}`
      )
    ),
  executionLogStreamUrl: (workspaceId: string, executionId: string) =>
    workspacePath(workspaceId, `/executions/${encodeURIComponent(executionId)}/logs/stream`),
  executionLogs: (workspaceId: string, executionId: string) =>
    request<ExecutionLogs>(workspacePath(workspaceId, `/executions/${encodeURIComponent(executionId)}/logs`)),
  executionChecks: (workspaceId: string, executionId: string) =>
    request<ExecutionChecks>(workspacePath(workspaceId, `/executions/${encodeURIComponent(executionId)}/checks`)),
  chat: (
    workspaceId: string,
    message: string,
    chatId?: string,
    seedMessages?: ChatSeedMessage[],
    mentions?: ChatAttachment[]
  ) =>
    request<ChatResponse>(workspacePath(workspaceId, "/chat"), {
      method: "POST",
      body: JSON.stringify({ message, chat_id: chatId, seed_messages: seedMessages, mentions })
    }),
  chatDetail: (workspaceId: string, chatId: string) =>
    request<ChatDetail>(workspacePath(workspaceId, `/chat/${encodeURIComponent(chatId)}`)),
  chats: (workspaceId: string) => request<ChatSummary[]>(workspacePath(workspaceId, "/chats")),
  charts: (workspaceId: string) => request<ChartSummary[]>(workspacePath(workspaceId, "/charts")),
  deleteChart: (workspaceId: string, id: string) =>
    request<{ status: string }>(workspacePath(workspaceId, `/charts/${encodeURIComponent(id)}`), {
      method: "DELETE"
    }),
  reports: (workspaceId: string) => request<ReportSummary[]>(workspacePath(workspaceId, "/reports")),
  reportFileUrl: (workspaceId: string, reportId: string) =>
    workspacePath(workspaceId, `/reports/${encodeURIComponent(reportId)}/file`),
  reportDownloadUrl: (workspaceId: string, reportId: string) =>
    workspacePath(workspaceId, `/reports/${encodeURIComponent(reportId)}/download`),
  refreshReport: (workspaceId: string, reportId: string) =>
    request<ExecutionSummary>(workspacePath(workspaceId, `/reports/${encodeURIComponent(reportId)}/refresh`), {
      method: "POST"
    }),
  deleteReport: (workspaceId: string, id: string) =>
    request<{ status: string }>(workspacePath(workspaceId, `/reports/${encodeURIComponent(id)}`), {
      method: "DELETE"
    }),
  gitStatus: (workspaceId: string) => request<GitStatus>(workspacePath(workspaceId, "/git/status")),
  commit: (workspaceId: string, message: string) =>
    request<{ output: string }>(workspacePath(workspaceId, "/git/commit"), {
      method: "POST",
      body: JSON.stringify({ message })
    }),
  discardTracked: (workspaceId: string) =>
    request<{
      discarded_tracked: string[];
      discarded_untracked: string[];
      skipped_untracked: string[];
      backup_path: string;
    }>(workspacePath(workspaceId, "/git/discard"), {
      method: "POST",
      body: JSON.stringify({ confirm: true, include_untracked: false, paths: [] })
    }),
  duckQuery: (workspaceId: string, sql: string) =>
    request<{ columns: string[]; rows: Record<string, unknown>[] }>(workspacePath(workspaceId, "/duckdb/query"), {
      method: "POST",
      body: JSON.stringify({ sql })
    })
};
