# Arc Design Notes

This is the durable UI context for Arc. Keep it short, practical, and current. If the product direction changes, update this file instead of relying on chat history.

## Design Read

Arc is an operational desktop-style app for physical assets, real-world test runs, workbook review surfaces, local files, reports, charts, and agent work.

The UI should feel closer to Replicate's clean product surfaces than to a marketing SaaS dashboard:

- sparse, table-first, and direct
- strong information hierarchy
- thin dividers and restrained borders
- compact controls
- minimal chrome
- no decorative card-heavy dashboard layouts
- no marketing-page composition inside the app

Raycast is a useful component reference for dark surfaces, compact inputs, badges, and small status treatments, but Arc should not copy Raycast fonts, red brand color, or brand styling.

## Core Principles

- Keep the simplest UI that communicates the state clearly.
- Prefer tables, rows, lists, and dividers over cards.
- Use cards only for repeated visual charts, modals, or genuinely framed tools.
- Avoid nested cards.
- Use square corners everywhere. Do not add rounded corners to controls, panels, cards, messages, menus, or dialogs.
- Avoid large warning panels unless the issue is critical.
- Use icons for statuses where possible, with text only when the surrounding table does not explain the meaning.
- Favor Base UI primitives for menus, dialogs, tabs, selects, checkboxes, and similar interactive controls.
- Keep Base UI wrappers simple and local; do not add a broad component abstraction layer unless repeated UI actually needs it.
- Do not add a layout engine, drag/drop system, or grid library until the simple approach actually breaks.

## Theme Direction

Light mode:

- strong white background
- black primary text
- gray only for subtitles, metadata, secondary labels, and dividers
- avoid warm cream, beige, or washed-out gray
- should feel like crisp white/black Arc dashboard styling

Dark mode:

- near-black canvas
- subtle dark surface stack
- high contrast headings and body text
- borders must be visible enough to scan tables
- semantic colors should be distinctive and bold
- avoid muddy low-contrast workbook screens

Useful dark reference values from the Raycast design reference:

- canvas around `#040506`
- surfaces around `#07080a`, `#111214`, `#1b1c1e`
- compact controls with subtle borders

## Typography

Arc uses a Minor Third type scale from a 15px base:

- `--font-size--2`: 10.42px
- `--font-size--1`: 12.5px
- `--font-size-0`: 15px
- `--font-size-1`: 18px
- `--font-size-2`: 21.6px
- `--font-size-3`: 25.92px
- `--font-size-4`: 31.1px

Do not scale font size with viewport width. Keep headings sized to their context: hero-scale type does not belong inside compact panels or tables.

## Icons

The app uses `@iconify/react` through a small local icon map in `frontend/src/components/AppIcon.tsx`.

Current direction:

- use pixel-style Iconify glyphs lightly across the app
- use active nav icon color as a strong tab signal
- use theme-toggle hover colors: sun gets warm yellow/orange, moon gets blue
- use simple symbolic status icons instead of verbose pills
- use the shared emerald `--color-success` token for all success states; avoid one-off greens

Status icon rules live in `frontend/src/components/StatusIcon.tsx`:

- completed, ready, success: emerald check
- failed, error, invalid: red cross
- running: blue spinner or dot
- queued, pending: muted clock or dot
- inactive, unknown: muted dot

All status icons need `title` and `aria-label`.

## Controls

- Use the shared Base UI-backed `AppSelect` for app dropdowns instead of native selects.
- Dropdowns should be compact and square-cornered.
- Button styling is CSS-only. Use `button` for plain neutral actions, `.button` when a link or label needs button styling, and compose only these variants: `.button-primary`, `.button-secondary`, `.button-danger`, `.button-table`, `.button-icon`, `.button-step`, `.button-link`, `.button-upload`, `.button-run`.
- Run buttons should be a larger icon plus text button using `.button-run`.
- Delete buttons should use a simple red outline, red text, and the trash icon.
- Use icon-only delete buttons where space is tight; use icon plus `Delete` for primary destructive actions.

## Time And Metadata

All user-facing relative time should go through `frontend/src/utils/format.ts`.

Rules:

- under 60 seconds: `25 seconds ago`
- under 1 hour: `12 minutes ago`
- 1 hour to under 24 hours: local time only, like `2:34 PM`
- 1 day or older: date plus time, like `Jun 1, 2:34 PM`

Use this across Assets, Runs, Workbooks, Data, Settings, and any future provenance UI.

## Data UI

Data is a file-first workspace browser:

- left panel: Local and Shared folder/file browser, search, upload
- right panel: selected file table takes the full panel with no inner margin or floating preview card
- selecting a file uses the existing `?file=` deep link
- uploads land in `files/local`; files copied into `files/local` or `files/shared` appear after the page refetches

Big-file rule:

- never load a whole large file into the browser
- use backend paging
- use a native table with sticky header, horizontal scroll, vertical scroll, page controls, and page-size select
- no TanStack Table or Glide Data Grid in the current pass

Current endpoint:

- `GET /api/workspaces/{workspace_id}/files/table?path=...&page=0&page_size=100`

CSV and JSON should page through DuckDB when possible. Text and unknown files get a bounded preview. TDMS keeps the raw file as source of truth, writes a channel manifest, and reads channel samples on demand. TDM waits for real sample files and parser confirmation.

## Assets

Assets are physical things. Systems and components share the same flat card list:

- keep the existing card grid; do not introduce a hierarchy table
- cards show whether the asset is a system or component
- asset detail uses tabs for Overview, Runs, Workbooks, and Components
- a system's Components tab shows its assigned component assets as cards
- a component's Components tab shows live readings, recording controls, channels, and model documentation
- supported component models are integrations, not separate user-facing assets
- asset rows use names first, ids only as metadata

## Runs

Runs are real-world test windows for one asset. They are not execution jobs.

- use the same left/right browser layout
- left pane: run list, newest first
- right pane: selected run detail
- header: run name, asset, start/end time
- sections: Workbooks, Executions, Properties
- data belongs to workbooks as Workbook Data, not to runs

## Workbooks

Workbooks replace dashboards. A workbook is a dashboard plus editable/reusable analysis steps.

- use the same left/right browser layout
- left pane: workbook list
- right pane: selected workbook
- header: title, target asset/run, template, status, Compute button
- body: panels first, then Workbook Data, then steps and executions
- Workbook Data is shown as an inset table of attached files/datasets
- every step is a Python-backed analysis step created from a prompt
- computed steps write outputs under an execution `outputs/` folder
- Arc infers chart/report/check outputs from the files the step writes
- panels show visible chart/report/check outputs
- execution logs stay secondary, below the steps, as plain `pre/code`
- do not add drag/drop layout or dashboard grid sizing yet

## Chat

Chat has its own more atmospheric surface:

- centered conversation with margins on both sides
- do not show a redundant in-page chat title
- keep history and new-chat controls at the bottom right by the composer
- user messages do not show `USER`
- assistant is labeled `Arc Agent`
- send button is an arrow-up circle
- textarea scrollbar should sit above the send button
- background uses a pure blue to black gradient inspired by archelps.com, without muddy purple

## Settings

Settings should stay minimal:

- workspace name
- Arc Agent system prompt

Do not turn Settings into a dumping ground.

## Implementation Pointers

Shared frontend primitives:

- `frontend/src/components/StatusIcon.tsx`
- `frontend/src/components/PaginatedDataTable.tsx`
- `frontend/src/components/AppIcon.tsx`
- `frontend/src/utils/format.ts`
- `frontend/src/styles/app.css`

Backend helpers for current UI direction:

- paged files: `backend/app/core/files.py`, `backend/app/core/duck.py`
- assets: `backend/app/core/assets.py`
- real-world runs: `backend/app/core/real_runs.py`
- workbook templates and workbooks: `backend/app/core/workbooks.py`
- executions, logs, and outputs: `backend/app/core/executions.py`, `backend/app/core/runs.py`, `backend/app/core/control_db.py`
- chart/report output pointers: `backend/app/core/charts.py`, `backend/app/core/reports.py`

When extending the UI, first check whether one of these helpers already exists. Add a shared primitive only when it removes real duplication or clarifies an app-wide rule.
