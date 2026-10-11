import { useNavigate, useRouterState } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Menu } from "@base-ui/react/menu";
import { Toast } from "@base-ui/react/toast";
import { useEffect, useMemo, useRef, useState, type CSSProperties, type DragEvent } from "react";

import { api } from "../api/client";
import type { FileEntry, PlotlyFigure } from "../api/types";
import { AppIcon } from "../components/AppIcon";
import { AppSelect } from "../components/AppSelect";
import { BackIconButton } from "../components/BackButton";
import { ConfirmDeleteDialog } from "../components/ConfirmDeleteDialog";
import { HtmlPreview } from "../components/HtmlPreview";
import { PageLoading } from "../components/PageLoading";
import { PaginatedDataTable } from "../components/PaginatedDataTable";
import { PlotlyChart } from "../components/PlotlyChart";
import { formatArcTime, formatBytes, fileName } from "../utils/format";
import { useWorkspaceId } from "./workspaceContext";

type FileTreeNode = {
  name: string;
  fullPath?: string;
  entry?: FileEntry;
  striped?: boolean;
  children: FileTreeNode[];
};

type TdmsChannelSelection = {
  group_name: string;
  channel_name: string;
};
type DataDestination = "local" | "shared";
type DataRootFilter = "all" | DataDestination;
type DataView = "files" | "integrations";
type FolderDatasetAction = {
  disabled: boolean;
  reason?: string;
};
type DataIntegration = {
  name: string;
  logo: string;
  color: string;
};

const dataRoots = [
  { label: "Local", prefix: "files/local/" },
  { label: "Shared", prefix: "files/shared/" }
] as const;
const supportedUploadExtensions = [
  ".arrow",
  ".csv",
  ".dat",
  ".feather",
  ".h5",
  ".hdf5",
  ".htm",
  ".html",
  ".json",
  ".jsonl",
  ".ndjson",
  ".parquet",
  ".pq",
  ".tdm",
  ".tdms",
  ".tsv",
  ".xls",
  ".xlsx",
  ".xml"
];
const supportedUploadAccept = supportedUploadExtensions.join(",");
const htmlExtensions = new Set([".html", ".htm"]);
const tdmsDatasetExtensions = new Set([".tdms"]);
const tableDatasetExtensions = new Set([".csv", ".tsv"]);
const dataToastManager = Toast.createToastManager();
const dataIntegrations: DataIntegration[] = [
  { name: "OneDrive", logo: "OD", color: "#0078d4" },
  { name: "OneNote", logo: "N", color: "#7719aa" },
  { name: "GitHub", logo: "GH", color: "#24292f" },
  { name: "Bitbucket", logo: "BB", color: "#0052cc" },
  { name: "Confluence", logo: "C", color: "#172b4d" },
  { name: "Jira", logo: "J", color: "#0c66e4" }
];

export function DataPage() {
  const workspaceId = useWorkspaceId();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const uploadInputRef = useRef<HTMLInputElement>(null);
  const requestedPath = useRouterState({
    select: (state) => {
      const search = state.location.search as Record<string, unknown>;
      return typeof search.file === "string" ? search.file : undefined;
    }
  });
  const requestedUpload = useRouterState({
    select: (state) => {
      const search = state.location.search as Record<string, unknown>;
      return search.upload === "1" || search.upload === "true" || search.upload === true;
    }
  });
  const [selectedPath, setSelectedPath] = useState<string>();
  const [showUpload, setShowUpload] = useState(false);
  const [search, setSearch] = useState("");
  const [rootFilter, setRootFilter] = useState<DataRootFilter>("all");
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(100);
  const [deleteFilePath, setDeleteFilePath] = useState<string | undefined>();
  const [uploadError, setUploadError] = useState<string | undefined>();
  const [uploadFiles, setUploadFiles] = useState<File[]>([]);
  const [uploadDestination, setUploadDestination] = useState<DataDestination>("local");
  const [uploadName, setUploadName] = useState("");
  const [dataView, setDataView] = useState<DataView>("files");
  const [selectedTdmsChannel, setSelectedTdmsChannel] = useState<TdmsChannelSelection | undefined>();
  const [collapsedFolders, setCollapsedFolders] = useState<Set<string>>(() => new Set());
  const selectedPathIsHtml = selectedPath ? isHtmlPath(selectedPath) : false;

  const files = useQuery({
    queryKey: ["files", workspaceId],
    queryFn: () => api.files(workspaceId),
    refetchInterval: 4000
  });
  const table = useQuery({
    queryKey: [
      "file-table",
      workspaceId,
      selectedPath,
      selectedTdmsChannel?.group_name,
      selectedTdmsChannel?.channel_name,
      page,
      pageSize
    ],
    queryFn: () => api.fileTable(workspaceId, selectedPath!, page, pageSize, selectedTdmsChannel),
    enabled: Boolean(selectedPath && !selectedPathIsHtml),
    refetchInterval: selectedPath && !selectedPathIsHtml ? 4000 : false
  });
  const upload = useMutation({
    mutationFn: () => api.uploadDataSource(workspaceId, uploadFiles, uploadDestination, uploadName),
    onSuccess: (result) => {
      setSelectedPath(result.path);
      setShowUpload(false);
      setUploadError(undefined);
      setUploadFiles([]);
      setUploadName("");
      setPage(0);
      setSearch("");
      setSelectedTdmsChannel(undefined);
      queryClient.invalidateQueries({ queryKey: ["files", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
      navigate({
        to: "/w/$workspaceId/data",
        params: { workspaceId },
        search: { file: result.path }
      });
    }
  });
  const deleteFile = useMutation({
    mutationFn: (path: string) => api.deleteFile(workspaceId, path),
    onSuccess: () => {
      if (deleteFilePath === selectedPath) {
        setSelectedPath(undefined);
        setSelectedTdmsChannel(undefined);
        setPage(0);
        navigate({
          to: "/w/$workspaceId/data",
          params: { workspaceId },
          search: {},
          replace: true
        });
      }
      setDeleteFilePath(undefined);
      queryClient.invalidateQueries({ queryKey: ["files", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["file-table", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });
  const createDataset = useMutation({
    mutationFn: (path: string) => api.createDataset(workspaceId, path),
    onSuccess: (result) => {
      setSelectedPath(result.path);
      setShowUpload(false);
      setPage(0);
      setSelectedTdmsChannel(undefined);
      queryClient.invalidateQueries({ queryKey: ["files", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["file-table", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
      navigate({
        to: "/w/$workspaceId/data",
        params: { workspaceId },
        search: { file: result.path }
      });
    },
    onError: (error) => {
      dataToastManager.add({
        title: "Dataset was not created",
        description: error instanceof Error ? error.message : "Folder is not a valid dataset.",
        type: "error",
        priority: "high"
      });
    }
  });

  const sourceEntries = useMemo(
    () => (files.data ?? []).filter((entry) => entry.kind === "file" || entry.source_kind === "dataset"),
    [files.data]
  );
  const selectedSource = sourceEntries.find((file) => file.path === selectedPath);
  const deleteTarget = sourceEntries.find((file) => file.path === deleteFilePath);

  useEffect(() => {
    setSelectedPath(undefined);
    setShowUpload(false);
    setSearch("");
    setRootFilter("all");
    setPage(0);
    setDeleteFilePath(undefined);
    setUploadError(undefined);
    setUploadFiles([]);
    setUploadDestination("local");
    setUploadName("");
    setDataView("files");
    setSelectedTdmsChannel(undefined);
    setCollapsedFolders(new Set());
  }, [workspaceId]);

  useEffect(() => {
    if (!requestedPath) return;
    if (sourceEntries.some((file) => file.path === requestedPath)) {
      setDataView("files");
      setSelectedPath(requestedPath);
      setShowUpload(false);
      setPage(0);
      setSearch("");
      setRootFilter("all");
      setSelectedTdmsChannel(undefined);
    }
  }, [sourceEntries, requestedPath]);

  useEffect(() => {
    if (!requestedUpload) return;
    setDataView("files");
    setSelectedPath(undefined);
    setShowUpload(true);
    setPage(0);
    setUploadError(undefined);
    setSelectedTdmsChannel(undefined);
  }, [requestedUpload, workspaceId]);

  const visibleFiles = useMemo(() => {
    const searchTerm = search.trim().toLowerCase();
    return sourceEntries.filter((file) => {
      if (rootFilter !== "all" && !file.path.startsWith(`files/${rootFilter}/`)) return false;
      if (!searchTerm) return true;
      return file.name.toLowerCase().includes(searchTerm) || file.path.toLowerCase().includes(searchTerm);
    });
  }, [rootFilter, sourceEntries, search]);

  const tree = useMemo(() => buildFileTree(visibleFiles, rootFilter), [rootFilter, visibleFiles]);

  function selectFile(path: string) {
    setSelectedPath(path);
    setShowUpload(false);
    setPage(0);
    setSelectedTdmsChannel(undefined);
    navigate({
      to: "/w/$workspaceId/data",
      params: { workspaceId },
      search: { file: path }
    });
  }

  function openUpload() {
    setDataView("files");
    setSelectedPath(undefined);
    setShowUpload(true);
    setPage(0);
    setUploadError(undefined);
    setUploadFiles([]);
    setUploadDestination("local");
    setUploadName("");
    setSelectedTdmsChannel(undefined);
    navigate({
      to: "/w/$workspaceId/data",
      params: { workspaceId },
      search: { upload: "1" }
    });
  }

  function chooseUploadFiles(files?: FileList | File[] | null) {
    const nextFiles = Array.from(files ?? []);
    if (!nextFiles.length) return;
    const unsupported = nextFiles.find((file) => !isSupportedUpload(file.name));
    if (unsupported) {
      setUploadError(`Unsupported file: ${unsupported.name}`);
      return;
    }
    setUploadError(undefined);
    upload.reset();
    setUploadFiles(nextFiles);
    if (!uploadName.trim()) setUploadName(defaultUploadName(nextFiles));
  }

  function createDataSource() {
    if (!uploadFiles.length) {
      setUploadError("Choose at least one data file.");
      return;
    }
    setUploadError(undefined);
    upload.mutate();
  }

  function dropUploadFile(event: DragEvent<HTMLButtonElement>) {
    event.preventDefault();
    chooseUploadFiles(event.dataTransfer.files);
  }

  function toggleFolder(path: string) {
    setCollapsedFolders((current) => {
      const next = new Set(current);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  }

  function createDatasetFromFolder(path: string) {
    createDataset.mutate(path);
  }

  const previewPaneClassName = selectedPath
    ? "data-pane preview-pane has-selection"
    : showUpload
      ? "data-pane preview-pane upload-pane"
      : "data-pane preview-pane";

  return (
    <Toast.Provider toastManager={dataToastManager}>
      <div className="page data-page">
        {deleteTarget ? (
          <ConfirmDeleteDialog
            error={deleteFile.error instanceof Error ? deleteFile.error.message : null}
            isPending={deleteFile.isPending}
            title={`Delete ${deleteTarget.name}?`}
            onCancel={() => setDeleteFilePath(undefined)}
            onConfirm={() => deleteFile.mutate(deleteTarget.path)}
          >
            <div className="delete-copy">
              <p>This deletes only this data source. Assets, runs, workbooks, charts, reports, and outputs are not deleted.</p>
            </div>
          </ConfirmDeleteDialog>
        ) : null}
        <section className="assets-toolbar data-toolbar">
          <div className="assets-titlebar">
            <div className="assets-title-group">
              <h1>Data</h1>
              <div className="assets-tabs" role="tablist" aria-label="Data view">
                <button
                  className={dataView === "files" ? "active" : ""}
                  role="tab"
                  aria-selected={dataView === "files"}
                  onClick={() => setDataView("files")}
                  type="button"
                >
                  File browser
                </button>
                <button
                  className={dataView === "integrations" ? "active" : ""}
                  role="tab"
                  aria-selected={dataView === "integrations"}
                  onClick={() => setDataView("integrations")}
                  type="button"
                >
                  Integrations
                </button>
              </div>
            </div>
            {dataView === "files" ? (
              <button className="button button-primary" onClick={openUpload} type="button">
                <AppIcon name={upload.isPending ? "spinner" : "upload"} />
                Upload
              </button>
            ) : null}
          </div>
          {dataView === "files" ? (
            <div className="assets-controlbar data-controlbar">
              <label className="assets-search">
                <AppIcon name="search" />
                <input
                  placeholder="Search files"
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                />
              </label>
              <div className="assets-sort">
                <span>Source</span>
                <AppSelect
                  ariaLabel="Filter data source"
                  options={[
                    { label: "All", value: "all" },
                    { label: "Local", value: "local" },
                    { label: "Shared", value: "shared" }
                  ]}
                  value={rootFilter}
                  onValueChange={(value) => setRootFilter(value as DataRootFilter)}
                />
              </div>
            </div>
          ) : null}
        </section>
        {dataView === "integrations" ? (
          <section className="data-integrations-page" aria-label="Data integrations">
            <div className="data-integration-list">
              {dataIntegrations.map((integration) => (
                <article className="data-integration-card" key={integration.name}>
                  <div
                    className="data-integration-logo"
                    style={{ "--integration-color": integration.color } as CSSProperties}
                    aria-hidden="true"
                  >
                    {integration.logo}
                  </div>
                  <strong>{integration.name}</strong>
                  <button className="button button-primary" type="button">
                    Connect to {integration.name}
                  </button>
                </article>
              ))}
            </div>
          </section>
        ) : (
          <div className="data-browser">
            <section className="data-pane file-pane source-file-pane">
              <div className="file-tree" role="tree" aria-label="Workspace files">
                <FileTree
                  nodes={tree}
                  selectedPath={selectedPath}
                  deletePendingPath={deleteFile.isPending ? deleteFilePath : undefined}
                  collapsedFolders={collapsedFolders}
                  forceExpanded={Boolean(search.trim())}
                  onDelete={(file) => {
                    deleteFile.reset();
                    setDeleteFilePath(file.path);
                  }}
                  onCreateDataset={createDatasetFromFolder}
                  onSelect={selectFile}
                  onToggleFolder={toggleFolder}
                />
              </div>
            </section>

            <section className={previewPaneClassName}>
          {files.isLoading ? (
            <PageLoading className="pane-loading" label="Loading data" />
          ) : selectedPath ? (
            <div className="pane-title table-title">
              {selectedTdmsChannel ? (
                <BackIconButton
                  className="table-title-back"
                  label="Back to channels"
                  onClick={() => {
                    setSelectedTdmsChannel(undefined);
                    setPage(0);
                  }}
                />
              ) : null}
              <div className="table-title-copy">
                <strong>{selectedTdmsChannel?.channel_name ?? selectedSource?.name ?? fileName(selectedPath)}</strong>
                <span>
                  {selectedTdmsChannel
                    ? `${selectedTdmsChannel.group_name} · Tdms channel`
                    : selectedSource?.source_kind === "dataset"
                      ? `${datasetLabel(selectedSource)} · ${selectedSource.member_count ?? 0} files`
                    : selectedPathIsHtml
                      ? "Html"
                      : table.data?.kind
                      ? dataKindLabel(table.data.kind)
                      : "File"}
                  {selectedSource?.size ? ` · ${formatBytes(selectedSource.size)}` : ""}
                  {selectedSource?.modified_at ? ` · ${formatArcTime(selectedSource.modified_at)}` : ""}
                </span>
              </div>
            </div>
          ) : null}

          {files.isLoading ? null : showUpload ? (
            <div className="data-upload-page">
              <h2>Data wizard</h2>
              <button
                className="data-dropzone"
                disabled={upload.isPending}
                onClick={() => uploadInputRef.current?.click()}
                onDragOver={(event) => event.preventDefault()}
                onDrop={dropUploadFile}
                type="button"
              >
                <AppIcon name={upload.isPending ? "spinner" : "upload"} size={22} />
                <span>
                  {upload.isPending
                    ? "Creating source..."
                    : uploadFiles.length
                      ? `${uploadFiles.length} file${uploadFiles.length === 1 ? "" : "s"} selected`
                      : "Drop one file or a dataset folder's files here"}
                </span>
              </button>
              <input
                ref={uploadInputRef}
                accept={supportedUploadAccept}
                className="data-upload-input"
                multiple
                type="file"
                onChange={(event) => {
                  chooseUploadFiles(event.target.files);
                  event.target.value = "";
                }}
              />
              <div className="data-wizard-controls">
                <div className="data-wizard-field">
                  <span>Destination</span>
                  <div className="segmented-control">
                    <button
                      className={uploadDestination === "local" ? "active" : ""}
                      onClick={() => setUploadDestination("local")}
                      type="button"
                    >
                      Local
                    </button>
                    <button
                      className={uploadDestination === "shared" ? "active" : ""}
                      onClick={() => setUploadDestination("shared")}
                      type="button"
                    >
                      Shared
                    </button>
                  </div>
                </div>
                <label className="data-wizard-field">
                  <span>{uploadFiles.length > 1 ? "Dataset folder" : "File name"}</span>
                  <input
                    value={uploadName}
                    onChange={(event) => setUploadName(event.target.value)}
                    placeholder={uploadFiles.length > 1 ? "brake_run_42" : "sensor_run.tdms"}
                  />
                </label>
              </div>
              {uploadFiles.length ? (
                <div className="data-wizard-review">
                  <div>
                    <strong>{uploadFiles.length > 1 ? "Dataset" : "File"}</strong>
                    <span>
                      {uploadFiles.length > 1
                        ? `${uploadFiles.length} files will be stored as one folder`
                        : uploadFiles[0].name}
                    </span>
                  </div>
                  <button
                    className="button button-primary"
                    disabled={upload.isPending}
                    onClick={createDataSource}
                    type="button"
                  >
                    <AppIcon name={upload.isPending ? "spinner" : "upload"} />
                    Create
                  </button>
                </div>
              ) : null}
              {uploadError ? <p className="inline-error">{uploadError}</p> : null}
              {upload.isError ? <p className="inline-error">{upload.error.message}</p> : null}
            </div>
          ) : !selectedPath ? (
            <div className="empty-preview">
              <AppIcon name="file" size={22} />
              <p>Select a data source to preview.</p>
            </div>
          ) : selectedPathIsHtml ? (
            <HtmlPreview
              className="data-html-preview"
              title={selectedSource?.name ?? fileName(selectedPath)}
              url={api.fileHtmlUrl(workspaceId, selectedPath)}
            />
          ) : table.isError ? (
            <div className="empty-preview">
              <p>Sorry, this file could not be loaded.</p>
            </div>
          ) : table.data?.columns.length ? (
            <div className={isTdmsChannelTable(table.data.kind) ? "file-table-preview with-plot" : "file-table-preview"}>
              {isTdmsChannelTable(table.data.kind) ? <TdmsChannelPlot rows={table.data.rows} /> : null}
              <PaginatedDataTable
                columns={table.data.columns}
                rows={table.data.rows}
                page={page}
                pageSize={pageSize}
                hasNext={table.data.has_next}
                isLoading={table.isLoading}
                onRowClick={
                  table.data.kind === "tdms"
                    || table.data.kind === "tdms_dataset"
                    ? (row) => {
                        const groupName = row.group_name;
                        const channelName = row.channel_name;
                        if (typeof groupName !== "string" || typeof channelName !== "string") return;
                        setSelectedTdmsChannel({ group_name: groupName, channel_name: channelName });
                        setPage(0);
                      }
                    : undefined
                }
                onPageChange={setPage}
                onPageSizeChange={(nextPageSize) => {
                  setPageSize(nextPageSize);
                  setPage(0);
                }}
              />
            </div>
          ) : table.isLoading ? (
            <PageLoading className="pane-loading preview-loading" label="Loading preview" />
          ) : (
            <pre className="text-preview">{table.data?.text ?? "No preview available."}</pre>
          )}
            </section>
          </div>
        )}
      </div>
      <DataToasts />
    </Toast.Provider>
  );
}

function DataToasts() {
  const manager = Toast.useToastManager();
  return (
    <Toast.Portal>
      <Toast.Viewport className="arc-toast-viewport">
        {manager.toasts.map((toast) => (
          <Toast.Root className="arc-toast" key={toast.id} toast={toast}>
            <Toast.Content className="arc-toast-content">
              {toast.title ? <Toast.Title className="arc-toast-title">{toast.title}</Toast.Title> : null}
              {toast.description ? (
                <Toast.Description className="arc-toast-description">{toast.description}</Toast.Description>
              ) : null}
            </Toast.Content>
            <Toast.Close className="button button-icon arc-toast-close" aria-label="Close notification">
              <AppIcon name="cross" />
            </Toast.Close>
          </Toast.Root>
        ))}
      </Toast.Viewport>
    </Toast.Portal>
  );
}

function TdmsChannelPlot({ rows }: { rows: Record<string, unknown>[] }) {
  const figure = useMemo(() => tdmsChannelFigure(rows), [rows]);
  if (!figure) return null;
  return (
    <div className="tdms-channel-plot">
      <PlotlyChart figure={figure} />
    </div>
  );
}

function tdmsChannelFigure(rows: Record<string, unknown>[]): PlotlyFigure | null {
  const xField = tdmsXAxisField(rows);
  const unit = firstString(rows, "unit");
  const x: Array<string | number> = [];
  const y: number[] = [];

  for (const row of rows) {
    const value = numericValue(row.value);
    const xValue = xField ? axisValue(row[xField]) : undefined;
    if (value === undefined || xValue === undefined) continue;
    x.push(xValue);
    y.push(value);
  }

  if (!x.length) return null;

  return {
    data: [
      {
        type: "scatter",
        mode: "lines",
        x,
        y,
        hovertemplate: "%{x}<br>%{y}<extra></extra>"
      }
    ],
    layout: {
      height: 260,
      margin: { l: 56, r: 18, t: 14, b: 44 },
      xaxis: { title: axisTitle(xField), automargin: true },
      yaxis: { title: unit || "Value", automargin: true }
    }
  };
}

function tdmsXAxisField(rows: Record<string, unknown>[]) {
  if (rows.some((row) => axisValue(row.timestamp) !== undefined)) return "timestamp";
  if (rows.some((row) => axisValue(row.elapsed_seconds) !== undefined)) return "elapsed_seconds";
  if (rows.some((row) => axisValue(row.sample_index) !== undefined)) return "sample_index";
  return null;
}

function axisTitle(field: string | null) {
  if (field === "timestamp") return "Timestamp";
  if (field === "elapsed_seconds") return "Elapsed seconds";
  return "Sample index";
}

function firstString(rows: Record<string, unknown>[], field: string) {
  for (const row of rows) {
    const value = row[field];
    if (typeof value === "string" && value.trim()) return value;
  }
  return "";
}

function axisValue(value: unknown) {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim()) return value;
  return undefined;
}

function numericValue(value: unknown) {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value !== "string" || !value.trim()) return undefined;
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : undefined;
}

function isHtmlPath(path: string) {
  const lowerPath = path.toLowerCase();
  return Array.from(htmlExtensions).some((extension) => lowerPath.endsWith(extension));
}

function isTdmsChannelTable(kind: string) {
  return kind === "tdms_channel" || kind === "tdms_dataset_channel";
}

function isSupportedUpload(name: string) {
  const lowerName = name.toLowerCase();
  return supportedUploadExtensions.some((extension) => lowerName.endsWith(extension));
}

function defaultUploadName(files: File[]) {
  if (files.length === 1) return files[0].name;
  let prefix = fileStem(files[0].name);
  files.slice(1).forEach((file) => {
    const stem = fileStem(file.name);
    while (prefix && !stem.startsWith(prefix)) {
      prefix = prefix.slice(0, -1);
    }
  });
  return prefix.replace(/[ _.-]+$/, "") || "dataset";
}

function fileStem(name: string) {
  const index = name.lastIndexOf(".");
  return index > 0 ? name.slice(0, index) : name;
}

function datasetLabel(entry: FileEntry) {
  const kind = entry.dataset_kind ? dataKindLabel(entry.dataset_kind) : "";
  if (entry.status && entry.status !== "ready") {
    return kind ? `${kind} dataset (${entry.status})` : `Dataset (${entry.status})`;
  }
  return kind ? `${kind} dataset` : "Dataset";
}

function dataKindLabel(kind: string) {
  return kind.replace(/[_-]+/g, " ").trim().toLowerCase() || "file";
}

function FileTree({
  nodes,
  selectedPath,
  deletePendingPath,
  collapsedFolders,
  forceExpanded,
  onDelete,
  onCreateDataset,
  onSelect,
  onToggleFolder,
  level = 0
}: {
  nodes: FileTreeNode[];
  selectedPath?: string;
  deletePendingPath?: string;
  collapsedFolders: Set<string>;
  forceExpanded: boolean;
  onDelete: (file: FileEntry) => void;
  onCreateDataset: (path: string) => void;
  onSelect: (path: string) => void;
  onToggleFolder: (path: string) => void;
  level?: number;
}) {
  return (
    <>
      {nodes.map((node) => {
        if (node.entry && node.fullPath) {
          const isDeleting = deletePendingPath === node.fullPath;
          const isDataset = node.entry.source_kind === "dataset";
          const rowClassName = [
            "file-tree-row",
            isDataset ? "dataset" : "file",
            node.striped ? "striped" : "",
            node.fullPath === selectedPath ? "active" : ""
          ]
            .filter(Boolean)
            .join(" ");
          return (
            <div
              className={rowClassName}
              key={node.fullPath}
              role="treeitem"
              aria-selected={node.fullPath === selectedPath}
              style={{ paddingLeft: 12 + level * 14 }}
            >
              <button className="file-tree-row-main" onClick={() => onSelect(node.fullPath!)} type="button">
                <AppIcon name={isDataset ? "data" : "file"} />
                <span>{node.name}</span>
              </button>
              <div className="file-tree-row-trailing">
                <small>
                  {isDataset
                    ? `${datasetLabel(node.entry)} · ${node.entry.member_count ?? 0}`
                    : formatBytes(node.entry.size)}
                </small>
                <button
                  aria-label={`Delete ${node.name}`}
                  className="button button-icon button-danger file-tree-delete"
                  disabled={isDeleting}
                  title={isDataset ? "Delete dataset" : "Delete file"}
                  type="button"
                  onClick={() => onDelete(node.entry!)}
                >
                  <AppIcon name={isDeleting ? "spinner" : "trash"} />
                </button>
              </div>
            </div>
          );
        }

        const folderPath = node.fullPath ?? `${level}-${node.name}`;
        const isCollapsed = !forceExpanded && collapsedFolders.has(folderPath);
        const datasetAction = folderDatasetAction(node, level);
        return (
          <div className="file-tree-group" key={`${level}-${folderPath}`}>
            <div className="file-tree-row folder" style={{ paddingLeft: 12 + level * 14 }}>
              <button
                aria-expanded={!isCollapsed}
                className="file-tree-folder-main"
                onClick={() => onToggleFolder(folderPath)}
                type="button"
              >
                <AppIcon name="folder" />
                <span>{node.name}</span>
              </button>
              {datasetAction ? (
                <Menu.Root>
                  <Menu.Trigger
                    render={
                      <button
                        aria-label={`Actions for ${node.name}`}
                        className="button button-icon file-tree-folder-menu"
                        title="Folder actions"
                        type="button"
                      >
                        <AppIcon name="more" />
                      </button>
                    }
                  />
                  <Menu.Portal>
                    <Menu.Positioner align="end" sideOffset={4}>
                      <Menu.Popup className="file-tree-menu">
                        <Menu.Item
                          className={
                            datasetAction.disabled ? "file-tree-menu-item disabled" : "file-tree-menu-item"
                          }
                          disabled={datasetAction.disabled}
                          onClick={() => {
                            if (!datasetAction.disabled) onCreateDataset(folderPath);
                          }}
                        >
                          <span>Create dataset</span>
                          {datasetAction.reason ? <small>{datasetAction.reason}</small> : null}
                        </Menu.Item>
                      </Menu.Popup>
                    </Menu.Positioner>
                  </Menu.Portal>
                </Menu.Root>
              ) : null}
            </div>
            {isCollapsed ? null : (
              <FileTree
                nodes={node.children}
                selectedPath={selectedPath}
                deletePendingPath={deletePendingPath}
                collapsedFolders={collapsedFolders}
                forceExpanded={forceExpanded}
                onDelete={onDelete}
                onCreateDataset={onCreateDataset}
                onSelect={onSelect}
                onToggleFolder={onToggleFolder}
                level={level + 1}
              />
            )}
          </div>
        );
      })}
    </>
  );
}

function folderDatasetAction(node: FileTreeNode, level: number): FolderDatasetAction | null {
  if (level === 0) return null;
  const immediateFiles = node.children.filter((child) => child.entry?.kind === "file");
  if (!immediateFiles.length) {
    return { disabled: true, reason: "No immediate TDMS or CSV files" };
  }
  const extensions = new Set(immediateFiles.map((child) => extensionForName(child.name)));
  if (setEquals(extensions, tdmsDatasetExtensions)) {
    return { disabled: false };
  }
  if ([...extensions].every((extension) => tableDatasetExtensions.has(extension))) {
    return { disabled: false };
  }
  return { disabled: true, reason: "Use TDMS files or CSV/TSV files" };
}

function extensionForName(name: string) {
  const index = name.lastIndexOf(".");
  return index >= 0 ? name.slice(index).toLowerCase() : "";
}

function setEquals(left: Set<string>, right: Set<string>) {
  if (left.size !== right.size) return false;
  return [...left].every((value) => right.has(value));
}

function buildFileTree(entries: FileEntry[], rootFilter: DataRootFilter = "all") {
  const visibleRoots = dataRoots.filter((dataRoot) => {
    if (rootFilter === "all") return true;
    return dataRoot.prefix === `files/${rootFilter}/`;
  });
  const root: FileTreeNode = {
    name: "root",
    children: visibleRoots.map((dataRoot) => ({ name: dataRoot.label, fullPath: dataRoot.prefix, children: [] }))
  };

  entries.forEach((entry) => {
    const dataRoot = dataRoots.find((candidate) => entry.path.startsWith(candidate.prefix));
    if (!dataRoot) return;
    const group = root.children.find((node) => node.name === dataRoot.label);
    if (!group) return;
    const displayPath = entry.path.slice(dataRoot.prefix.length);
    const parts = displayPath.split("/").filter(Boolean);
    let current = group;
    parts.forEach((part, index) => {
      const isFile = index === parts.length - 1;
      let next = current.children.find((child) => child.name === part && Boolean(child.entry) === isFile);
      if (!next) {
        next = {
          name: part,
          fullPath: isFile ? entry.path : `${dataRoot.prefix}${parts.slice(0, index + 1).join("/")}/`,
          children: []
        };
        current.children.push(next);
      }
      if (isFile) {
        next.fullPath = entry.path;
        next.entry = entry;
      }
      current = next;
    });
  });

  sortTree(root.children);
  stripeFileRows(root.children);
  return root.children;
}

function sortTree(nodes: FileTreeNode[]) {
  nodes.sort((left, right) => {
    if (Boolean(left.entry) !== Boolean(right.entry)) return left.entry ? 1 : -1;
    return left.name.localeCompare(right.name);
  });
  nodes.forEach((node) => sortTree(node.children));
}

function stripeFileRows(nodes: FileTreeNode[], state = { index: 0 }) {
  nodes.forEach((node) => {
    if (node.entry) {
      node.striped = state.index % 2 === 1;
      state.index += 1;
      return;
    }
    stripeFileRows(node.children, state);
  });
}
