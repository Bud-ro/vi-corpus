export type WorkspaceSummary = {
  id: string;
  name: string;
  slug: string;
  root_path: string;
};

export type ProjectSummary = {
  workspace: WorkspaceSummary;
  chat_available: boolean;
  chat_setup_message?: string | null;
  tabs: string[];
};

export type ProjectSettings = {
  name: string;
  agent_system_prompt: string;
};

export type WorkspaceApiTokenStatus = {
  token_prefix?: string | null;
  created_at?: string | null;
  last_used_at?: string | null;
};

export type WorkspaceApiTokenCreateResponse = WorkspaceApiTokenStatus & {
  token: string;
};

export type FileEntry = {
  path: string;
  name: string;
  kind: "file" | "directory";
  size?: number | null;
  modified_at?: string | null;
  source_kind: "file" | "dataset";
  dataset_kind?: string | null;
  status?: string | null;
  member_count?: number | null;
};

export type FilePreview = {
  path: string;
  kind: string;
  columns: string[];
  rows: Record<string, unknown>[];
  text?: string | null;
};

export type FileTablePage = {
  path: string;
  kind: string;
  columns: string[];
  rows: Record<string, unknown>[];
  page: number;
  page_size: number;
  has_next: boolean;
  row_count?: number | null;
  text?: string | null;
};

export type WorkspaceFileRead = {
  path: string;
  name: string;
  language?: string | null;
  size: number;
  modified_at?: string | null;
  text: string;
  truncated: boolean;
};

export type UploadResponse = {
  path: string;
  sha256?: string | null;
  size: number;
  duckdb_table?: string | null;
  kind: "file" | "dataset";
  dataset_kind?: string | null;
  status?: string | null;
  member_count?: number | null;
};

export type ComponentDocLink = {
  label: string;
  url: string;
  kind: string;
};

export type ComponentChannel = {
  id: string;
  label: string;
  unit: string;
};

export type ComponentModelDefinition = {
  id: string;
  name: string;
  vendor: string;
  kind: string;
  description: string;
  default_sample_rate_hz: number;
  channels: ComponentChannel[];
  docs: ComponentDocLink[];
  notes: string;
};

export type ComponentSample = {
  timestamp: string;
  asset_id: string;
  component_model_id: string;
  sequence: number;
  ax_g: number;
  ay_g: number;
  az_g: number;
  temperature_c: number;
  event?: string | null;
};

export type ComponentRecordingStartResponse = {
  id: string;
  asset_id: string;
  component_model_id: string;
  sample_rate_hz: number;
  started_at: string;
  status: "recording";
};

export type ComponentRecordingStopResponse = {
  id: string;
  asset_id: string;
  component_model_id: string;
  sample_rate_hz: number;
  started_at: string;
  stopped_at: string;
  sample_count: number;
  event_count: number;
  file_path: string;
  run_id: string;
};

export type AssetSummary = {
  id: string;
  name: string;
  asset_type: "system" | "component";
  parent_asset_id?: string | null;
  component_model_id?: string | null;
  tags: string[];
  properties: Record<string, string>;
  archived_at?: string | null;
  path?: string | null;
  run_count: number;
  workbook_count: number;
  component_count: number;
};

export type AssetInput = Omit<AssetSummary, "path" | "run_count" | "workbook_count" | "component_count">;

export type TestRunSummary = {
  id: string;
  name: string;
  asset_id: string;
  asset_name?: string | null;
  start_time: string;
  end_time: string;
  notes: string;
  tags: string[];
  properties: Record<string, string>;
  path?: string | null;
  workbook_count: number;
  execution_count: number;
};

export type TestRunInput = Omit<TestRunSummary, "asset_name" | "path" | "workbook_count" | "execution_count">;

export type WorkbookStep = {
  id: string;
  title: string;
  prompt: string;
  input_refs: string[];
  entrypoint: string;
  script?: string | null;
  active: boolean;
};

export type WorkbookTemplateSummary = {
  id: string;
  name: string;
  description: string;
  steps: string[];
  step_files: WorkbookStep[];
  tags: string[];
  properties: Record<string, string>;
  path?: string | null;
  workbook_count: number;
};

export type WorkbookTemplateInput = Omit<WorkbookTemplateSummary, "step_files" | "path" | "workbook_count">;

export type WorkbookDataSource = {
  id: string;
  name: string;
  path: string;
  kind: string;
  notes: string;
};

export type WorkbookSummary = {
  id: string;
  title: string;
  template_id: string;
  template_name?: string | null;
  linked_asset_id: string;
  linked_asset_name?: string | null;
  step_order: string[];
  data_sources: WorkbookDataSource[];
  tags: string[];
  properties: Record<string, string>;
  status: "draft" | "ready" | "computing" | "failed" | "locked" | "archived";
  path?: string | null;
  latest_execution_id?: string | null;
  latest_execution_status?: string | null;
  latest_execution_started_at?: string | null;
  updated_at?: string | null;
};

export type WorkbookInput = Omit<
  WorkbookSummary,
  | "template_name"
  | "linked_asset_name"
  | "path"
  | "latest_execution_id"
  | "latest_execution_status"
  | "latest_execution_started_at"
  | "updated_at"
>;

export type WorkbookDuplicateInput = {
  id?: string | null;
  title?: string | null;
  linked_asset_id?: string | null;
  data_sources?: WorkbookDataSource[] | null;
};

export type WorkbookStepGenerateInput = {
  title: string;
  prompt: string;
  input_refs: string[];
};

export type WorkbookStepReviseInput = {
  instruction: string;
  input_refs: string[];
};

export type WorkbookDetail = {
  workbook: WorkbookSummary;
  template: WorkbookTemplateSummary;
  steps: WorkbookStep[];
  panels: PanelSummary[];
  executions: ExecutionSummary[];
  charts: ChartSummary[];
  reports: ReportSummary[];
  checks: CheckResult[];
};

export type CheckResult = {
  id: string;
  name: string;
  status: "pass" | "warn" | "fail";
  step_id?: string | null;
  severity?: "info" | "warning" | "critical" | null;
  value?: unknown;
  threshold?: unknown;
  unit?: string | null;
  message: string;
  output_path?: string | null;
};

export type PanelSummary = {
  id: string;
  title: string;
  kind: "chart" | "report" | "check";
  step_id?: string | null;
  execution_id?: string | null;
  source_output_path?: string | null;
  status?: string | null;
};

export type ExecutionChecks = {
  execution_id: string;
  checks: CheckResult[];
};

export type ExecutionSummary = {
  id: string;
  workspace_id?: string | null;
  workbook_id: string;
  template_id: string;
  target_type: string;
  target_id: string;
  linked_asset_id?: string | null;
  status: string;
  started_at: string;
  completed_at?: string | null;
  error?: string | null;
  workbook_git_commit?: string | null;
  log_count: number;
  check_counts: Record<string, number>;
};

export type ExecutionLogEntry = {
  seq: number;
  timestamp: string;
  level: string;
  source: "runner" | "stdout" | "stderr";
  message: string;
  step_id?: string | null;
};

export type ExecutionOutput = {
  path: string;
  name: string;
  kind: string;
  size: number;
};

export type ExecutionOutputPreview = {
  path: string;
  kind: string;
  text?: string | null;
  json_value?: unknown;
};

export type ExecutionLogs = {
  execution_id: string;
  entries: ExecutionLogEntry[];
  text: string;
};

export type ChatResponse = {
  chat_id: string;
  assistant_message: string;
  attachments: ChatAttachment[];
  activity: ChatActivityEvent[];
};

export type ChatSeedMessage = {
  role: "user" | "assistant";
  content: string;
};

export type ChatDetail = {
  id: string;
  messages: Message[];
};

export type ChatSummary = {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
};

export type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
  attachments: ChatAttachment[];
  activity: ChatActivityEvent[];
};

export type ChatActivityEvent = {
  label: string;
  status: "ok" | "error";
  detail?: string | null;
  duration_ms?: number | null;
};

export type ChatAttachment = {
  type: "workspace_file";
  path: string;
  title?: string | null;
  language?: string | null;
  label?: string | null;
};

export type ChartSummary = {
  id: string;
  title: string;
  path: string;
  figure: PlotlyFigure;
  renderer: string;
  workbook_id?: string | null;
  step_id?: string | null;
  execution_id?: string | null;
  source_output_path?: string | null;
  updated_at?: string | null;
};

export type PlotlyFigure = {
  data?: unknown[];
  layout?: Record<string, unknown>;
};

export type GitStatus = {
  branch: string;
  porcelain: string[];
  diff: string;
};

export type ReportSummary = {
  id: string;
  title: string;
  path: string;
  format: string;
  workbook_id?: string | null;
  step_id?: string | null;
  execution_id?: string | null;
  source_output_path?: string | null;
  created_at?: string | null;
  chart_ids: string[];
};
