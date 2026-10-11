import React, { useEffect, useMemo, useState } from "react";
import ReactDOM from "react-dom/client";

import type { PlotlyFigure } from "./api/types";
import { ArcLogo } from "./components/ArcLogo";
import { AppIcon, type AppIconName } from "./components/AppIcon";
import { AppSelect } from "./components/AppSelect";
import { BackIconButton } from "./components/BackButton";
import { ConfirmDeleteDialog } from "./components/ConfirmDeleteDialog";
import { FormDialog } from "./components/FormDialog";
import { HtmlPreview } from "./components/HtmlPreview";
import { PageHeader } from "./components/PageHeader";
import { PageLoading } from "./components/PageLoading";
import { PaginatedDataTable } from "./components/PaginatedDataTable";
import { PlotlyChart } from "./components/PlotlyChart";
import { StatusIcon, statusKind } from "./components/StatusIcon";
import { WorkspaceProgressScreen } from "./components/WorkspaceProgressScreen";
import "./styles/app.css";
import "./component-library.css";

const sections = [
  ["foundations", "Foundations"],
  ["buttons", "Buttons"],
  ["forms", "Forms"],
  ["icons-status", "Icons + Status"],
  ["navigation", "Navigation"],
  ["tables", "Tables"],
  ["dialogs", "Dialogs"],
  ["loading-preview", "Loading + Preview"],
  ["data-files", "Data + Files"],
  ["assets-runs", "Assets + Runs"],
  ["workbooks-reports", "Workbooks + Reports"],
  ["chat", "Chat"],
  ["misc", "Misc"]
] as const;

const iconNames = [
  "arrowDown",
  "arrowUp",
  "chat",
  "check",
  "chevronDown",
  "chevronLeft",
  "chevronRight",
  "clock",
  "copy",
  "cross",
  "dashboard",
  "data",
  "dot",
  "edit",
  "file",
  "folder",
  "gitBranch",
  "gitCommit",
  "home",
  "moon",
  "more",
  "play",
  "plus",
  "refresh",
  "reports",
  "review",
  "save",
  "search",
  "send",
  "settings",
  "spinner",
  "steps",
  "sun",
  "trash",
  "undo",
  "upload",
  "charts"
] satisfies AppIconName[];

const tableRows = [
  {
    run_id: "run_2026_06_14_a",
    asset: "Vibration bench",
    status: "completed",
    peak_g: 14.8,
    updated: "Jun 14, 10:42 AM"
  },
  {
    run_id: "run_2026_06_14_b",
    asset: "Thermal chamber",
    status: "running",
    peak_g: 3.2,
    updated: "Jun 14, 11:04 AM"
  },
  {
    run_id: "run_2026_06_13_c",
    asset: "Prototype enclosure",
    status: "failed",
    peak_g: null,
    updated: "Jun 13, 4:18 PM"
  }
];

const previewHtml = encodeURIComponent(`
  <!doctype html>
  <html>
    <body style="font-family: Inter, system-ui, sans-serif; margin: 0; padding: 20px; color: #111;">
      <h1 style="font-size: 22px; margin: 0 0 10px;">Report preview</h1>
      <p style="line-height: 1.5; margin: 0 0 14px;">This frame uses the real HtmlPreview component.</p>
      <table style="border-collapse: collapse; width: 100%; font-size: 13px;">
        <tr><th style="border-bottom: 1px solid #ddd; text-align: left; padding: 8px;">Metric</th><th style="border-bottom: 1px solid #ddd; text-align: left; padding: 8px;">Value</th></tr>
        <tr><td style="border-bottom: 1px solid #eee; padding: 8px;">Status</td><td style="border-bottom: 1px solid #eee; padding: 8px;">Ready</td></tr>
        <tr><td style="border-bottom: 1px solid #eee; padding: 8px;">Rows</td><td style="border-bottom: 1px solid #eee; padding: 8px;">2,408</td></tr>
      </table>
    </body>
  </html>
`);

const plotFigure: PlotlyFigure = {
  data: [
    {
      x: ["Baseline", "Run A", "Run B", "Run C"],
      y: [8.2, 11.4, 9.7, 14.8],
      type: "bar",
      name: "Peak g"
    }
  ],
  layout: {
    height: 300,
    margin: { t: 20, r: 12, b: 36, l: 42 },
    xaxis: { title: "Run" },
    yaxis: { title: "Peak g" }
  }
};

function ComponentLibrary() {
  const [theme, setTheme] = useState<"light" | "dark">("light");
  const [selectValue, setSelectValue] = useState("ready");
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [confirmDialogOpen, setConfirmDialogOpen] = useState(false);
  const tableColumns = useMemo(() => ["run_id", "asset", "status", "peak_g", "updated"], []);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  return (
    <div className="component-library">
      {formDialogOpen ? (
        <FormDialog title="Create asset" onClose={() => setFormDialogOpen(false)}>
          <div className="workspace-create-form">
            <label className="workspace-create-field">
              <span>Name</span>
              <input defaultValue="Thermal chamber" />
            </label>
            <label className="workspace-create-field">
              <span>Asset ID</span>
              <input defaultValue="asset_thermal_chamber" />
            </label>
            <div className="workspace-create-actions">
              <button type="button" onClick={() => setFormDialogOpen(false)}>
                Cancel
              </button>
              <button className="button button-primary" type="button" onClick={() => setFormDialogOpen(false)}>
                <AppIcon name="save" />
                Save
              </button>
            </div>
          </div>
        </FormDialog>
      ) : null}
      {confirmDialogOpen ? (
        <ConfirmDeleteDialog
          title="Delete report?"
          onCancel={() => setConfirmDialogOpen(false)}
          onConfirm={() => setConfirmDialogOpen(false)}
        >
          <div className="delete-copy">
            <p>This shows the real ConfirmDeleteDialog component with app dialog styling.</p>
            <div className="danger-note">
              <p>Use this treatment for destructive confirmation only.</p>
            </div>
          </div>
        </ConfirmDeleteDialog>
      ) : null}

      <div className="library-shell">
        <aside className="library-sidebar">
          <div className="brand-copy">
            <ArcLogo />
          </div>
          <div>
            <h1>Component Library</h1>
            <p>Internal-only catalog for shared React components and app CSS patterns.</p>
          </div>
          <button
            className="button button-icon theme-toggle"
            data-theme-mode={theme === "dark" ? "dark" : "light"}
            type="button"
            title="Toggle theme"
            aria-label="Toggle theme"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          >
            <AppIcon name={theme === "dark" ? "sun" : "moon"} />
          </button>
          <nav aria-label="Component sections">
            {sections.map(([id, label]) => (
              <a href={`#${id}`} key={id}>
                {label}
              </a>
            ))}
          </nav>
        </aside>

        <main className="library-main">
          <section className="library-hero">
            <div className="eyebrow">Internal dev view</div>
            <h1>Arc Component Library</h1>
            <p>
              This page is not wired into the product router or sidebar. It is a standalone Vite entry that imports the
              real app CSS and the safe-to-mount shared React components, with static examples for backend-bound screen
              patterns.
            </p>
            <p className="library-note">
              Open directly at <code>/component-library.html</code> while the frontend dev server is running.
            </p>
          </section>

          <LibrarySection
            id="foundations"
            title="Foundations"
            description="Theme tokens, typography, basic panels, metadata, and the square-corner visual rule."
          >
            <div className="library-grid">
              <Example title="Type scale" note="Global h1, h2, paragraph, eyebrow, muted, and code treatments.">
                <div className="library-stack vertical">
                  <div className="eyebrow">WORKBOOK / RUN</div>
                  <h1>Page title</h1>
                  <h2>Section heading</h2>
                  <p>Body copy keeps the app direct and readable.</p>
                  <span className="muted">Muted metadata text</span>
                  <code>workspace/output/report.html</code>
                </div>
              </Example>
              <Example title="Color tokens" note="The app intentionally stays mostly black, white, and gray.">
                <div className="library-color-grid">
                  <Token name="--color-bg" color="var(--color-bg)" />
                  <Token name="--color-panel-soft" color="var(--color-panel-soft)" />
                  <Token name="--color-control" color="var(--color-control)" />
                  <Token name="--color-border" color="var(--color-border)" />
                  <Token name="--color-success" color="var(--color-success)" />
                  <Token name="--color-danger" color="var(--color-danger)" />
                  <Token name="--color-running" color="var(--color-running)" />
                  <Token name="--color-warning" color="var(--color-warning)" />
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="buttons" title="Buttons" description="CSS-only button variants used across the app.">
            <div className="library-grid">
              <Example title="Core buttons" note="Use plain button first, then add variants only when meaning changes.">
                <div className="library-stack">
                  <button type="button">Default</button>
                  <button className="button button-secondary" type="button">
                    Secondary
                  </button>
                  <button className="button button-primary" type="button">
                    <AppIcon name="save" />
                    Primary
                  </button>
                  <button className="button button-danger" type="button">
                    <AppIcon name="trash" />
                    Delete
                  </button>
                  <button className="button button-link" type="button">
                    Link button
                  </button>
                </div>
              </Example>
              <Example title="Icon and run actions" note="The run button is intentionally larger and heavier.">
                <div className="library-stack">
                  <BackIconButton />
                  <button className="button button-icon" type="button" title="Refresh">
                    <AppIcon name="refresh" />
                  </button>
                  <button className="button button-table" type="button">
                    <AppIcon name="review" />
                    Review
                  </button>
                  <button className="button button-run" type="button">
                    <AppIcon name="play" size={18} />
                    Compute
                  </button>
                </div>
              </Example>
              <Example title="Disabled and block states" note="Shared disabled opacity and full-width action.">
                <div className="library-stack vertical">
                  <button disabled type="button">
                    Disabled
                  </button>
                  <button className="button button-primary button-block" type="button">
                    Full width primary
                  </button>
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="forms" title="Forms" description="Inputs, selects, segmented controls, sliders, chips, and form grids.">
            <div className="library-grid">
              <Example title="Inputs" note="Use simple labels and direct field layouts.">
                <div className="settings-panel">
                  <label className="settings-field">
                    <span>Workspace name</span>
                    <input defaultValue="Arc Lab" />
                  </label>
                  <label className="settings-field">
                    <span>System prompt</span>
                    <textarea className="settings-prompt small" defaultValue="Keep analysis grounded in source files." />
                  </label>
                </div>
              </Example>
              <Example title="AppSelect" note="Real Base UI-backed AppSelect component.">
                <div className="library-stack">
                  <AppSelect
                    ariaLabel="Status"
                    value={selectValue}
                    onValueChange={setSelectValue}
                    options={[
                      { label: "Draft", value: "draft" },
                      { label: "Ready", value: "ready" },
                      { label: "Computing", value: "computing" },
                      { label: "Archived", value: "archived", disabled: true }
                    ]}
                  />
                  <AppSelect
                    ariaLabel="Loading select"
                    isLoading
                    value=""
                    onValueChange={() => undefined}
                    options={[]}
                  />
                </div>
              </Example>
              <Example title="Segmented + upload" note="Current data upload and segmented control styling.">
                <div className="library-stack vertical">
                  <div className="segmented-control">
                    <button className="active" type="button">
                      Local
                    </button>
                    <button type="button">Shared</button>
                  </div>
                  <label className="button button-upload">
                    <AppIcon name="upload" />
                    Upload file
                    <input type="file" />
                  </label>
                </div>
              </Example>
              <Example title="Labels and chips" note="Asset tag editor and reusable mono chips.">
                <div className="asset-label-editor">
                  <span className="asset-label-chip">
                    thermal
                    <AppIcon name="cross" size={12} />
                  </span>
                  <span className="asset-label-chip">prototype</span>
                  <input placeholder="Add label" />
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="icons-status" title="Icons + Status" description="The Iconify-backed AppIcon map and status treatments.">
            <div className="library-grid wide">
              <Example title="AppIcon map" note="Real AppIcon component for every icon name currently exported.">
                <div className="library-icon-grid">
                  {iconNames.map((name) => (
                    <div className="library-icon-cell" key={name}>
                      <AppIcon name={name} />
                      <span>{name}</span>
                    </div>
                  ))}
                </div>
              </Example>
              <Example title="StatusIcon" note="Real StatusIcon component and statusKind mapping.">
                <div className="library-stack">
                  {["completed", "failed", "running", "queued", "inactive", "unknown"].map((status) => (
                    <span className="table-leading-cell" key={status}>
                      <StatusIcon status={status} />
                      {status} / {statusKind(status)}
                    </span>
                  ))}
                </div>
              </Example>
              <Example title="Status badges" note="Table and compact status variants.">
                <div className="library-stack">
                  {["success", "error", "running", "pending", "inactive"].map((kind) => (
                    <span className={`table-status-badge ${kind}`} key={kind}>
                      {kind}
                    </span>
                  ))}
                  <span className="table-status-badge success">current</span>
                  <span className="status-pill failed">failed</span>
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="navigation" title="Navigation" description="Sidebar, active nav rows, quick actions, breadcrumbs, and page headers.">
            <div className="library-grid">
              <Example title="PageHeader" note="Real shared PageHeader component.">
                <PageHeader
                  eyebrow="Workspace"
                  title="Assets"
                  actions={
                    <>
                      <button type="button">
                        <AppIcon name="refresh" />
                        Refresh
                      </button>
                      <button className="button button-primary" type="button">
                        <AppIcon name="plus" />
                        New
                      </button>
                    </>
                  }
                />
              </Example>
              <Example title="Sidebar nav" note="Same classes used by the app shell; not wired to the router here.">
                <div className="library-nav-preview">
                  <nav className="nav">
                    <div className="nav-link-row has-quick-action">
                      <a className="nav-link active" data-accent="blue" href="#navigation">
                        <span className="nav-link-main">
                          <AppIcon name="chat" />
                          <span className="nav-label">Chat</span>
                        </span>
                      </a>
                      <button className="nav-quick-action" type="button" title="New chat">
                        <AppIcon name="plus" size={14} />
                      </button>
                    </div>
                    <div className="nav-link-row">
                      <a className="nav-link" href="#navigation">
                        <span className="nav-link-main">
                          <AppIcon name="dashboard" />
                          <span className="nav-label">Assets</span>
                        </span>
                      </a>
                    </div>
                    <div className="nav-link-row">
                      <a className="nav-link active" data-accent="green" href="#navigation">
                        <span className="nav-link-main">
                          <AppIcon name="data" />
                          <span className="nav-label">Data</span>
                        </span>
                      </a>
                    </div>
                  </nav>
                </div>
              </Example>
              <Example title="Breadcrumbs" note="Asset detail breadcrumb treatment.">
                <div className="asset-breadcrumbs">
                  <a href="#navigation">Assets</a>
                  <AppIcon name="chevronRight" size={13} />
                  <span>thermal_chamber</span>
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="tables" title="Tables" description="Native table, metadata table, paginated table, and table actions.">
            <div className="library-grid wide">
              <Example title="PaginatedDataTable" note="Real shared PaginatedDataTable component with AppSelect pager.">
                <PaginatedDataTable
                  columns={tableColumns}
                  rows={tableRows}
                  page={0}
                  pageSize={100}
                  hasNext
                  onPageChange={() => undefined}
                  onPageSizeChange={() => undefined}
                  onRowClick={() => undefined}
                />
              </Example>
              <Example title="Meta table" note="Static table surface used for compact summaries and workbook data.">
                <div className="table-surface">
                  <table className="meta-table">
                    <thead>
                      <tr>
                        <th>Output</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>
                          <strong>response_curve.html</strong>
                          <span className="muted">Report output</span>
                        </td>
                        <td>
                          <span className="table-status-badge success">ready</span>
                        </td>
                        <td>
                          <div className="table-actions">
                            <a href="#tables">Open</a>
                            <button className="button button-icon" type="button">
                              <AppIcon name="trash" />
                            </button>
                          </div>
                        </td>
                      </tr>
                      <tr>
                        <td>
                          <strong>checks.json</strong>
                          <span className="muted">Check output</span>
                        </td>
                        <td>
                          <span className="table-status-badge pending">queued</span>
                        </td>
                        <td>
                          <div className="table-actions">
                            <a href="#tables">Open</a>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="dialogs" title="Dialogs" description="Real dialog components plus specialized dialog class shapes.">
            <div className="library-grid">
              <Example title="FormDialog" note="Click to open the real FormDialog component.">
                <button type="button" onClick={() => setFormDialogOpen(true)}>
                  Open form dialog
                </button>
              </Example>
              <Example title="ConfirmDeleteDialog" note="Click to open the real destructive confirmation component.">
                <button className="button button-danger" type="button" onClick={() => setConfirmDialogOpen(true)}>
                  <AppIcon name="trash" />
                  Open delete dialog
                </button>
              </Example>
              <Example title="Inline errors and notes" note="Common error and destructive copy treatments.">
                <div className="library-stack vertical">
                  <p className="inline-error">
                    <AppIcon name="cross" />
                    Could not save workspace settings.
                  </p>
                  <div className="danger-note">
                    <p>Destructive actions should explain exactly what will be removed.</p>
                  </div>
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="loading-preview" title="Loading + Preview" description="Loading states, progress screen, charts, and HTML previews.">
            <div className="library-grid">
              <Example title="PageLoading" note="Real PageLoading component, constrained inside a preview box.">
                <div className="library-loading-preview">
                  <PageLoading label="Loading component library preview" />
                </div>
              </Example>
              <Example title="WorkspaceProgressScreen" note="Real workspace boot/progress component.">
                <div className="library-start-preview">
                  <WorkspaceProgressScreen />
                </div>
              </Example>
              <Example title="HtmlPreview" note="Real iframe wrapper component.">
                <div className="library-iframe-preview">
                  <HtmlPreview title="Report preview" url={`data:text/html;charset=utf-8,${previewHtml}`} />
                </div>
              </Example>
              <Example title="PlotlyChart" note="Real PlotlyChart component with app theme palette.">
                <div className="library-chart-preview">
                  <PlotlyChart figure={plotFigure} />
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="data-files" title="Data + Files" description="Data browser, file tree, dropzone, preview title, and text preview patterns.">
            <div className="library-grid wide">
              <Example title="Data browser shell" note="Representative left/right browser pattern used by Data and Workflows.">
                <div className="data-page library-data-preview">
                  <div className="data-browser">
                    <section className="data-pane source-file-pane">
                      <div className="pane-toolbar">
                        <div className="pane-title">
                          <span>Files</span>
                          <strong>3</strong>
                        </div>
                      </div>
                      <label className="search-field">
                        <AppIcon name="search" />
                        <input placeholder="Search files" />
                      </label>
                      <div className="file-tree-title">Local</div>
                      <div className="file-tree">
                        <div className="file-tree-row folder">
                          <button className="file-tree-folder-main" type="button">
                            <AppIcon name="chevronDown" />
                            <span>files/local</span>
                          </button>
                          <button className="file-tree-folder-menu" type="button">
                            <AppIcon name="more" size={14} />
                          </button>
                        </div>
                        <div className="file-tree-row file active">
                          <button className="file-tree-row-main" type="button">
                            <AppIcon name="file" />
                            <span>thermal_run.csv</span>
                          </button>
                          <div className="file-tree-row-trailing">
                            <small>2.4 MB</small>
                            <button className="file-tree-delete" type="button">
                              <AppIcon name="trash" size={13} />
                            </button>
                          </div>
                        </div>
                        <div className="file-tree-row dataset striped">
                          <button className="file-tree-row-main" type="button">
                            <AppIcon name="data" />
                            <span>tdms_channels</span>
                          </button>
                          <div className="file-tree-row-trailing">
                            <small>12</small>
                          </div>
                        </div>
                      </div>
                    </section>
                    <section className="data-pane preview-pane has-selection">
                      <div className="table-title">
                        <BackIconButton className="table-title-back" />
                        <div className="table-title-copy">
                          <strong>thermal_run.csv</strong>
                          <span>CSV / 2,408 rows</span>
                        </div>
                      </div>
                      <PaginatedDataTable
                        columns={tableColumns}
                        rows={tableRows}
                        page={0}
                        pageSize={100}
                        hasNext={false}
                        onPageChange={() => undefined}
                        onPageSizeChange={() => undefined}
                      />
                    </section>
                  </div>
                </div>
              </Example>
              <div className="library-grid">
                <Example title="Dropzone" note="Data upload dropzone and review row.">
                  <div className="data-upload-page">
                    <button className="data-dropzone" type="button">
                      <AppIcon name="upload" size={28} />
                      <span>Drop files here or click to upload</span>
                    </button>
                    <div className="data-wizard-review">
                      <div>
                        <strong>thermal_run.csv</strong>
                        <span>files/local/thermal_run.csv</span>
                      </div>
                      <button type="button">Import</button>
                    </div>
                  </div>
                </Example>
                <Example title="Text preview" note="Source file and log text preview treatment.">
                  <pre className="text-preview inline">{`time,temp_c,pressure_kpa\n0,20.1,101.2\n1,20.6,101.3\n2,21.4,101.2`}</pre>
                </Example>
              </div>
            </div>
          </LibrarySection>

          <LibrarySection id="assets-runs" title="Assets + Runs" description="Asset tiles, metrics, status chips, run cards, and detail grids.">
            <div className="library-grid wide">
              <Example title="Asset toolbar and metrics" note="Current asset page top-of-screen pattern.">
                <div className="assets-toolbar">
                  <div className="assets-titlebar">
                    <div className="assets-title-group">
                      <h1>Assets</h1>
                      <div className="assets-tabs">
                        <button className="active" type="button">
                          Assets
                        </button>
                        <button type="button">Runs</button>
                      </div>
                    </div>
                    <button className="button button-primary" type="button">
                      <AppIcon name="plus" />
                      New asset
                    </button>
                  </div>
                  <div className="assets-controlbar">
                    <label className="assets-search">
                      <AppIcon name="search" />
                      <input placeholder="Search assets" />
                    </label>
                    <div className="assets-sort">
                      <span>Sort</span>
                      <select defaultValue="updated">
                        <option value="updated">Updated</option>
                        <option value="name">Name</option>
                      </select>
                    </div>
                  </div>
                  <div className="asset-metric-grid">
                    <div className="asset-metric-tile">
                      <span>Assets</span>
                      <strong>12</strong>
                      <small>3 need data</small>
                    </div>
                    <div className="asset-metric-tile">
                      <span>Runs</span>
                      <strong>48</strong>
                      <small>6 this week</small>
                    </div>
                  </div>
                </div>
              </Example>
              <Example title="Asset tiles" note="Active, needs-data, archived, and empty states.">
                <div className="asset-tile-grid">
                  <button className="asset-tile active" type="button">
                    <div className="asset-tile-header">
                      <div>
                        <span className="asset-icon">
                          <AppIcon name="dashboard" />
                        </span>
                        <h2>Thermal chamber</h2>
                      </div>
                      <span className="asset-status active">active</span>
                    </div>
                    <div className="asset-chip-row">
                      <span>thermal</span>
                      <span>prototype</span>
                    </div>
                    <div className="asset-tile-body">
                      <p>
                        <span>Runs</span>
                        <strong>18</strong>
                      </p>
                      <p>
                        <span>Updated</span>
                        <strong>Jun 14, 10:42 AM</strong>
                      </p>
                    </div>
                  </button>
                  <button className="asset-tile needs-data" type="button">
                    <div className="asset-tile-header">
                      <div>
                        <span className="asset-icon">
                          <AppIcon name="dashboard" />
                        </span>
                        <h2>Load cell rig</h2>
                      </div>
                      <span className="asset-status needs-data">needs data</span>
                    </div>
                    <div className="asset-card-meta">
                      <span>No workbook data</span>
                      <span>0 runs</span>
                    </div>
                  </button>
                  <div className="asset-empty-card is-static">
                    <AppIcon name="plus" />
                    <strong>No assets yet</strong>
                    <span>Create an asset to connect runs, workbooks, and local files.</span>
                  </div>
                </div>
              </Example>
              <Example title="Run card and terminal" note="Expandable run card, logs, terminal, and summary grid.">
                <div className="run-card expanded">
                  <button className="run-card-header" type="button">
                    <span className="run-card-toggle">-</span>
                    <span className="run-card-title">
                      <strong>Thermal soak run</strong>
                      <span>Thermal chamber / Jun 14, 9:00 AM</span>
                    </span>
                    <span className="status-pill completed">completed</span>
                  </button>
                  <div className="run-card-body">
                    <div className="run-summary-grid">
                      <div>
                        <span>Duration</span>
                        <strong>2h 14m</strong>
                      </div>
                      <div>
                        <span>Executions</span>
                        <strong>3</strong>
                      </div>
                      <div>
                        <span>Checks</span>
                        <strong>2 pass / 1 warn</strong>
                      </div>
                    </div>
                    <div className="event-log">
                      <div className="event">
                        <span>09:00:00</span>
                        <p>Started run capture.</p>
                      </div>
                      <div className="event error">
                        <span>09:42:13</span>
                        <p>Sensor spike exceeded warning threshold.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="workbooks-reports" title="Workbooks + Reports" description="Workbook header, tabs, steps, panel grid, reports, checks, and script dialog code styling.">
            <div className="library-grid wide">
              <Example title="Workbook detail" note="Header, tabs, panel cards, and workbook step workspace.">
                <div className="workbook-detail-page">
                  <header className="workbook-detail-header">
                    <div className="workbook-detail-title">
                      <BackIconButton />
                      <div>
                        <div className="eyebrow">THERMAL CHAMBER</div>
                        <h1>Thermal response workbook</h1>
                      </div>
                    </div>
                    <button className="button button-run" type="button">
                      <AppIcon name="play" />
                      Compute
                    </button>
                  </header>
                  <div className="workbook-detail-tabs">
                    <button className="active" type="button">
                      Panels
                    </button>
                    <button type="button">Data</button>
                    <button type="button">Steps</button>
                    <button type="button">Executions</button>
                  </div>
                  <div className="workbook-panel-grid">
                    <div className="workbook-panel-card">
                      <div className="workbook-panel-card-header">
                        <h3>Peak response</h3>
                        <button className="workbook-panel-menu-trigger" type="button">
                          <AppIcon name="more" />
                        </button>
                      </div>
                      <div className="workbook-panel-content">
                        <PlotlyChart figure={plotFigure} />
                      </div>
                    </div>
                    <div className="workbook-panel-card">
                      <div className="workbook-panel-card-header">
                        <h3>Check result</h3>
                        <StatusIcon status="success" />
                      </div>
                      <div className="workbook-panel-check">
                        <strong>Pass: peak vibration below threshold</strong>
                        <p>Peak g stayed below the configured warning threshold for this asset.</p>
                        <span className="workbook-panel-check-value">14.8 g / threshold 18 g</span>
                      </div>
                    </div>
                  </div>
                </div>
              </Example>
              <Example title="Workbook steps" note="Step rail, detail metadata, data chips, and panel chips.">
                <div className="workbook-step-workspace">
                  <aside className="workbook-step-rail">
                    <div className="section-heading">
                      <h2>Steps</h2>
                      <span>3</span>
                    </div>
                    <div className="workbook-step-list">
                      <button className="workbook-step-row active" type="button">
                        <span className="workbook-step-index">01</span>
                        <span className="workbook-step-row-main">
                          <strong>Load channels</strong>
                          <span>Python analysis step</span>
                        </span>
                      </button>
                      <button className="workbook-step-row" type="button">
                        <span className="workbook-step-index">02</span>
                        <span className="workbook-step-row-main">
                          <strong>Compute response</strong>
                          <span>Creates chart output</span>
                        </span>
                      </button>
                    </div>
                  </aside>
                  <main className="workbook-step-detail">
                    <header className="workbook-step-detail-header">
                      <div>
                        <h2>Load channels</h2>
                        <div className="workbook-step-data-link-row">
                          <a className="workbook-step-data-link" href="#workbooks-reports">
                            thermal_run.csv
                          </a>
                          <a className="workbook-step-data-link" href="#workbooks-reports">
                            asset_limits.json
                          </a>
                        </div>
                      </div>
                      <button type="button">
                        <AppIcon name="edit" />
                        Edit
                      </button>
                    </header>
                    <div className="workbook-step-meta">
                      <p>
                        <span>Entrypoint</span>
                        <strong>steps/load_channels.py</strong>
                      </p>
                      <p>
                        <span>Status</span>
                        <strong>Active</strong>
                      </p>
                    </div>
                    <div className="workbook-step-panel-list">
                      <span className="workbook-panel-chip">
                        <AppIcon name="charts" />
                        <strong>chart</strong>
                        response_curve
                      </span>
                      <span className="workbook-panel-chip">
                        <AppIcon name="reports" />
                        <strong>report</strong>
                        summary
                      </span>
                    </div>
                  </main>
                </div>
              </Example>
              <Example title="Report cards and code" note="Report list cards and script/code preview treatments.">
                <div className="library-two-up">
                  <div className="report-list">
                    <button className="report-card report-card-previewable" type="button">
                      <span className="report-card-main">
                        <strong>Thermal response report</strong>
                        <span className="report-card-meta">
                          <span>
                            <AppIcon name="reports" />
                            HTML
                          </span>
                          <span>Jun 14, 11:08 AM</span>
                        </span>
                      </span>
                      <span className="report-card-actions">
                        <span className="button button-table">Open</span>
                      </span>
                    </button>
                  </div>
                  <pre className="step-script-code">
                    <code>{`def run(inputs, outputs):\n    frame = load_csv(inputs["thermal_run"])\n    chart = build_response_chart(frame)\n    chart.write_html(outputs / "response.html")`}</code>
                  </pre>
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="chat" title="Chat" description="Chat has its own atmospheric surface, message cards, markdown, activity, files, and composer.">
            <div className="library-grid wide">
              <Example title="Chat surface" note="Representative chat classes in the blue/black surface.">
                <div className="library-chat-preview">
                  <div className="messages">
                    <div className="message user">
                      <p>Can you inspect the latest workbook output?</p>
                      <div className="chat-user-attachments">
                        <div className="chat-user-attachment">
                          <AppIcon name="file" />
                          <span className="chat-user-attachment-name">response.html</span>
                          <span className="chat-user-attachment-path">outputs/response.html</span>
                        </div>
                      </div>
                    </div>
                    <div className="message assistant">
                      <span>Arc Agent</span>
                      <div className="chat-markdown">
                        <p>The output is ready. Peak response stayed below the threshold.</p>
                        <pre>
                          <code>{`peak_g = 14.8\nthreshold = 18.0`}</code>
                        </pre>
                        <blockquote>One warning came from a short sensor spike.</blockquote>
                      </div>
                      <details className="chat-activity" open>
                        <summary>
                          <span className="chat-activity-title">Activity</span>
                          <span className="chat-activity-summary">2 steps</span>
                        </summary>
                        <div className="chat-activity-list">
                          <div className="chat-activity-item">
                            <AppIcon name="check" size={13} />
                            <span className="chat-activity-label">Read report</span>
                            <span className="chat-activity-detail">outputs/response.html</span>
                          </div>
                          <div className="chat-activity-item error">
                            <AppIcon name="cross" size={13} />
                            <span className="chat-activity-label">Check warning</span>
                            <span className="chat-activity-detail">Transient threshold spike</span>
                          </div>
                        </div>
                      </details>
                    </div>
                  </div>
                  <div className="chat-suggestion-chips">
                    <button className="button chat-suggestion-chip" type="button">
                      <AppIcon name="charts" />
                      Summarize charts
                    </button>
                    <button className="button chat-suggestion-chip" type="button">
                      <AppIcon name="data" />
                      Attach data
                    </button>
                  </div>
                  <div className="composer library-composer-preview">
                    <div className="composer-attachments">
                      <div className="composer-attachment ready">
                        <AppIcon className="composer-attachment-icon" name="file" />
                        <span className="composer-attachment-name">thermal_run.csv</span>
                        <span className="composer-attachment-meta">ready</span>
                        <button className="composer-attachment-remove" type="button">
                          <AppIcon name="cross" size={13} />
                        </button>
                      </div>
                    </div>
                    <textarea placeholder="Ask Arc..." defaultValue="Compare this with the previous run." />
                    <button className="button button-icon composer-upload-button" type="button">
                      <AppIcon name="upload" />
                    </button>
                    <button className="button button-icon send-button" type="button">
                      <AppIcon name="arrowUp" />
                    </button>
                  </div>
                </div>
              </Example>
            </div>
          </LibrarySection>

          <LibrarySection id="misc" title="Misc" description="Git panel shape, terminal logs, file cards, empty states, and utility classes.">
            <div className="library-grid">
              <Example title="GitStatusPanel shape" note="The real GitStatusPanel is backend-bound, so this mirrors its class structure.">
                <section className="panel compact">
                  <div className="panel-title">
                    <span>Workspace git</span>
                    <button className="button button-icon" type="button" title="Refresh status">
                      <AppIcon name="refresh" />
                    </button>
                  </div>
                  <div className="meta-row">
                    <span>Branch</span>
                    <strong>main</strong>
                  </div>
                  <div className="status-list">
                    <code>M frontend/src/component-library.tsx</code>
                    <code>?? frontend/component-library.html</code>
                  </div>
                  <div className="commit-row">
                    <input defaultValue="Update workspace" />
                    <button type="button">
                      <AppIcon name="gitCommit" />
                      Commit
                    </button>
                  </div>
                  <button className="button button-secondary button-block git-discard-action" type="button">
                    <AppIcon name="undo" />
                    Discard tracked
                  </button>
                </section>
              </Example>
              <Example title="Terminal" note="Run terminal and log output styling.">
                <div className="run-terminal">
                  <div className="terminal-titlebar">
                    <div className="terminal-dots">
                      <span />
                      <span />
                      <span />
                    </div>
                    <strong>Execution output</strong>
                    <span>run_014</span>
                  </div>
                  <div className="terminal-body">
                    <div className="terminal-line command">
                      <span className="terminal-prompt">$</span>
                      <span>python steps/compute_response.py</span>
                    </div>
                    <div className="terminal-line">
                      <span className="terminal-step">load_data</span>
                      <span>Loaded 2,408 rows.</span>
                    </div>
                    <div className="terminal-line success">
                      <span className="terminal-prompt">ok</span>
                      <span>Wrote outputs/response.html.</span>
                    </div>
                  </div>
                </div>
              </Example>
              <Example title="Chat file card" note="Reusable file inspection card inside chat messages.">
                <div className="chat-file-card">
                  <details open>
                    <summary>
                      <span className="chat-file-title">analysis.py</span>
                      <span className="chat-file-path">workbooks/thermal/steps/analysis.py</span>
                    </summary>
                    <div className="chat-file-meta">
                      <span>Python</span>
                      <span>1.8 KB</span>
                    </div>
                    <pre className="chat-file-code">{`def compute(frame):\n    return frame["peak_g"].max()`}</pre>
                  </details>
                </div>
              </Example>
              <Example title="Empty states" note="Shared asset empty card and generic empty preview.">
                <div className="library-stack vertical">
                  <div className="empty-preview">
                    <AppIcon name="file" />
                    <p>Select a file to preview its rows.</p>
                  </div>
                  <div className="asset-empty-card is-static">
                    <AppIcon name="steps" />
                    <strong>No executions</strong>
                    <span>Executions appear after a workbook runs.</span>
                  </div>
                </div>
              </Example>
            </div>
          </LibrarySection>
        </main>
      </div>
    </div>
  );
}

function LibrarySection({
  children,
  description,
  id,
  title
}: {
  children: React.ReactNode;
  description: string;
  id: string;
  title: string;
}) {
  return (
    <section className="library-section" id={id}>
      <div className="library-section-header">
        <h2>{title}</h2>
        <p>{description}</p>
      </div>
      {children}
    </section>
  );
}

function Example({ children, note, title }: { children: React.ReactNode; note: string; title: string }) {
  return (
    <div className="library-example">
      <div className="library-example-header">
        <strong>{title}</strong>
        <span>{note}</span>
      </div>
      {children}
    </div>
  );
}

function Token({ color, name }: { color: string; name: string }) {
  return (
    <div className="library-token">
      <div className="library-token-swatch" style={{ background: color }} />
      <code>{name}</code>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("component-library-root")!).render(
  <React.StrictMode>
    <ComponentLibrary />
  </React.StrictMode>
);
