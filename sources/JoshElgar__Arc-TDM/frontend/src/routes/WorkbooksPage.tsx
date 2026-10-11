import { Menu } from "@base-ui/react/menu";
import { Link, useNavigate, useParams } from "@tanstack/react-router";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { FormEvent } from "react";
import { Fragment, useEffect, useMemo, useState } from "react";

import { api } from "../api/client";
import type {
  ExecutionLogEntry,
  FileEntry,
  PanelSummary,
  WorkbookDataSource,
  WorkbookStep,
  WorkbookDetail,
  WorkbookInput,
  WorkbookSummary,
  WorkbookTemplateInput,
  WorkbookTemplateSummary
} from "../api/types";
import { AppIcon } from "../components/AppIcon";
import { AppSelect } from "../components/AppSelect";
import { FormDialog } from "../components/FormDialog";
import { HtmlPreview } from "../components/HtmlPreview";
import { PageLoading } from "../components/PageLoading";
import { PlotlyChart } from "../components/PlotlyChart";
import { StatusIcon, statusKind } from "../components/StatusIcon";
import { parseCommaList, parseProperties, slugify } from "../utils/formHelpers";
import { fileName, formatArcDuration, formatArcTime, shortId } from "../utils/format";
import { useWorkspaceId } from "./workspaceContext";

type WorkbookDraft = {
  id: string;
  title: string;
  templateId: string;
  linkedAssetId: string;
  tags: string;
  properties: string;
};

type TemplateDraft = {
  id: string;
  name: string;
  description: string;
  tags: string;
  properties: string;
};

type StepDraft = {
  id: string;
  title: string;
  prompt: string;
  inputRefs: string;
};

type StepAiEditDraft = {
  instruction: string;
  inputRefs: string;
};

type WorkbookDataDraft = {
  path: string;
  name: string;
  notes: string;
};

type WorkbookFilter = "all" | "asset";
type WorkbookSort = "updated" | "name" | "target" | "status";
type WorkbookDetailTab = "dashboard" | "steps" | "data" | "executions";

export function WorkbooksPage() {
  const params = useParams({ strict: false }) as { workbookId?: string };
  if (params.workbookId) return <WorkbookDetailPage workbookId={params.workbookId} />;
  return <WorkbookListPage />;
}

function WorkbookListPage() {
  const workspaceId = useWorkspaceId();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [creating, setCreating] = useState<WorkbookDraft | null>(null);
  const [creatingTemplate, setCreatingTemplate] = useState<TemplateDraft | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [templateFormError, setTemplateFormError] = useState<string | null>(null);
  const [filter, setFilter] = useState<WorkbookFilter>("all");
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState<WorkbookSort>("updated");
  const workbooks = useQuery({ queryKey: ["workbooks", workspaceId], queryFn: () => api.workbooks(workspaceId) });
  const templates = useQuery({ queryKey: ["workbook-templates", workspaceId], queryFn: () => api.workbookTemplates(workspaceId) });
  const assets = useQuery({ queryKey: ["assets", workspaceId], queryFn: () => api.assets(workspaceId) });
  const templatesById = useMemo(
    () => new Map((templates.data ?? []).map((template) => [template.id, template])),
    [templates.data]
  );
  const visibleWorkbooks = useMemo(() => {
    const query = search.trim().toLowerCase();
    return (workbooks.data ?? [])
      .filter((workbook) => {
        if (filter === "asset" && !workbook.linked_asset_id) return false;
        if (!query) return true;
        return [
          workbook.title,
          workbook.id,
          workbook.linked_asset_name ?? workbook.linked_asset_id,
          workbook.template_name ?? workbook.template_id,
          workbook.tags.join(" "),
          Object.values(workbook.properties).join(" ")
        ].some((value) => value.toLowerCase().includes(query));
      })
      .sort((a, b) => compareWorkbooks(a, b, sort));
  }, [filter, search, sort, workbooks.data]);
  const saveWorkbook = useMutation({
    mutationFn: (workbook: WorkbookInput) => api.saveWorkbook(workspaceId, workbook),
    onSuccess: (workbook) => {
      setCreating(null);
      setFormError(null);
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbook", workspaceId, workbook.id] });
      queryClient.invalidateQueries({ queryKey: ["assets", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
      navigate({ to: "/w/$workspaceId/workbooks/$workbookId", params: { workspaceId, workbookId: workbook.id } });
    }
  });
  const saveTemplate = useMutation({
    mutationFn: (template: WorkbookTemplateInput) => api.saveWorkbookTemplate(workspaceId, template),
    onSuccess: () => {
      setCreatingTemplate(null);
      setTemplateFormError(null);
      queryClient.invalidateQueries({ queryKey: ["workbook-templates", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });

  function startNewWorkbook() {
    const template = (templates.data ?? [])[0];
    setFormError(null);
    setCreating({
      id: "",
      title: "",
      templateId: template?.id ?? "",
      linkedAssetId: assets.data?.[0]?.id ?? "",
      tags: "",
      properties: ""
    });
  }

  function startNewTemplate() {
    setCreating(null);
    saveTemplate.reset();
    setTemplateFormError(null);
    setCreatingTemplate({
      id: "",
      name: "",
      description: "",
      tags: "",
      properties: ""
    });
  }

  function submitWorkbook(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!creating) return;
    try {
      const title = creating.title.trim();
      const id = slugify(creating.id || title);
      if (!id || !title) throw new Error("Workbook needs a title.");
      if (!creating.templateId) throw new Error("Choose a template.");
      if (!creating.linkedAssetId) throw new Error("Choose an asset.");
      saveWorkbook.mutate({
        id,
        title,
        template_id: creating.templateId,
        linked_asset_id: creating.linkedAssetId,
        step_order: [],
        data_sources: [],
        tags: parseCommaList(creating.tags),
        properties: parseProperties(creating.properties),
        status: "ready"
      });
    } catch (error) {
      setFormError(error instanceof Error ? error.message : "Workbook could not be saved.");
    }
  }

  function submitTemplate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!creatingTemplate) return;
    try {
      const name = creatingTemplate.name.trim();
      const id = slugify(creatingTemplate.id || name);
      if (!id || !name) throw new Error("Template needs a name.");
      saveTemplate.mutate({
        id,
        name,
        description: creatingTemplate.description.trim(),
        steps: [],
        tags: parseCommaList(creatingTemplate.tags),
        properties: parseProperties(creatingTemplate.properties)
      });
    } catch (error) {
      setTemplateFormError(error instanceof Error ? error.message : "Template could not be saved.");
    }
  }

  if (workbooks.isLoading || templates.isLoading || assets.isLoading) {
    return <PageLoading label="Loading workbooks" />;
  }

  return (
    <div className="page workbooks-page assets-page">
      <section className="assets-toolbar">
        <div className="assets-titlebar">
          <div className="assets-title-group">
            <h1>Workbooks</h1>
            <div className="assets-tabs" role="tablist" aria-label="Workbook filters">
              {([
                ["all", "All"],
                ["asset", "Assets"]
              ] as const).map(([value, label]) => (
                <button
                  className={filter === value ? "active" : ""}
                  key={value}
                  onClick={() => setFilter(value)}
                  type="button"
                >
                  {label}
                </button>
              ))}
            </div>
          </div>
          <div className="button-row">
            <button className="button" onClick={() => startNewTemplate()} type="button">
              <AppIcon name="plus" />
              New Template
            </button>
            <button className="button button-primary" disabled={!templates.data?.length || !assets.data?.length} onClick={startNewWorkbook} type="button">
              <AppIcon name="plus" />
              New Workbook
            </button>
          </div>
        </div>
        <div className="assets-controlbar">
          <label className="assets-search">
            <AppIcon name="search" />
            <input placeholder="Search workbooks" value={search} onChange={(event) => setSearch(event.target.value)} />
          </label>
          <div className="assets-sort">
            <span>Sort</span>
            <AppSelect
              ariaLabel="Sort workbooks"
              options={[
                { label: "Updated", value: "updated" },
                { label: "Name", value: "name" },
                { label: "Target", value: "target" },
                { label: "Status", value: "status" }
              ]}
              value={sort}
              onValueChange={(value) => setSort(value as WorkbookSort)}
            />
          </div>
        </div>
      </section>

      {creating ? (
        <FormDialog title="New workbook" onClose={() => setCreating(null)}>
          <WorkbookForm
            assets={assets.data ?? []}
            draft={creating}
            error={formError || (saveWorkbook.error instanceof Error ? saveWorkbook.error.message : null)}
            pending={saveWorkbook.isPending}
            templates={templates.data ?? []}
            onCancel={() => setCreating(null)}
            onChange={(patch) => setCreating((current) => current ? { ...current, ...patch } : current)}
            onSubmit={submitWorkbook}
          />
        </FormDialog>
      ) : null}

      {creatingTemplate ? (
        <FormDialog title="New template" onClose={() => setCreatingTemplate(null)}>
          <WorkbookTemplateForm
            draft={creatingTemplate}
            error={templateFormError || (saveTemplate.error instanceof Error ? saveTemplate.error.message : null)}
            pending={saveTemplate.isPending}
            onCancel={() => setCreatingTemplate(null)}
            onChange={(patch) => setCreatingTemplate((current) => current ? { ...current, ...patch } : current)}
            onSubmit={submitTemplate}
          />
        </FormDialog>
      ) : null}

      <section className="asset-tile-grid workbook-tile-grid" aria-label="Workbooks">
        {visibleWorkbooks.map((workbook) => (
          <Link
            className={workbookTileClass(workbook)}
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
            <div className="asset-chip-row">
              <span>{formatCount(templateStepCount(templatesById.get(workbook.template_id), workbook), "step")}</span>
              <span>{workbook.template_name ?? workbook.template_id}</span>
            </div>
          </Link>
        ))}
        {!visibleWorkbooks.length ? (
          templates.data?.length ? (
            <button className="asset-empty-card" onClick={startNewWorkbook} type="button">
              <AppIcon name="plus" size={22} />
              <strong>Create new workbook</strong>
              <span>Choose an asset, then add Python steps and data.</span>
            </button>
          ) : (
            <button className="asset-empty-card" onClick={() => startNewTemplate()} type="button">
              <AppIcon name="steps" size={22} />
              <strong>No workbook templates yet</strong>
              <span>Create a blank template first, then make workbooks from it.</span>
            </button>
          )
        ) : null}
      </section>
    </div>
  );
}

function WorkbookDetailPage({ workbookId }: { workbookId: string }) {
  const workspaceId = useWorkspaceId();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [selectedStepId, setSelectedStepId] = useState<string>();
  const [creatingStep, setCreatingStep] = useState(false);
  const [expandedExecutionId, setExpandedExecutionId] = useState<string>();
  const [liveLogEntries, setLiveLogEntries] = useState<ExecutionLogEntry[]>([]);
  const files = useQuery({ queryKey: ["files", workspaceId], queryFn: () => api.files(workspaceId) });
  const detail = useQuery({
    queryKey: ["workbook", workspaceId, workbookId],
    queryFn: () => api.workbook(workspaceId, workbookId)
  });
  const executionLogs = useQuery({
    queryKey: ["execution-logs", workspaceId, expandedExecutionId],
    queryFn: () => api.executionLogs(workspaceId, expandedExecutionId!),
    enabled: Boolean(expandedExecutionId)
  });
  const computeWorkbook = useMutation({
    mutationFn: () => api.computeWorkbook(workspaceId, workbookId),
    onSuccess: (execution) => {
      setExpandedExecutionId(execution.id);
      setLiveLogEntries([]);
      const source = new EventSource(api.executionLogStreamUrl(workspaceId, execution.id));
      source.onmessage = (event) => {
        setLiveLogEntries((current) => [...current, JSON.parse(event.data) as ExecutionLogEntry]);
      };
      source.onerror = () => {
        source.close();
        queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
        queryClient.invalidateQueries({ queryKey: ["workbook", workspaceId, workbookId] });
        queryClient.invalidateQueries({ queryKey: ["charts", workspaceId] });
        queryClient.invalidateQueries({ queryKey: ["reports", workspaceId] });
        queryClient.invalidateQueries({ queryKey: ["executions", workspaceId] });
        queryClient.invalidateQueries({ queryKey: ["execution-logs", workspaceId, execution.id] });
      };
    }
  });
  const saveWorkbook = useMutation({
    mutationFn: (workbook: WorkbookInput) => api.saveWorkbook(workspaceId, workbook),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workbook", workspaceId, workbookId] });
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });
  const duplicateWorkbook = useMutation({
    mutationFn: () => {
      const current = detail.data?.workbook;
      if (!current) throw new Error("Workbook is not loaded.");
      return api.duplicateWorkbook(workspaceId, current.id, {
        title: `${current.title} Copy`,
        linked_asset_id: current.linked_asset_id,
        data_sources: current.data_sources
      });
    },
    onSuccess: (workbook) => {
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
      navigate({ to: "/w/$workspaceId/workbooks/$workbookId", params: { workspaceId, workbookId: workbook.id } });
    }
  });
  const saveStep = useMutation({
    mutationFn: async ({ step }: { step: WorkbookStep; isNew: boolean }) => {
      const current = detail.data;
      if (!current) throw new Error("Workbook is not loaded.");
      return api.saveWorkbookStep(workspaceId, current.workbook.id, step);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workbook", workspaceId, workbookId] });
      queryClient.invalidateQueries({ queryKey: ["workbook-templates", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });
  const deleteStep = useMutation({
    mutationFn: (stepId: string) => {
      const current = detail.data;
      if (!current) throw new Error("Workbook is not loaded.");
      return api.deleteWorkbookStep(workspaceId, current.workbook.id, stepId);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workbook", workspaceId, workbookId] });
      queryClient.invalidateQueries({ queryKey: ["workbook-templates", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["workbooks", workspaceId] });
      queryClient.invalidateQueries({ queryKey: ["git-status", workspaceId] });
    }
  });
  const generateStep = useMutation({
    mutationFn: (draft: StepDraft) => {
      const current = detail.data;
      if (!current) throw new Error("Workbook is not loaded.");
      return api.generateWorkbookStep(workspaceId, current.workbook.id, {
        title: draft.title.trim(),
        prompt: draft.prompt.trim(),
        input_refs: parseCommaList(draft.inputRefs)
      });
    }
  });
  const reviseStep = useMutation({
    mutationFn: ({ stepId, draft }: { stepId: string; draft: StepAiEditDraft }) => {
      const current = detail.data;
      if (!current) throw new Error("Workbook is not loaded.");
      return api.reviseWorkbookStep(workspaceId, current.workbook.id, stepId, {
        instruction: draft.instruction.trim(),
        input_refs: parseCommaList(draft.inputRefs)
      });
    }
  });

  function saveWorkbookData(dataSources: WorkbookDataSource[]) {
    if (!detail.data) return;
    saveWorkbook.mutate({ ...detail.data.workbook, data_sources: dataSources });
  }

  if (detail.isLoading || files.isLoading) return <PageLoading label="Loading workbook" />;
  if (!detail.data) {
    return (
      <div className="page assets-page workbook-detail-page">
        <section className="workbook-detail-header">
          <nav className="asset-breadcrumbs" aria-label="Breadcrumbs">
            <Link params={{ workspaceId }} to="/w/$workspaceId/workbooks">Workbooks</Link>
          </nav>
          <p className="empty-state">Workbook not found.</p>
        </section>
      </div>
    );
  }

  return (
    <div className="page assets-page workbook-detail-page">
      <WorkbookDetailHeader
        detail={detail.data}
        duplicatePending={duplicateWorkbook.isPending}
        pending={computeWorkbook.isPending}
        onCompute={() => computeWorkbook.mutate()}
        onDuplicate={() => duplicateWorkbook.mutate()}
        workspaceId={workspaceId}
      />
      <WorkbookContent
        computeError={computeWorkbook.error instanceof Error ? computeWorkbook.error.message : null}
        creatingStep={creatingStep}
        dataError={saveWorkbook.error instanceof Error ? saveWorkbook.error.message : null}
        detail={detail.data}
        error={
          saveStep.error instanceof Error
            ? saveStep.error.message
            : deleteStep.error instanceof Error
              ? deleteStep.error.message
              : null
        }
        expandedExecutionId={expandedExecutionId}
        files={files.data ?? []}
        liveLogEntries={liveLogEntries}
        logs={executionLogs.data?.text}
        onAddStep={() => {
          generateStep.reset();
          setCreatingStep(true);
        }}
        onCloseModal={() => {
          generateStep.reset();
          setCreatingStep(false);
        }}
        onOpenStep={(stepId) => setSelectedStepId(stepId)}
        onSaveDataSources={saveWorkbookData}
        onToggleExecution={(executionId) =>
          setExpandedExecutionId((current) => (current === executionId ? undefined : executionId))
        }
        pending={saveStep.isPending}
        generateError={generateStep.error instanceof Error ? generateStep.error.message : null}
        generating={generateStep.isPending}
        savingData={saveWorkbook.isPending}
        onGenerateStep={(draft) => generateStep.mutateAsync(draft)}
        onSaveStep={(step, isNew) => {
          saveStep.mutate({ step, isNew });
          generateStep.reset();
          setSelectedStepId(undefined);
          setCreatingStep(false);
        }}
        workspaceId={workspaceId}
      />
      {selectedStepId ? (
        <WorkbookStepDetailDialog
          deleting={deleteStep.isPending && deleteStep.variables === selectedStepId}
          detail={detail.data}
          error={reviseStep.error instanceof Error ? reviseStep.error.message : null}
          revising={reviseStep.isPending}
          saving={Boolean(saveStep.isPending && saveStep.variables?.step.id === selectedStepId)}
          step={detail.data.steps.find((candidate) => candidate.id === selectedStepId) ?? null}
          workspaceId={workspaceId}
          onDelete={(step) => {
            if (!window.confirm(`Delete "${step.title}"?`)) return;
            deleteStep.mutate(step.id);
            setSelectedStepId(undefined);
          }}
          onClose={() => {
            reviseStep.reset();
            setSelectedStepId(undefined);
          }}
          onReviseStep={(step, draft) => reviseStep.mutateAsync({ stepId: step.id, draft })}
          onSaveRevision={(step) => {
            saveStep.mutate({ step, isNew: false });
            reviseStep.reset();
            setSelectedStepId(undefined);
          }}
        />
      ) : null}
    </div>
  );
}

function WorkbookTemplateForm({
  draft,
  error,
  pending,
  onCancel,
  onChange,
  onSubmit
}: {
  draft: TemplateDraft;
  error?: string | null;
  pending: boolean;
  onCancel: () => void;
  onChange: (patch: Partial<TemplateDraft>) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <form className="asset-form workbook-form" onSubmit={onSubmit}>
      <div className="asset-form-header">
        <div>
          <h2>New template</h2>
          <p>A template is a blank starter for future workbooks.</p>
        </div>
      </div>
      <div className="asset-form-grid">
        <label className="settings-field">
          <span>Name</span>
          <input value={draft.name} onChange={(event) => onChange({ name: event.target.value })} />
        </label>
        <label className="settings-field form-span-full">
          <span>Description</span>
          <textarea className="settings-prompt small" value={draft.description} onChange={(event) => onChange({ description: event.target.value })} />
        </label>
        <label className="settings-field">
          <span>Labels</span>
          <input value={draft.tags} onChange={(event) => onChange({ tags: event.target.value })} />
        </label>
        <label className="settings-field form-span-full">
          <span>Properties JSON</span>
          <textarea className="settings-prompt small" value={draft.properties} onChange={(event) => onChange({ properties: event.target.value })} />
        </label>
        <div className="button-row form-span-full">
          <button className="button-primary" disabled={pending} type="submit">
            <AppIcon name={pending ? "spinner" : "save"} />
            Save template
          </button>
          <button disabled={pending} onClick={onCancel} type="button">Cancel</button>
          {error ? <span className="muted">{error}</span> : null}
        </div>
      </div>
    </form>
  );
}

function WorkbookForm({
  assets,
  draft,
  error,
  pending,
  templates,
  onCancel,
  onChange,
  onSubmit
}: {
  assets: Array<{ id: string; name: string }>;
  draft: WorkbookDraft;
  error?: string | null;
  pending: boolean;
  templates: Array<{ id: string; name: string }>;
  onCancel: () => void;
  onChange: (patch: Partial<WorkbookDraft>) => void;
  onSubmit: (event: FormEvent<HTMLFormElement>) => void;
}) {
  return (
    <form className="asset-form workbook-form" onSubmit={onSubmit}>
      <div className="asset-form-header">
        <div>
          <h2>New workbook</h2>
          <p>Workbooks belong to one asset. Attach run-specific data inside the workbook.</p>
        </div>
      </div>
      <div className="asset-form-grid">
        <label className="settings-field">
          <span>Title</span>
          <input value={draft.title} onChange={(event) => onChange({ title: event.target.value })} />
        </label>
        <div className="settings-field">
          <span>Start from</span>
          <AppSelect
            ariaLabel="Select workbook template"
            options={templates.map((template) => ({ label: template.name, value: template.id }))}
            value={draft.templateId}
            onValueChange={(value) => onChange({ templateId: value })}
          />
        </div>
        <div className="settings-field">
          <span>Linked asset</span>
          <AppSelect
            ariaLabel="Select linked asset"
            options={assets.map((asset) => ({ label: asset.name, value: asset.id }))}
            value={draft.linkedAssetId}
            onValueChange={(value) => onChange({ linkedAssetId: value })}
          />
        </div>
        <label className="settings-field">
          <span>Labels</span>
          <input value={draft.tags} onChange={(event) => onChange({ tags: event.target.value })} />
        </label>
        <label className="settings-field form-span-full">
          <span>Properties JSON</span>
          <textarea className="settings-prompt small" value={draft.properties} onChange={(event) => onChange({ properties: event.target.value })} />
        </label>
        <div className="button-row form-span-full">
          <button className="button-primary" disabled={pending} type="submit">
            <AppIcon name={pending ? "spinner" : "save"} />
            Save workbook
          </button>
          <button disabled={pending} onClick={onCancel} type="button">Cancel</button>
          {error ? <span className="muted">{error}</span> : null}
        </div>
      </div>
    </form>
  );
}

function WorkbookDetailHeader({
  detail,
  duplicatePending,
  pending,
  onCompute,
  onDuplicate,
  workspaceId
}: {
  detail: WorkbookDetail;
  duplicatePending: boolean;
  pending: boolean;
  onCompute: () => void;
  onDuplicate: () => void;
  workspaceId: string;
}) {
  const workbook = detail.workbook;
  return (
    <section className="workbook-detail-header">
      <div className="workbook-detail-title">
        <div>
          <nav className="asset-breadcrumbs" aria-label="Breadcrumbs">
            <Link params={{ workspaceId }} to="/w/$workspaceId/workbooks">Workbooks</Link>
            <span>/</span>
            <WorkbookTargetBreadcrumbItem workbook={workbook} workspaceId={workspaceId} />
            <span>/</span>
            <span>{workbook.title}</span>
          </nav>
          <div className="workbook-title-row">
            <h1>{workbook.title}</h1>
          </div>
        </div>
      </div>
      <div className="header-actions">
        <button className="button" disabled={duplicatePending} onClick={onDuplicate} type="button">
          <AppIcon name={duplicatePending ? "spinner" : "copy"} />
          Duplicate
        </button>
        <button className="button button-run" disabled={pending} onClick={onCompute} type="button">
          <AppIcon name={pending ? "spinner" : "play"} size={18} />
          {pending ? "Running" : "Run workbook"}
        </button>
      </div>
    </section>
  );
}

function WorkbookTargetBreadcrumbItem({
  workbook,
  workspaceId
}: {
  workbook: WorkbookSummary;
  workspaceId: string;
}) {
  if (workbook.linked_asset_id) {
    return (
      <Link
        params={{ workspaceId, assetId: workbook.linked_asset_id }}
        to="/w/$workspaceId/assets/$assetId"
      >
        {workbook.linked_asset_name ?? workbook.linked_asset_id}
      </Link>
    );
  }

  return <span>Missing asset</span>;
}

function WorkbookContent({
  computeError,
  creatingStep,
  dataError,
  detail,
  error,
  expandedExecutionId,
  files,
  liveLogEntries,
  logs,
  onAddStep,
  onCloseModal,
  onOpenStep,
  onSaveDataSources,
  onToggleExecution,
  pending,
  generateError,
  generating,
  savingData,
  onGenerateStep,
  onSaveStep,
  workspaceId
}: {
  computeError?: string | null;
  creatingStep: boolean;
  dataError?: string | null;
  detail: WorkbookDetail;
  error?: string | null;
  expandedExecutionId?: string;
  files: FileEntry[];
  liveLogEntries: ExecutionLogEntry[];
  logs?: string;
  onAddStep: () => void;
  onCloseModal: () => void;
  onOpenStep: (stepId: string) => void;
  onSaveDataSources: (dataSources: WorkbookDataSource[]) => void;
  onToggleExecution: (executionId: string) => void;
  pending: boolean;
  generateError?: string | null;
  generating: boolean;
  savingData: boolean;
  onGenerateStep: (draft: StepDraft) => Promise<WorkbookStep>;
  onSaveStep: (step: WorkbookStep, isNew: boolean) => void;
  workspaceId: string;
}) {
  const [newStep, setNewStep] = useState<StepDraft>(() => emptyStepDraft());
  const [activeTab, setActiveTab] = useState<WorkbookDetailTab>("dashboard");
  const expandedExecution = detail.executions.find((execution) => execution.id === expandedExecutionId);
  const liveLogText = renderExecutionLogEntries(liveLogEntries);
  const expandedLogText =
    logs?.trim() || liveLogText || (expandedExecution ? "Waiting for logs..." : "No logs recorded for this execution.");
  return (
    <div className="workbook-detail-content">
      {computeError ? <p className="inline-error">{computeError}</p> : null}
      {error ? <p className="inline-error">{error}</p> : null}
      <WorkbookDetailTabs activeTab={activeTab} onChange={setActiveTab} />
      <div className="workbook-tab-panel">
        {activeTab === "dashboard" ? (
          <WorkbookPanelsSection detail={detail} workspaceId={workspaceId} onOpenStep={onOpenStep} />
        ) : null}
        {activeTab === "steps" ? (
          <WorkbookStepsTable
            detail={detail}
            onAddStep={onAddStep}
            onOpenStep={onOpenStep}
          />
        ) : null}
        {activeTab === "data" ? (
          <WorkbookDataSection
            detail={detail}
            error={dataError}
            files={files}
            pending={savingData}
            onSave={onSaveDataSources}
          />
        ) : null}
        {activeTab === "executions" ? (
          <WorkbookExecutionsSection
            detail={detail}
            expandedExecutionId={expandedExecutionId}
            expandedLogText={expandedLogText}
            onToggleExecution={onToggleExecution}
          />
        ) : null}
      </div>
      {creatingStep ? (
        <WorkbookStepCreateDialog
          dataSources={detail.workbook.data_sources}
          draft={newStep}
          error={generateError}
          generating={generating}
          pending={pending}
          onChange={(patch) => setNewStep((current) => ({ ...current, ...patch }))}
          onClose={() => {
            setNewStep(emptyStepDraft());
            onCloseModal();
          }}
          onGenerate={onGenerateStep}
          onSave={(step) => {
            onSaveStep(step, true);
            setNewStep(emptyStepDraft());
          }}
        />
      ) : null}
    </div>
  );
}

function WorkbookDetailTabs({
  activeTab,
  onChange
}: {
  activeTab: WorkbookDetailTab;
  onChange: (tab: WorkbookDetailTab) => void;
}) {
  const tabs: Array<{ id: WorkbookDetailTab; label: string }> = [
    { id: "dashboard", label: "Dashboard" },
    { id: "steps", label: "Steps" },
    { id: "data", label: "Data" },
    { id: "executions", label: "Executions" }
  ];

  return (
    <div className="workbook-detail-tabs" role="tablist" aria-label="Workbook sections">
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

function WorkbookExecutionsSection({
  detail,
  expandedExecutionId,
  expandedLogText,
  onToggleExecution
}: {
  detail: WorkbookDetail;
  expandedExecutionId?: string;
  expandedLogText: string;
  onToggleExecution: (executionId: string) => void;
}) {
  return (
    <section className="panel workbook-executions">
      <div className="section-heading">
        <h2>Executions</h2>
        <span>{detail.executions.length}</span>
      </div>
      <div className="table-surface">
        <table className="meta-table">
          <thead>
            <tr>
              <th>Execution</th>
              <th>Status</th>
              <th>Started</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            {detail.executions.map((execution) => {
              const expanded = execution.id === expandedExecutionId;
              return (
                <Fragment key={execution.id}>
                  <tr
                    className={expanded ? "table-click-row execution-row active" : "table-click-row execution-row"}
                    onClick={() => onToggleExecution(execution.id)}
                    onKeyDown={(event) => {
                      if (event.key === "Enter" || event.key === " ") {
                        event.preventDefault();
                        onToggleExecution(execution.id);
                      }
                    }}
                    role="button"
                    tabIndex={0}
                  >
                    <td>{shortId(execution.id)}</td>
                    <td>
                      <span className={`table-status-badge ${statusKind(execution.status)}`}>
                        {execution.status}
                      </span>
                    </td>
                    <td>{formatArcTime(execution.started_at)}</td>
                    <td>{formatArcDuration(execution.started_at, execution.completed_at)}</td>
                  </tr>
                  {expanded ? (
                    <tr className="expanded-execution-row">
                      <td colSpan={4}>
                        <ExecutionLogExpansion execution={execution} text={expandedLogText} />
                      </td>
                    </tr>
                  ) : null}
                </Fragment>
              );
            })}
          </tbody>
        </table>
        {!detail.executions.length ? <p className="empty-state table-empty">No executions yet.</p> : null}
      </div>
    </section>
  );
}

function ExecutionLogExpansion({
  execution,
  text
}: {
  execution: WorkbookDetail["executions"][number];
  text: string;
}) {
  return (
    <div className="execution-log-expansion">
      {execution.error ? (
        <div className="inline-error">
          <StatusIcon status="error" />
          <span>{execution.error}</span>
        </div>
      ) : null}
      <div className="run-card-section">
        <div className="execution-log-heading">
          <h3>Logs</h3>
          <span>{execution.log_count} entries</span>
        </div>
        <pre className="simple-log">{text}</pre>
      </div>
    </div>
  );
}

function renderExecutionLogEntries(entries: ExecutionLogEntry[]) {
  return entries.map(renderExecutionLogEntry).join("\n").trim();
}

function renderExecutionLogEntry(entry: ExecutionLogEntry) {
  const step = entry.step_id ? ` ${entry.step_id}` : "";
  return `${entry.timestamp} ${entry.level} ${entry.source}${step} ${entry.message}`;
}

function StepDraftEditor({
  dataSources,
  draft,
  error,
  pending,
  submitLabel,
  submitIcon = "save",
  extraAction,
  onChange,
  onSubmit
}: {
  dataSources: WorkbookDataSource[];
  draft: StepDraft;
  error?: string | null;
  pending: boolean;
  submitLabel: string;
  submitIcon?: "save" | "plus" | null;
  extraAction?: {
    label: string;
    icon: "check";
    onClick: () => void;
  };
  onChange: (patch: Partial<StepDraft>) => void;
  onSubmit: () => void;
}) {
  const selectedDataSourceIds = new Set(parseCommaList(draft.inputRefs));

  function toggleDataSource(dataSourceId: string) {
    const next = new Set(selectedDataSourceIds);
    if (next.has(dataSourceId)) next.delete(dataSourceId);
    else next.add(dataSourceId);
    onChange({ inputRefs: Array.from(next).join(", ") });
  }

  return (
    <form
      className="asset-form workbook-form"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <div className="asset-form-grid">
        {error ? <p className="inline-error form-span-full">{error}</p> : null}
        <label className="settings-field">
          <span>Title</span>
          <input
            placeholder="Leave blank to auto-generate from description."
            value={draft.title}
            onChange={(event) => onChange({ title: event.target.value })}
          />
        </label>
        <section className="settings-field form-span-full workbook-step-data-picker">
          <span>workbook data, optional</span>
          {dataSources.length ? (
            <div className="table-surface">
              <table className="meta-table workbook-step-data-table">
                <thead>
                  <tr>
                    <th aria-label="Use" />
                    <th>Name</th>
                    <th>Kind</th>
                    <th>Path</th>
                  </tr>
                </thead>
                <tbody>
                  {dataSources.map((source) => (
                    <tr className="table-click-row" key={source.id} onClick={() => toggleDataSource(source.id)}>
                      <td>
                        <input
                          checked={selectedDataSourceIds.has(source.id)}
                          aria-label={`Use ${source.name}`}
                          readOnly
                          type="checkbox"
                        />
                      </td>
                      <td>{source.name}</td>
                      <td>{source.kind}</td>
                      <td>{source.path}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p className="empty-state">No workbook data attached.</p>
          )}
        </section>
        <label className="settings-field form-span-full">
          <span>Description</span>
          <textarea
            className="settings-prompt small"
            placeholder="Check EEG signal quality and summarize anything suspicious."
            value={draft.prompt}
            onChange={(event) => onChange({ prompt: event.target.value })}
          />
        </label>
        <div className="button-row form-span-full">
          <button className="button-primary" disabled={pending || !hasStepContent(draft)} type="submit">
            {pending ? <AppIcon name="spinner" /> : submitIcon ? <AppIcon name={submitIcon} /> : null}
            {submitLabel}
          </button>
          {extraAction ? (
            <button disabled={pending || !hasStepContent(draft)} onClick={extraAction.onClick} type="button">
              <AppIcon name={extraAction.icon} />
              {extraAction.label}
            </button>
          ) : null}
        </div>
      </div>
    </form>
  );
}

function WorkbookStepDetailContent({
  dataSources,
  deleting,
  draft,
  error,
  pending,
  revisedStep,
  onDelete,
  onChangeDraft,
  onGenerateRevision,
  onSaveRevision,
  onClearRevision,
  step,
  workspaceId
}: {
  dataSources: WorkbookDataSource[];
  deleting: boolean;
  draft: StepAiEditDraft;
  error?: string | null;
  pending: boolean;
  revisedStep: WorkbookStep | null;
  onDelete: (step: WorkbookStep) => void;
  onChangeDraft: (patch: Partial<StepAiEditDraft>) => void;
  onGenerateRevision: () => void;
  onSaveRevision: (step: WorkbookStep) => void;
  onClearRevision: () => void;
  step: WorkbookStep;
  workspaceId: string;
}) {
  return (
    <article className="workbook-step-detail">
      {dataSources.length ? (
        <div className="workbook-step-data-link-row" aria-label="Workbook data used">
          {dataSources.map((source) => (
            <Link
              className="workbook-step-data-link"
              key={source.id}
              params={{ workspaceId }}
              search={{ file: source.path }}
              to="/w/$workspaceId/data"
            >
              @{fileName(source.path)}
            </Link>
          ))}
        </div>
      ) : null}
      <div className="workbook-step-meta">
        <p>
          <span>Description</span>
          <strong>{step.prompt || "No purpose written yet."}</strong>
        </p>
      </div>
      <PythonScriptPreview code={step.script ?? ""} />
      <WorkbookStepAiInlineEditor
        draft={draft}
        error={error}
        pending={pending}
        revisedStep={revisedStep}
        onChange={onChangeDraft}
        onClearRevision={onClearRevision}
        onSaveRevision={onSaveRevision}
        onSubmit={onGenerateRevision}
      />
      <div className="workbook-step-detail-actions">
        <button className="button button-danger" disabled={deleting} onClick={() => onDelete(step)} type="button">
          <AppIcon name={deleting ? "spinner" : "trash"} />
          Delete Step
        </button>
      </div>
    </article>
  );
}

function WorkbookStepDetailDialog({
  deleting,
  detail,
  error,
  revising,
  saving,
  step,
  workspaceId,
  onDelete,
  onReviseStep,
  onSaveRevision,
  onClose
}: {
  deleting: boolean;
  detail: WorkbookDetail;
  error?: string | null;
  revising: boolean;
  saving: boolean;
  step: WorkbookStep | null;
  workspaceId: string;
  onDelete: (step: WorkbookStep) => void;
  onReviseStep: (step: WorkbookStep, draft: StepAiEditDraft) => Promise<WorkbookStep>;
  onSaveRevision: (step: WorkbookStep) => void;
  onClose: () => void;
}) {
  const [draft, setDraft] = useState<StepAiEditDraft>(() => stepAiEditDraft(step));
  const [revisedStep, setRevisedStep] = useState<WorkbookStep | null>(null);

  useEffect(() => {
    setDraft(stepAiEditDraft(step));
    setRevisedStep(null);
  }, [step?.id]);

  if (!step) return null;
  const dataSources = dataSourcesForStep(detail.workbook.data_sources, step);

  async function generateRevision() {
    const revision = await onReviseStep(step!, draft);
    setRevisedStep(revision);
  }

  return (
    <FormDialog title={step.title} onClose={onClose}>
      <WorkbookStepDetailContent
        dataSources={dataSources}
        deleting={deleting}
        draft={draft}
        error={error}
        pending={revising || saving}
        revisedStep={revisedStep}
        onChangeDraft={(patch) => {
          setDraft((current) => ({ ...current, ...patch }));
          setRevisedStep(null);
        }}
        onClearRevision={() => setRevisedStep(null)}
        onDelete={onDelete}
        onGenerateRevision={generateRevision}
        onSaveRevision={(nextStep) => onSaveRevision(nextStep)}
        step={step}
        workspaceId={workspaceId}
      />
    </FormDialog>
  );
}

function WorkbookStepAiInlineEditor({
  draft,
  error,
  pending,
  revisedStep,
  onChange,
  onClearRevision,
  onSaveRevision,
  onSubmit
}: {
  draft: StepAiEditDraft;
  error?: string | null;
  pending: boolean;
  revisedStep: WorkbookStep | null;
  onChange: (patch: Partial<StepAiEditDraft>) => void;
  onClearRevision: () => void;
  onSaveRevision: (step: WorkbookStep) => void;
  onSubmit: () => void;
}) {
  return (
    <form
      className="workbook-step-ai-inline-editor"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      {error ? <p className="inline-error">{error}</p> : null}
      <label className="workbook-step-ai-input">
        <span>Edit with AI</span>
        <div>
          <textarea
            placeholder="Ask for a change to this step..."
            rows={2}
            value={draft.instruction}
            onChange={(event) => {
              onChange({ instruction: event.target.value });
              onClearRevision();
            }}
          />
          <button
            aria-label="Generate revision"
            className="button button-icon"
            disabled={pending || !hasStepAiEditContent(draft)}
            type="submit"
          >
            <AppIcon name={pending ? "spinner" : "send"} />
          </button>
        </div>
      </label>
      {revisedStep ? (
        <div className="workbook-step-revision-inline">
          <div className="workbook-generated-step-summary">
            <h2>{revisedStep.title}</h2>
            <p>{revisedStep.prompt || "No description written."}</p>
          </div>
          <PythonScriptPreview code={revisedStep.script ?? ""} />
          <div className="button-row">
            <button disabled={pending} onClick={onClearRevision} type="button">
              Discard
            </button>
            <button disabled={pending} onClick={() => onSaveRevision(revisedStep)} type="button">
              <AppIcon name={pending ? "spinner" : "save"} />
              Save
            </button>
            <button className="button-primary" disabled={pending} onClick={() => onSaveRevision({ ...revisedStep, active: true })} type="button">
              <AppIcon name={pending ? "spinner" : "check"} />
              Save and activate
            </button>
          </div>
        </div>
      ) : null}
    </form>
  );
}

function WorkbookStepCreateDialog({
  dataSources,
  draft,
  error,
  generating,
  pending,
  onChange,
  onClose,
  onGenerate,
  onSave
}: {
  dataSources: WorkbookDataSource[];
  draft: StepDraft;
  error?: string | null;
  generating: boolean;
  pending: boolean;
  onChange: (patch: Partial<StepDraft>) => void;
  onClose: () => void;
  onGenerate: (draft: StepDraft) => Promise<WorkbookStep>;
  onSave: (step: WorkbookStep) => void;
}) {
  const [generatedStep, setGeneratedStep] = useState<WorkbookStep | null>(null);

  async function generateStep() {
    const step = await onGenerate(draft);
    setGeneratedStep(step);
  }

  return (
    <FormDialog title="Add a step" onClose={onClose}>
      {generatedStep ? (
        <div className="workbook-generated-step-review">
          <div className="workbook-generated-step-summary">
            <h2>{generatedStep.title}</h2>
            <p>{generatedStep.prompt || "No description written."}</p>
          </div>
          <PythonScriptPreview code={generatedStep.script ?? ""} />
          <div className="button-row">
            <button disabled={pending} onClick={() => setGeneratedStep(null)} type="button">
              Back
            </button>
            <button disabled={pending} onClick={() => onSave(generatedStep)} type="button">
              <AppIcon name={pending ? "spinner" : "save"} />
              Save
            </button>
            <button className="button-primary" disabled={pending} onClick={() => onSave({ ...generatedStep, active: true })} type="button">
              <AppIcon name={pending ? "spinner" : "check"} />
              Save and activate
            </button>
          </div>
        </div>
      ) : (
        <StepDraftEditor
          dataSources={dataSources}
          draft={draft}
          error={error}
          pending={pending || generating}
          submitIcon={null}
          submitLabel={generating ? "Generating step" : "Generate step"}
          onChange={(patch) => {
            setGeneratedStep(null);
            onChange(patch);
          }}
          onSubmit={generateStep}
        />
      )}
    </FormDialog>
  );
}

function PythonScriptPreview({ code }: { code: string }) {
  const [html, setHtml] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setHtml(null);
    import("shiki")
      .then(({ codeToHtml }) =>
        codeToHtml(code, {
          lang: "python",
          theme: "github-light"
        })
      )
      .then((nextHtml) => {
        if (!cancelled) setHtml(nextHtml);
      })
      .catch(() => {
        if (!cancelled) setHtml(null);
      });
    return () => {
      cancelled = true;
    };
  }, [code]);

  return (
    <pre className="step-script-code workbook-generated-step-code">
      {html ? (
        <div className="step-script-highlight" dangerouslySetInnerHTML={{ __html: html }} />
      ) : (
        <code>{code}</code>
      )}
    </pre>
  );
}

function WorkbookPanelsSection({
  detail,
  workspaceId,
  onOpenStep
}: {
  detail: WorkbookDetail;
  workspaceId: string;
  onOpenStep: (stepId: string) => void;
}) {
  const [openReport, setOpenReport] = useState<WorkbookDetail["reports"][number] | null>(null);

  return (
    <section className="workbook-panels" aria-label="Workbook panels">
      <div className="workbook-panel-grid">
        {detail.panels.map((panel) => (
          <WorkbookPanelCard
            detail={detail}
            key={panel.id}
            panel={panel}
            workspaceId={workspaceId}
            onOpenReport={setOpenReport}
            onOpenStep={onOpenStep}
          />
        ))}
        {!detail.panels.length ? (
          <div className="asset-empty-card is-static">
            <AppIcon name="dashboard" size={22} />
            <strong>No panels yet</strong>
            <span>Run the workbook to create visible charts, reports, or checks.</span>
          </div>
        ) : null}
      </div>
      {openReport ? (
        <WorkbookPanelReportDialog
          report={openReport}
          workspaceId={workspaceId}
          onClose={() => setOpenReport(null)}
        />
      ) : null}
    </section>
  );
}

function WorkbookDataSection({
  detail,
  error,
  files,
  pending,
  onSave
}: {
  detail: WorkbookDetail;
  error?: string | null;
  files: FileEntry[];
  pending: boolean;
  onSave: (dataSources: WorkbookDataSource[]) => void;
}) {
  const attachedPaths = new Set(detail.workbook.data_sources.map((source) => source.path));
  const availableFiles = files.filter(
    (file) => (file.kind === "file" || file.source_kind === "dataset") && !attachedPaths.has(file.path)
  );
  const [draft, setDraft] = useState<WorkbookDataDraft | null>(null);

  function startAttach() {
    const first = availableFiles[0];
    setDraft({
      path: first?.path ?? "",
      name: first?.name ?? "",
      notes: ""
    });
  }

  function attachData(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!draft?.path) return;
    const file = files.find((candidate) => candidate.path === draft.path);
    const name = draft.name.trim() || file?.name || draft.path.split("/").pop() || draft.path;
    onSave([
      ...detail.workbook.data_sources,
      {
        id: slugify(name || draft.path),
        name,
        path: draft.path,
        kind: file?.source_kind === "dataset" ? "dataset" : file?.kind ?? "file",
        notes: draft.notes.trim()
      }
    ]);
    setDraft(null);
  }

  function removeData(sourceId: string) {
    onSave(detail.workbook.data_sources.filter((source) => source.id !== sourceId));
  }

  return (
    <section className="panel workbook-data-section" aria-label="Workbook data">
      <div className="section-heading">
        <h2>Workbook Data</h2>
        <div className="workbook-steps-heading-actions">
          <span>{detail.workbook.data_sources.length}</span>
          <button className="button button-table" disabled={!availableFiles.length || pending} onClick={startAttach} type="button">
            <AppIcon name="plus" />
            Add data
          </button>
        </div>
      </div>
      {error ? <p className="inline-error">{error}</p> : null}
      {detail.workbook.data_sources.length ? (
        <div className="table-surface">
          <table className="meta-table workbook-data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Kind</th>
                <th>Path</th>
                <th>Notes</th>
                <th aria-label="Actions" />
              </tr>
            </thead>
            <tbody>
              {detail.workbook.data_sources.map((source) => (
                <tr key={source.id}>
                  <td>{source.name}</td>
                  <td>{source.kind}</td>
                  <td>{source.path}</td>
                  <td>{source.notes || "-"}</td>
                  <td>
                    <button className="button button-table" disabled={pending} onClick={() => removeData(source.id)} type="button">
                      <AppIcon name="trash" />
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <button className="asset-empty-card workbook-data-empty-card" disabled={!availableFiles.length || pending} onClick={startAttach} type="button">
          <div className="workbook-steps-empty-card-title">
            <AppIcon name="data" size={18} />
            <strong>Add workbook data</strong>
          </div>
          <span>Attach files or datasets that steps can inspect and analyze.</span>
        </button>
      )}
      {draft ? (
        <FormDialog title="Add workbook data" onClose={() => setDraft(null)}>
          <form className="asset-form workbook-form" onSubmit={attachData}>
            <div className="asset-form-grid">
              <div className="settings-field form-span-full">
                <span>Data source</span>
                <AppSelect
                  ariaLabel="Select workbook data source"
                  options={availableFiles.map((file) => ({ label: file.path, value: file.path }))}
                  value={draft.path}
                  onValueChange={(value) => {
                    const file = files.find((candidate) => candidate.path === value);
                    setDraft((current) => current ? { ...current, path: value, name: file?.name ?? current.name } : current);
                  }}
                />
              </div>
              <label className="settings-field">
                <span>Name</span>
                <input value={draft.name} onChange={(event) => setDraft((current) => current ? { ...current, name: event.target.value } : current)} />
              </label>
              <label className="settings-field form-span-full">
                <span>Notes</span>
                <textarea className="settings-prompt small" value={draft.notes} onChange={(event) => setDraft((current) => current ? { ...current, notes: event.target.value } : current)} />
              </label>
              <div className="button-row form-span-full">
                <button className="button-primary" disabled={pending || !draft.path} type="submit">
                  <AppIcon name={pending ? "spinner" : "plus"} />
                  Add data
                </button>
                <button disabled={pending} onClick={() => setDraft(null)} type="button">Cancel</button>
              </div>
            </div>
          </form>
        </FormDialog>
      ) : null}
    </section>
  );
}

function WorkbookStepsTable({
  detail,
  onAddStep,
  onOpenStep
}: {
  detail: WorkbookDetail;
  onAddStep?: () => void;
  onOpenStep: (stepId: string) => void;
}) {
  if (!detail.steps.length) {
    return (
      <section className="panel workbook-steps-section" aria-label="Workbook steps">
        <div className="section-heading">
          <h2>Steps</h2>
          <div className="workbook-steps-heading-actions">
            <span>0</span>
          </div>
        </div>
        <button className="asset-empty-card workbook-steps-empty-card" onClick={onAddStep} type="button">
          <div className="workbook-steps-empty-card-title">
            <AppIcon name="plus" size={18} />
            <strong>Add a step</strong>
          </div>
          <span>Generate a step using this workbook's data.</span>
        </button>
      </section>
    );
  }

  return (
    <section className="panel workbook-steps-section" aria-label="Workbook steps">
      <div className="section-heading">
        <h2>Steps</h2>
        <div className="workbook-steps-heading-actions">
          <span>{detail.steps.length}</span>
          <button className="button button-table" onClick={onAddStep} type="button">
            <AppIcon name="plus" />
            Add a step
          </button>
        </div>
      </div>
      <div className="table-surface">
        <table className="meta-table workbook-steps-table">
          <thead>
            <tr>
              <th>Step</th>
              <th>Status</th>
              <th>Workbook Data</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            {detail.steps.map((step) => (
              <tr className="table-click-row" key={step.id} onClick={() => onOpenStep(step.id)}>
                <td>{step.title}</td>
                <td>
                  <span className={`table-status-badge ${step.active ? "success" : "inactive"}`}>
                    {step.active ? "Active" : "Inactive"}
                  </span>
                </td>
                <td>{step.input_refs.length ? step.input_refs.join(", ") : "-"}</td>
                <td>{step.prompt || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function WorkbookPanelCard({
  detail,
  panel,
  workspaceId,
  onOpenReport,
  onOpenStep
}: {
  detail: WorkbookDetail;
  panel: PanelSummary;
  workspaceId: string;
  onOpenReport: (report: WorkbookDetail["reports"][number]) => void;
  onOpenStep: (stepId: string) => void;
}) {
  const sourceId = panel.id.split(":").slice(1).join(":");
  const chart = panel.kind === "chart" ? detail.charts.find((candidate) => candidate.id === sourceId) : undefined;
  const report = panel.kind === "report" ? detail.reports.find((candidate) => candidate.id === sourceId) : undefined;
  const check = panel.kind === "check" ? detail.checks.find((candidate) => candidate.id === sourceId) : undefined;
  const step = detail.steps.find((candidate) => candidate.id === panel.step_id);

  return (
    <article className={`workbook-panel-card ${panel.kind}`}>
      <div className="workbook-panel-card-header">
        <h3>{panel.title}</h3>
        <WorkbookPanelMenu
          panel={panel}
          report={report}
          step={step}
          onOpenReport={onOpenReport}
          onOpenStep={onOpenStep}
        />
      </div>
      <div className="workbook-panel-content">
        {chart ? <PlotlyChart figure={chart.figure} /> : null}
        {report ? (
          <div className="workbook-panel-report">
            <HtmlPreview
              className="workbook-panel-report-frame"
              title={report.title}
              url={api.reportFileUrl(workspaceId, report.id)}
            />
            <button className="workbook-panel-open-report" onClick={() => onOpenReport(report)} type="button">
              Open report
            </button>
          </div>
        ) : null}
        {check ? <WorkbookPanelCheck check={check} /> : null}
        {!chart && !report && !check ? <p className="workbook-panel-missing">Panel source is unavailable.</p> : null}
      </div>
    </article>
  );
}

function WorkbookPanelMenu({
  panel,
  report,
  step,
  onOpenReport,
  onOpenStep
}: {
  panel: PanelSummary;
  report?: WorkbookDetail["reports"][number];
  step?: WorkbookStep;
  onOpenReport: (report: WorkbookDetail["reports"][number]) => void;
  onOpenStep: (stepId: string) => void;
}) {
  const hasActions = Boolean(step || report);

  return (
    <Menu.Root>
      <Menu.Trigger
        render={
          <button
            aria-label={`Actions for ${panel.title}`}
            className="button button-icon workbook-panel-menu-trigger"
            title="Panel actions"
            type="button"
          >
            <AppIcon name="more" />
          </button>
        }
      />
      <Menu.Portal>
        <Menu.Positioner align="end" sideOffset={4}>
          <Menu.Popup className="file-tree-menu workbook-panel-menu">
            {step ? (
              <Menu.Item className="file-tree-menu-item" onClick={() => onOpenStep(step.id)}>
                <span>Open script</span>
                <small>{step.title}</small>
              </Menu.Item>
            ) : null}
            {report ? (
              <Menu.Item className="file-tree-menu-item" onClick={() => onOpenReport(report)}>
                <span>Open report</span>
                <small>{report.format}</small>
              </Menu.Item>
            ) : null}
            {!hasActions ? (
              <Menu.Item className="file-tree-menu-item disabled" disabled>
                <span>No actions</span>
              </Menu.Item>
            ) : null}
          </Menu.Popup>
        </Menu.Positioner>
      </Menu.Portal>
    </Menu.Root>
  );
}

function WorkbookPanelCheck({ check }: { check: WorkbookDetail["checks"][number] }) {
  const hasDisplayValue = check.value !== undefined && check.value !== null;

  return (
    <div className="workbook-panel-check">
      <span className={`table-status-badge ${statusKind(check.status)}`}>{check.status}</span>
      <strong>{check.name}</strong>
      {check.message ? <p>{check.message}</p> : null}
      {hasDisplayValue ? (
        <span className="workbook-panel-check-value">
          {String(check.value)}
          {check.unit ? ` ${check.unit}` : ""}
        </span>
      ) : null}
    </div>
  );
}

function WorkbookPanelReportDialog({
  report,
  workspaceId,
  onClose
}: {
  report: WorkbookDetail["reports"][number];
  workspaceId: string;
  onClose: () => void;
}) {
  return (
    <FormDialog className="workbook-report-dialog" title={report.title} onClose={onClose}>
      <HtmlPreview
        className="workbook-report-dialog-frame"
        title={report.title}
        url={api.reportFileUrl(workspaceId, report.id)}
      />
    </FormDialog>
  );
}

function dataSourcesForStep(dataSources: WorkbookDataSource[], step: WorkbookStep): WorkbookDataSource[] {
  const inputRefs = new Set(step.input_refs);
  return dataSources.filter((source) => inputRefs.has(source.id));
}

function compareWorkbooks(a: WorkbookSummary, b: WorkbookSummary, sort: WorkbookSort): number {
  if (sort === "name") return a.title.localeCompare(b.title);
  if (sort === "target") return (a.linked_asset_name ?? a.linked_asset_id ?? "").localeCompare(b.linked_asset_name ?? b.linked_asset_id ?? "");
  if (sort === "status") return (a.latest_execution_status ?? a.status).localeCompare(b.latest_execution_status ?? b.status);
  return dateValue(b.updated_at) - dateValue(a.updated_at) || a.title.localeCompare(b.title);
}

function workbookTileClass(workbook: WorkbookSummary): string {
  const classes = ["asset-tile", "workbook-tile"];
  if (workbook.latest_execution_status === "failed" || workbook.status === "failed") classes.push("needs-data");
  if (!workbook.latest_execution_status) classes.push("no-workbook");
  return classes.join(" ");
}

function templateStepCount(template: WorkbookTemplateSummary | undefined, workbook: WorkbookSummary): number {
  return workbook.step_order.length || template?.steps.length || 0;
}

function formatCount(count: number, label: string): string {
  return `${count} ${label}${count === 1 ? "" : "s"}`;
}

function emptyStepDraft(): StepDraft {
  return { id: "", title: "", prompt: "", inputRefs: "" };
}

function stepAiEditDraft(step: WorkbookStep | null): StepAiEditDraft {
  return { instruction: "", inputRefs: step?.input_refs.join(", ") ?? "" };
}

function hasStepContent(draft: StepDraft): boolean {
  return Boolean(draft.title.trim() || draft.prompt.trim());
}

function hasStepAiEditContent(draft: StepAiEditDraft): boolean {
  return Boolean(draft.instruction.trim());
}

function dateValue(value?: string | null): number {
  if (!value) return 0;
  const parsed = Date.parse(value);
  return Number.isFinite(parsed) ? parsed : 0;
}
