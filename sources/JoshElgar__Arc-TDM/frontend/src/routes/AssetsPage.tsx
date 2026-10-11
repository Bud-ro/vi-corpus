import { Menu } from "@base-ui/react/menu";
import { Link, useNavigate, useParams } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { FormEvent, KeyboardEvent } from "react";
import { useMemo, useState } from "react";

import { api } from "../api/client";
import type {
  AssetInput,
  AssetSummary,
  ComponentModelDefinition,
  TestRunInput,
  TestRunSummary,
  WorkbookSummary
} from "../api/types";
import { AppIcon } from "../components/AppIcon";
import { AppSelect } from "../components/AppSelect";
import { ConfirmDeleteDialog } from "../components/ConfirmDeleteDialog";
import { FormDialog } from "../components/FormDialog";
import { PageLoading } from "../components/PageLoading";
import {
  formatProperties,
  fromLocalInputValue,
  parseCommaList,
  parseProperties,
  slugify,
  toLocalInputValue
} from "../utils/formHelpers";
import { formatArcTime } from "../utils/format";
import { RunForm, type RunDraft } from "./RunsPage";
import { AssetComponentConsole } from "./AssetComponentsSection";
import { useWorkspaceId } from "./workspaceContext";

type AssetDraft = {
  id: string;
  name: string;
  asset_type: "system" | "component";
  parent_asset_id: string;
  component_model_id: string;
  tags: string;
  properties: string;
  archived_at: string | null;
  original_id: string | null;
};

type AssetSort = "recent" | "name" | "runs";
type AssetDetailTab = "overview" | "runs" | "workbooks" | "components";
const maxAssetLabels = 10;

export function AssetsPage() {
  const params = useParams({ strict: false }) as { assetId?: string };
  if (params.assetId) return <AssetDetailPage assetId={params.assetId} />;
  return <AssetListPage />;
}

function AssetListPage() {
  const workspaceId = useWorkspaceId();
  const queryClient = useQueryClient();
  const [editing, setEditing] = useState<AssetDraft | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<AssetSort>("recent");
  const assets = useQuery({ queryKey: ["assets", workspaceId], queryFn: () => api.assets(workspaceId) });
  const componentModels = useQuery({
    queryKey: ["component-models", workspaceId],
    queryFn: () => api.componentModels(workspaceId)
  });
  const runs = useQuery({ queryKey: ["test-runs", workspaceId], queryFn: () => api.runs(workspaceId) });
  const workbooks = useQuery({ queryKey: ["workbooks", workspaceId], queryFn: () => api.workbooks(workspaceId) });
  const assetRows = useMemo(
    () => buildAssetRows(assets.data ?? [], runs.data ?? [], workbooks.data ?? []),
    [assets.data, runs.data, workbooks.data]
  );
  const visibleAssets = useMemo(() => {
    const query = search.trim().toLowerCase();
    return assetRows
      .filter((row) => {
        if (!query) return true;
        return [
          row.asset.name,
          row.asset.id,
          row.asset.tags.join(" "),
          Object.values(row.asset.properties).join(" "),
        ].some((value) => value.toLowerCase().includes(query));
      })
      .sort((a, b) => compareAssetRows(a, b, sort));
  }, [assetRows, search, sort]);
  const metrics = useMemo(() => {
    const activeAssets = assetRows.filter((row) => !row.asset.archived_at);
    const assetsWithoutRuns = activeAssets.filter((row) => row.runs.length === 0);
    const recentRunCount = (runs.data ?? []).filter((run) => isRecent(run.start_time)).length;
    return [
      { label: "Total assets", value: assetRows.length.toString(), detail: `${activeAssets.length} active` },
      { label: "Recent runs", value: recentRunCount.toString(), detail: "last 7 days" },
      { label: "No runs yet", value: assetsWithoutRuns.length.toString(), detail: "active assets" }
    ];
  }, [assetRows, runs.data]);
  const saveAsset = useMutation({
    mutationFn: (asset: AssetInput) => api.saveAsset(workspaceId, asset),
    onSuccess: (asset) => {
      setEditing(null);
      setFormError(null);
      queryClient.invalidateQueries({ queryKey: ["assets", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["test-runs", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });

  function startNewAsset() {
    setFormError(null);
    setEditing({
      id: "",
      name: "",
      asset_type: "system",
      parent_asset_id: "",
      component_model_id: "",
      tags: "",
      properties: "",
      archived_at: null,
      original_id: null
    });
  }

  function submitAsset(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!editing) return;
    try {
      const name = editing.name.trim();
      const id = slugify(editing.id || name);
      if (!id || !name) throw new Error("Asset needs a name.");
      saveAsset.mutate({
        id,
        name,
        asset_type: editing.asset_type,
        parent_asset_id: editing.asset_type === "component" ? editing.parent_asset_id || null : null,
        component_model_id: editing.asset_type === "component" ? editing.component_model_id || null : null,
        tags: parseAssetLabels(editing.tags),
        properties: parseProperties(editing.properties),
        archived_at: editing.archived_at
      });
    } catch (error) {
      setFormError(error instanceof Error ? error.message : "Asset could not be saved.");
    }
  }

  if (assets.isLoading || runs.isLoading || workbooks.isLoading || componentModels.isLoading) {
    return <PageLoading label="Loading assets" />;
  }

  return (
    <div className="page assets-page">
      <section className="assets-toolbar">
        <div className="assets-titlebar">
          <div className="assets-title-group">
            <h1>Assets</h1>
          </div>
          <button className="button button-primary" onClick={startNewAsset} type="button">
            <AppIcon name="plus" />
            New Asset
          </button>
        </div>
        <div className="assets-controlbar">
          <label className="assets-search">
            <AppIcon name="search" />
            <input
              placeholder="Search assets"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </label>
          <div className="assets-sort">
            <span>Sort</span>
            <AppSelect
              ariaLabel="Sort assets"
              options={[
                { label: "Recent run", value: "recent" },
                { label: "Name", value: "name" },
                { label: "Run count", value: "runs" }
              ]}
              value={sort}
              onValueChange={(value) => setSort(value as AssetSort)}
            />
          </div>
        </div>
      </section>

      <section className="asset-metric-grid" aria-label="Asset summary">
        {metrics.map((metric) => (
          <div className="asset-metric-tile" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
            <small>{metric.detail}</small>
          </div>
        ))}
      </section>

      {editing ? (
        <FormDialog title={editing.original_id ? "Edit asset" : "New asset"} onClose={() => setEditing(null)}>
          <AssetForm
            draft={editing}
            assets={assets.data ?? []}
            componentModels={componentModels.data ?? []}
            error={formError || (saveAsset.error instanceof Error ? saveAsset.error.message : null)}
            pending={saveAsset.isPending}
            onCancel={() => setEditing(null)}
            onChange={(patch) => setEditing((current) => current ? { ...current, ...patch } : current)}
            onSubmit={submitAsset}
          />
        </FormDialog>
      ) : null}

      <section className="asset-tile-grid" aria-label="Assets">
        {visibleAssets.map((row) => (
          <Link
            className={assetTileClass(row)}
            key={row.asset.id}
            params={{ workspaceId, assetId: row.asset.id }}
            to="/w/$workspaceId/assets/$assetId"
          >
            <div className="asset-tile-header">
              <div>
                <span className="asset-icon">
                  <AppIcon name="dashboard" />
                </span>
                <h2>{row.asset.name}</h2>
              </div>
              <span className={row.asset.archived_at ? "asset-status archived" : "asset-status active"}>
                {row.asset.asset_type === "component" ? "Component" : "System"}
              </span>
            </div>
            <div className="asset-chip-row">
              <span>#{row.asset.id}</span>
              <span>{row.lastRun ? formatArcTime(row.lastRun.start_time) : "No runs"}</span>
              <span>{row.runs.length} runs</span>
              <span>{row.workbooks.length} workbooks</span>
              {row.asset.asset_type === "system" ? <span>{row.asset.component_count} components</span> : null}
            </div>
          </Link>
        ))}
        {!visibleAssets.length ? (
          <button className="asset-empty-card" onClick={startNewAsset} type="button">
            <AppIcon name="plus" size={22} />
            <strong>Create new asset</strong>
            <span>Add a headset, prototype, rig, vehicle, engine, or other physical thing.</span>
          </button>
        ) : null}
      </section>
    </div>
  );
}

function AssetDetailPage({ assetId }: { assetId: string }) {
  const workspaceId = useWorkspaceId();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [editing, setEditing] = useState<AssetDraft | null>(null);
  const [editingRun, setEditingRun] = useState<RunDraft | null>(null);
  const [selectedRunId, setSelectedRunId] = useState<string | null>(null);
  const [confirmDeleteOpen, setConfirmDeleteOpen] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [runFormError, setRunFormError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<AssetDetailTab | null>(null);
  const asset = useQuery({ queryKey: ["asset", workspaceId, assetId], queryFn: () => api.asset(workspaceId, assetId) });
  const assets = useQuery({ queryKey: ["assets", workspaceId], queryFn: () => api.assets(workspaceId) });
  const componentModels = useQuery({
    queryKey: ["component-models", workspaceId],
    queryFn: () => api.componentModels(workspaceId)
  });
  const runs = useQuery({ queryKey: ["test-runs", workspaceId, assetId], queryFn: () => api.runs(workspaceId, assetId) });
  const workbooks = useQuery({ queryKey: ["workbooks", workspaceId], queryFn: () => api.workbooks(workspaceId) });
  const templates = useQuery({ queryKey: ["workbook-templates", workspaceId], queryFn: () => api.workbookTemplates(workspaceId) });
  const linkedWorkbooks = useMemo(
    () => linkAssetWorkbooks(assetId, runs.data ?? [], workbooks.data ?? []),
    [assetId, runs.data, workbooks.data]
  );
  const runRows = useMemo(
    () => [...(runs.data ?? [])].sort((a, b) => dateValue(b.start_time) - dateValue(a.start_time)),
    [runs.data]
  );
  const saveAsset = useMutation({
    mutationFn: (draft: AssetInput) => api.saveAsset(workspaceId, draft),
    onSuccess: (savedAsset) => {
      setEditing(null);
      setFormError(null);
      queryClient.invalidateQueries({ queryKey: ["asset", workspaceId, assetId] });
      queryClient.invalidateQueries({ queryKey: ["asset", workspaceId, savedAsset.id] });
      queryClient.invalidateQueries({ queryKey: ["assets", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["test-runs", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });
  const saveRun = useMutation({
    mutationFn: (run: TestRunInput) => api.saveRun(workspaceId, run),
    onSuccess: () => {
      setEditingRun(null);
      setRunFormError(null);
      queryClient.invalidateQueries({ queryKey: ["asset", workspaceId, assetId] });
      queryClient.invalidateQueries({ queryKey: ["assets", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["test-runs", workspaceId, assetId] });
      queryClient.invalidateQueries({ queryKey: ["test-runs", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });
  const saveWorkbook = useMutation({
    mutationFn: (workbook: {
      id: string;
      title: string;
      template_id: string;
      linked_asset_id: string;
      step_order: string[];
      data_sources: [];
      tags: string[];
      properties: Record<string, string>;
      status: "ready";
    }) => api.saveWorkbook(workspaceId, workbook),
    onSuccess: (workbook) => {
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["asset", workspaceId, assetId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
      navigate({ to: "/w/$workspaceId/workbooks/$workbookId", params: { workspaceId, workbookId: workbook.id } });
    }
  });
  const deleteAsset = useMutation({
    mutationFn: () => api.deleteAsset(workspaceId, assetId),
    onSuccess: () => {
      setConfirmDeleteOpen(false);
      queryClient.invalidateQueries({ queryKey: ["assets", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["asset", workspaceId, assetId] });
      queryClient.invalidateQueries({ queryKey: ["test-runs", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
      navigate({ to: "/w/$workspaceId", params: { workspaceId } });
    }
  });

  function startEditAsset() {
    if (!asset.data) return;
    setFormError(null);
    setEditing({
      id: asset.data.id,
      name: asset.data.name,
      asset_type: asset.data.asset_type,
      parent_asset_id: asset.data.parent_asset_id ?? "",
      component_model_id: asset.data.component_model_id ?? "",
      tags: asset.data.tags.join(", "),
      properties: formatProperties(asset.data.properties),
      archived_at: asset.data.archived_at ?? null,
      original_id: asset.data.id
    });
  }

  function startNewComponent() {
    setFormError(null);
    setEditing({
      id: "",
      name: "",
      asset_type: "component",
      parent_asset_id: assetId,
      component_model_id: "",
      tags: "",
      properties: "",
      archived_at: null,
      original_id: null
    });
  }

  function startNewRun() {
    const now = new Date();
    const later = new Date(now.getTime() + 60 * 60_000);
    setRunFormError(null);
    setEditingRun({
      id: "",
      name: "",
      assetId,
      startTime: toLocalInputValue(now.toISOString()),
      endTime: toLocalInputValue(later.toISOString()),
      notes: ""
    });
  }

  function startEditRun(run: TestRunSummary) {
    setRunFormError(null);
    setEditingRun({
      id: run.id,
      name: run.name,
      assetId: run.asset_id,
      startTime: toLocalInputValue(run.start_time),
      endTime: toLocalInputValue(run.end_time),
      notes: run.notes
    });
  }

  function submitRun(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!editingRun) return;
    try {
      const name = editingRun.name.trim();
      const id = slugify(editingRun.id || name);
      if (!id || !name) throw new Error("Run needs a name.");
      saveRun.mutate({
        id,
        name,
        asset_id: assetId,
        start_time: fromLocalInputValue(editingRun.startTime),
        end_time: fromLocalInputValue(editingRun.endTime),
        notes: editingRun.notes.trim(),
        tags: [],
        properties: {}
      });
    } catch (error) {
      setRunFormError(error instanceof Error ? error.message : "Run could not be saved.");
    }
  }

  function submitAsset(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!editing) return;
    try {
      const name = editing.name.trim();
      const id = slugify(editing.id || name);
      if (!id || !name) throw new Error("Asset needs a name.");
      saveAsset.mutate({
        id,
        name,
        asset_type: editing.asset_type,
        parent_asset_id: editing.asset_type === "component" ? editing.parent_asset_id || null : null,
        component_model_id: editing.asset_type === "component" ? editing.component_model_id || null : null,
        tags: parseAssetLabels(editing.tags),
        properties: parseProperties(editing.properties),
        archived_at: editing.archived_at
      });
    } catch (error) {
      setFormError(error instanceof Error ? error.message : "Asset could not be saved.");
    }
  }

  function createWorkbook(assetId: string, assetName: string) {
    const template = (templates.data ?? [])[0];
    if (!template) return;
    const title = `${assetName} Workbook`;
    saveWorkbook.mutate({
      id: slugify(title),
      title,
      template_id: template.id,
      linked_asset_id: assetId,
      step_order: [],
      data_sources: [],
      tags: [],
      properties: {},
      status: "ready"
    });
  }

  if (
    asset.isLoading ||
    assets.isLoading ||
    componentModels.isLoading ||
    runs.isLoading ||
    workbooks.isLoading ||
    templates.isLoading
  ) {
    return <PageLoading label="Loading asset" />;
  }

  if (!asset.data) {
    return (
      <div className="page assets-page workbook-detail-page asset-detail-page">
        <section className="workbook-detail-header">
          <div className="asset-breadcrumbs">
            <Link params={{ workspaceId }} to="/w/$workspaceId/assets">Assets</Link>
          </div>
          <p className="empty-state">Asset not found.</p>
        </section>
      </div>
    );
  }

  const lastRun = runRows[0] ?? null;
  const selectedRun = runRows.find((run) => run.id === selectedRunId) ?? null;
  const selectedTab = activeTab ?? (asset.data.asset_type === "component" ? "components" : "overview");
  const linkedComponents = (assets.data ?? []).filter(
    (candidate) => candidate.asset_type === "component" && candidate.parent_asset_id === assetId
  );
  const componentModel = componentModels.data?.find(
    (candidate) => candidate.id === asset.data.component_model_id
  ) ?? null;

  return (
    <div className="page assets-page workbook-detail-page asset-detail-page">
      <section className="workbook-detail-header asset-detail-header">
        <div className="workbook-detail-title">
          <div>
            <div className="asset-breadcrumbs">
              <Link params={{ workspaceId }} to="/w/$workspaceId/assets">Assets</Link>
              <span>/</span>
              <span>{asset.data.name}</span>
            </div>
          </div>
        </div>
        <div className="button-row">
          <button className="button" onClick={startNewRun} type="button">
            <AppIcon name="plus" />
            New Run
          </button>
          <button
            className="button"
            disabled={!templates.data?.length || saveWorkbook.isPending}
            onClick={() => createWorkbook(asset.data.id, asset.data.name)}
            type="button"
          >
            <AppIcon name={saveWorkbook.isPending ? "spinner" : "plus"} />
            New Workbook
          </button>
          <button className="button button-primary" onClick={startEditAsset} type="button">
            Edit Asset
          </button>
          <AssetActionsMenu
            assetName={asset.data.name}
            onDelete={() => setConfirmDeleteOpen(true)}
          />
        </div>
      </section>

      <AssetDetailTabs
        activeTab={selectedTab}
        componentCount={asset.data.asset_type === "system" ? linkedComponents.length : undefined}
        onChange={setActiveTab}
      />

      {selectedTab === "overview" ? (
        <div className="asset-detail-tab-panel">
          <section className="asset-metric-grid asset-detail-summary" aria-label="Asset summary">
            <div className="asset-metric-tile">
              <span>Type</span>
              <strong>{asset.data.asset_type === "component" ? "Component" : "System"}</strong>
              <small>#{asset.data.id}</small>
            </div>
            <div className="asset-metric-tile">
              <span>Last run</span>
              <strong>{lastRun ? formatArcTime(lastRun.start_time) : "-"}</strong>
              <small>{lastRun?.name ?? "No runs yet"}</small>
            </div>
            <div className="asset-metric-tile">
              <span>Workbooks</span>
              <strong>{linkedWorkbooks.length}</strong>
              <small>linked to this asset</small>
            </div>
            {asset.data.asset_type === "system" ? (
              <div className="asset-metric-tile">
                <span>Components</span>
                <strong>{linkedComponents.length}</strong>
                <small>assigned to this system</small>
              </div>
            ) : null}
          </section>
          <AssetProperties asset={asset.data} assets={assets.data ?? []} componentModel={componentModel} />
        </div>
      ) : null}

      {editing ? (
        <FormDialog title="Edit asset" onClose={() => setEditing(null)}>
          <AssetForm
            draft={editing}
            assets={assets.data ?? []}
            componentModels={componentModels.data ?? []}
            error={formError || (saveAsset.error instanceof Error ? saveAsset.error.message : null)}
            pending={saveAsset.isPending}
            onCancel={() => setEditing(null)}
            onChange={(patch) => setEditing((current) => current ? { ...current, ...patch } : current)}
            onSubmit={submitAsset}
          />
        </FormDialog>
      ) : null}

      {editingRun ? (
        <FormDialog title={editingRun.id ? "Edit run" : "New run"} onClose={() => setEditingRun(null)}>
          <RunForm
            assets={[{ id: asset.data.id, name: asset.data.name }]}
            draft={editingRun}
            error={runFormError || (saveRun.error instanceof Error ? saveRun.error.message : null)}
            pending={saveRun.isPending}
            onCancel={() => setEditingRun(null)}
            onChange={(patch) => setEditingRun((current) => current ? { ...current, ...patch } : current)}
            onSubmit={submitRun}
          />
        </FormDialog>
      ) : null}

      {selectedRun ? (
        <RunDetailDialog
          run={selectedRun}
          onClose={() => setSelectedRunId(null)}
          onEdit={() => {
            setSelectedRunId(null);
            startEditRun(selectedRun);
          }}
        />
      ) : null}

      {confirmDeleteOpen ? (
        <ConfirmDeleteDialog
          title={`Delete ${asset.data.name}?`}
          error={deleteAsset.error instanceof Error ? deleteAsset.error.message : null}
          isPending={deleteAsset.isPending}
          onCancel={() => setConfirmDeleteOpen(false)}
          onConfirm={() => deleteAsset.mutate()}
        >
          <p>This deletes the asset record.</p>
        </ConfirmDeleteDialog>
      ) : null}

      {selectedTab === "runs" ? <section className="asset-detail-section">
        <div className="asset-detail-section-heading">
          <h2>Runs</h2>
        </div>
        <div className="asset-tile-grid asset-detail-grid">
          {runRows.map((run) => (
            <button
              className={
                [
                  "asset-tile run-tile",
                  selectedRun?.id === run.id ? "active" : ""
                ].filter(Boolean).join(" ")
              }
              key={run.id}
              onClick={() => setSelectedRunId(run.id)}
              type="button"
            >
              <div className="asset-tile-header">
                <div>
                  <span className="asset-icon">
                    <AppIcon name="clock" />
                  </span>
                  <h2>{run.name}</h2>
                </div>
              </div>
              <div className="asset-card-meta">
                <span>{formatArcTime(run.start_time)}</span>
                <span>#{run.id}</span>
              </div>
              <div className="asset-chip-row asset-card-chip-row">
                <span>{formatCount(run.workbook_count, "workbook")}</span>
                <span>{formatCount(run.execution_count, "execution")}</span>
              </div>
            </button>
          ))}
          {!runRows.length ? (
            <div className="asset-empty-card is-static">
              <AppIcon name="clock" size={22} />
              <strong>No runs yet</strong>
              <span>Add a run when this asset has a real-world test session.</span>
            </div>
          ) : null}
        </div>
      </section> : null}

      {selectedTab === "workbooks" ? <section className="asset-detail-section">
        <div className="asset-detail-section-heading">
          <h2>Workbooks</h2>
        </div>
        <div className="asset-tile-grid asset-detail-grid">
          {linkedWorkbooks.map((workbook) => (
            <Link
              className="asset-tile workbook-tile"
              key={workbook.id}
              params={{ workspaceId, workbookId: workbook.id }}
              to="/w/$workspaceId/workbooks/$workbookId"
            >
              <div className="asset-tile-header">
                <div>
                  <span className="asset-icon">
                    <AppIcon name="steps" />
                  </span>
                  <h2>{workbook.title}</h2>
                </div>
                <span className="asset-status">asset</span>
              </div>
              <div className="asset-card-meta">
                <span>{workbook.linked_asset_name ?? workbook.linked_asset_id}</span>
                <span>{workbook.latest_execution_started_at ? formatArcTime(workbook.latest_execution_started_at) : "Not run yet"}</span>
              </div>
              <div className="asset-chip-row asset-card-chip-row">
                <span>#{workbook.id}</span>
                <span>{formatCount(workbook.step_order.length, "step")}</span>
              </div>
            </Link>
          ))}
          {!linkedWorkbooks.length ? (
            <div className="asset-empty-card is-static">
              <AppIcon name="steps" size={22} />
              <strong>No workbooks yet</strong>
              <span>Create a workbook for this asset.</span>
            </div>
          ) : null}
        </div>
      </section> : null}

      {selectedTab === "components" ? (
        <section className="asset-detail-components">
          {asset.data.asset_type === "system" ? (
            <>
              <div className="asset-detail-section-heading">
                <h2>Components</h2>
                <button className="button button-primary" onClick={startNewComponent} type="button">
                  <AppIcon name="plus" />
                  New Component
                </button>
              </div>
              <div className="asset-tile-grid asset-detail-grid">
                {linkedComponents.map((component) => (
                  <Link
                    className="asset-tile"
                    key={component.id}
                    params={{ workspaceId, assetId: component.id }}
                    to="/w/$workspaceId/assets/$assetId"
                  >
                    <div className="asset-tile-header">
                      <div>
                        <span className="asset-icon"><AppIcon name="dashboard" /></span>
                        <h2>{component.name}</h2>
                      </div>
                      <span className="asset-status">Component</span>
                    </div>
                    <div className="asset-card-meta">
                      <span>{componentModelName(component, componentModels.data ?? [])}</span>
                      <span>#{component.id}</span>
                    </div>
                    <div className="asset-chip-row asset-card-chip-row">
                      <span>{formatCount(component.run_count, "run")}</span>
                      <span>{formatCount(component.workbook_count, "workbook")}</span>
                    </div>
                  </Link>
                ))}
                {!linkedComponents.length ? (
                  <button className="asset-empty-card" onClick={startNewComponent} type="button">
                    <AppIcon name="plus" size={22} />
                    <strong>Add a component</strong>
                    <span>Assign a sensor, board, or other physical part to this system.</span>
                  </button>
                ) : null}
              </div>
            </>
          ) : componentModel ? (
            <AssetComponentConsole assetId={asset.data.id} componentModel={componentModel} />
          ) : (
            <div className="empty-state">Choose a supported model in Edit Asset to enable live component tools.</div>
          )}
        </section>
      ) : null}
    </div>
  );
}

function AssetActionsMenu({ assetName, onDelete }: { assetName: string; onDelete: () => void }) {
  return (
    <Menu.Root>
      <Menu.Trigger
        render={
          <button
            aria-label={`Actions for ${assetName}`}
            className="button button-icon asset-actions-menu-trigger"
            title="Asset actions"
            type="button"
          >
            <AppIcon name="more" />
          </button>
        }
      />
      <Menu.Portal>
        <Menu.Positioner align="end" sideOffset={4}>
          <Menu.Popup className="file-tree-menu asset-actions-menu">
            <Menu.Item className="file-tree-menu-item asset-actions-delete" onClick={onDelete}>
              <AppIcon name="trash" />
              <span>Delete Asset</span>
            </Menu.Item>
          </Menu.Popup>
        </Menu.Positioner>
      </Menu.Portal>
    </Menu.Root>
  );
}

function RunDetailDialog({
  run,
  onClose,
  onEdit
}: {
  run: TestRunSummary;
  onClose: () => void;
  onEdit: () => void;
}) {
  return (
    <FormDialog title={run.name} onClose={onClose}>
      <div className="run-detail-dialog">
        <div className="run-detail-grid">
          <AssetField label="Start" value={formatArcTime(run.start_time)} />
          <AssetField label="End" value={formatArcTime(run.end_time)} />
          <AssetField label="Notes" value={run.notes.trim() || "-"} />
        </div>
        <div className="button-row">
          <button className="button button-primary" onClick={onEdit} type="button">
            <AppIcon name="edit" />
            Edit Run
          </button>
          <button className="button" onClick={onClose} type="button">Close</button>
        </div>
      </div>
    </FormDialog>
  );
}

function AssetDetailTabs({
  activeTab,
  componentCount,
  onChange
}: {
  activeTab: AssetDetailTab;
  componentCount?: number;
  onChange: (tab: AssetDetailTab) => void;
}) {
  const tabs: Array<{ id: AssetDetailTab; label: string }> = [
    { id: "overview", label: "Overview" },
    { id: "runs", label: "Runs" },
    { id: "workbooks", label: "Workbooks" },
    { id: "components", label: componentCount === undefined ? "Components" : `Components ${componentCount}` }
  ];
  return (
    <div className="workbook-detail-tabs" role="tablist" aria-label="Asset sections">
      {tabs.map((tab) => (
        <button
          aria-selected={activeTab === tab.id}
          className={activeTab === tab.id ? "active" : undefined}
          key={tab.id}
          onClick={() => onChange(tab.id)}
          role="tab"
          type="button"
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

function AssetProperties({
  asset,
  assets,
  componentModel
}: {
  asset: AssetSummary;
  assets: AssetSummary[];
  componentModel: ComponentModelDefinition | null;
}) {
  const parent = assets.find((candidate) => candidate.id === asset.parent_asset_id);
  const fields = [
    asset.asset_type === "component" ? ["System", parent?.name ?? "Unassigned"] : null,
    asset.asset_type === "component" ? ["Model", componentModel?.name ?? "None"] : null,
    ...Object.entries(asset.properties)
  ].filter((field): field is string[] => Boolean(field));
  if (!fields.length) return null;
  return (
    <section className="asset-detail-section">
      <div className="asset-detail-section-heading"><h2>Properties</h2></div>
      <div className="asset-properties-grid">
        {fields.map(([label, value]) => <AssetField key={label} label={label} value={value} />)}
      </div>
    </section>
  );
}

function AssetForm({
  draft,
  assets,
  componentModels,
  error,
  pending,
  onCancel,
  onChange,
  onSubmit
}: {
  draft: AssetDraft;
  assets: AssetSummary[];
  componentModels: ComponentModelDefinition[];
  error?: string | null;
  pending: boolean;
  onCancel: () => void;
  onChange: (patch: Partial<AssetDraft>) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <form className="asset-form" onSubmit={onSubmit}>
      <div className="asset-form-header">
        <div>
          <h2>{draft.original_id ? "Edit asset" : "New asset"}</h2>
          <p>Create the physical thing that runs belong to.</p>
        </div>
      </div>
      <div className="asset-form-grid">
        <label className="settings-field">
          <span>Type</span>
          <AppSelect
            ariaLabel="Asset type"
            options={[
              { label: "System", value: "system" },
              { label: "Component", value: "component" }
            ]}
            value={draft.asset_type}
            onValueChange={(value) => onChange({
              asset_type: value as AssetDraft["asset_type"],
              parent_asset_id: value === "component" ? draft.parent_asset_id : "",
              component_model_id: value === "component" ? draft.component_model_id : ""
            })}
          />
        </label>
        <label className="settings-field">
          <span>Name</span>
          <input value={draft.name} onChange={(event) => onChange({ name: event.target.value })} />
        </label>
        {draft.asset_type === "component" ? (
          <>
            <label className="settings-field">
              <span>System</span>
              <AppSelect
                ariaLabel="Parent system"
                options={[
                  { label: "Unassigned", value: "" },
                  ...assets
                    .filter((asset) => asset.asset_type === "system" && asset.id !== draft.original_id)
                    .map((asset) => ({ label: asset.name, value: asset.id }))
                ]}
                value={draft.parent_asset_id}
                onValueChange={(value) => onChange({ parent_asset_id: value })}
              />
            </label>
            <label className="settings-field">
              <span>Supported model</span>
              <AppSelect
                ariaLabel="Supported component model"
                options={[
                  { label: "None", value: "" },
                  ...componentModels.map((model) => ({ label: model.name, value: model.id }))
                ]}
                value={draft.component_model_id}
                onValueChange={(value) => onChange({ component_model_id: value })}
              />
            </label>
          </>
        ) : null}
        <AssetLabelEditor value={draft.tags} onChange={(tags) => onChange({ tags })} />
        <label className="settings-field form-span-full">
          <span>Properties JSON</span>
          <textarea
            className="settings-prompt small"
            placeholder='{"serial_number":"A014"}'
            value={draft.properties}
            onChange={(event) => onChange({ properties: event.target.value })}
          />
        </label>
        <div className="button-row form-span-full">
          <button className="button-primary" disabled={pending} type="submit">
            <AppIcon name={pending ? "spinner" : "save"} />
            Save asset
          </button>
          <button disabled={pending} onClick={onCancel} type="button">
            Cancel
          </button>
          {error ? <span className="muted">{error}</span> : null}
        </div>
      </div>
    </form>
  );
}

function AssetLabelEditor({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  const labels = cleanAssetLabels(value).slice(0, maxAssetLabels);
  const [pending, setPending] = useState("");
  const canAdd = labels.length < maxAssetLabels;

  function setLabels(nextLabels: string[]) {
    onChange(nextLabels.join(", "));
  }

  function addLabels(raw: string) {
    const incoming = parseCommaList(raw)
      .map((label) => label.trim().toLowerCase())
      .filter(Boolean);
    if (!incoming.length) return;
    const next = [...labels];
    for (const label of incoming) {
      if (next.includes(label) || next.length >= maxAssetLabels) continue;
      next.push(label);
    }
    setLabels(next);
    setPending("");
  }

  function removeLabel(label: string) {
    setLabels(labels.filter((item) => item !== label));
  }

  function handleKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === "Enter" || event.key === ",") {
      event.preventDefault();
      addLabels(pending);
      return;
    }
    if (event.key === "Backspace" && !pending && labels.length) {
      removeLabel(labels[labels.length - 1]);
    }
  }

  return (
    <div className="settings-field form-span-full asset-label-field">
      <span>Labels</span>
      <div className="asset-label-editor">
        {labels.map((label) => (
          <button className="asset-label-chip" key={label} onClick={() => removeLabel(label)} type="button">
            {label}
            <AppIcon name="cross" size={12} />
          </button>
        ))}
        <input
          disabled={!canAdd}
          placeholder={canAdd ? "Add label" : "10 label maximum"}
          value={pending}
          onBlur={() => addLabels(pending)}
          onChange={(event) => setPending(event.target.value)}
          onKeyDown={handleKeyDown}
          onPaste={(event) => {
            const pasted = event.clipboardData.getData("text");
            if (!pasted.includes(",")) return;
            event.preventDefault();
            addLabels(pasted);
          }}
        />
        <button className="button button-table" disabled={!canAdd || !pending.trim()} onClick={() => addLabels(pending)} type="button">
          Add
        </button>
      </div>
      <small>{labels.length}/{maxAssetLabels} labels</small>
    </div>
  );
}

function AssetField({ label, value }: { label: string; value: string }) {
  return (
    <p>
      <span>{label}</span>
      <strong>{value}</strong>
    </p>
  );
}

type AssetRow = {
  asset: AssetSummary;
  runs: TestRunSummary[];
  workbooks: WorkbookSummary[];
  lastRun: TestRunSummary | null;
};

function buildAssetRows(
  assets: AssetSummary[],
  runs: TestRunSummary[],
  workbooks: WorkbookSummary[]
): AssetRow[] {
  return assets.map((asset) => {
    const assetRuns = runs.filter((run) => run.asset_id === asset.id);
    const linkedWorkbooks = workbooks.filter((workbook) => workbookLinkedAssetId(workbook) === asset.id);
    const lastRun = [...assetRuns].sort((a, b) => dateValue(b.start_time) - dateValue(a.start_time))[0] ?? null;
    return { asset, runs: assetRuns, workbooks: linkedWorkbooks, lastRun };
  });
}

function linkAssetWorkbooks(
  assetId: string,
  _runs: TestRunSummary[],
  workbooks: WorkbookSummary[]
): WorkbookSummary[] {
  return workbooks
    .filter((workbook) => workbookLinkedAssetId(workbook) === assetId)
    .sort((a, b) => dateValue(b.updated_at) - dateValue(a.updated_at) || a.title.localeCompare(b.title));
}

function workbookLinkedAssetId(workbook: WorkbookSummary): string | null {
  return workbook.linked_asset_id ?? null;
}

function compareAssetRows(a: AssetRow, b: AssetRow, sort: AssetSort): number {
  if (sort === "name") return a.asset.name.localeCompare(b.asset.name);
  if (sort === "runs") return b.runs.length - a.runs.length || a.asset.name.localeCompare(b.asset.name);
  return dateValue(b.lastRun?.start_time) - dateValue(a.lastRun?.start_time) || a.asset.name.localeCompare(b.asset.name);
}

function assetTileClass(row: AssetRow): string {
  const classes = ["asset-tile"];
  if (row.asset.archived_at) classes.push("is-archived");
  if (!row.asset.archived_at && row.runs.length === 0) classes.push("needs-data");
  return classes.join(" ");
}

function formatCount(count: number, label: string): string {
  return `${count} ${label}${count === 1 ? "" : "s"}`;
}

function componentModelName(asset: AssetSummary, models: ComponentModelDefinition[]) {
  if (!asset.component_model_id) return "No supported model";
  return models.find((model) => model.id === asset.component_model_id)?.name ?? asset.component_model_id;
}

function parseAssetLabels(value: string): string[] {
  const labels = cleanAssetLabels(value);
  if (labels.length > maxAssetLabels) {
    throw new Error(`Asset can have at most ${maxAssetLabels} labels.`);
  }
  return labels;
}

function cleanAssetLabels(value: string): string[] {
  const seen = new Set<string>();
  const labels: string[] = [];
  for (const rawLabel of parseCommaList(value)) {
    const label = rawLabel.trim().toLowerCase();
    if (!label || seen.has(label)) continue;
    seen.add(label);
    labels.push(label);
  }
  return labels;
}

function isRecent(value: string): boolean {
  const date = dateValue(value);
  if (!date) return false;
  return Date.now() - date <= 7 * 24 * 60 * 60 * 1000;
}

function dateValue(value?: string | null): number {
  if (!value) return 0;
  const parsed = Date.parse(value);
  return Number.isFinite(parsed) ? parsed : 0;
}
