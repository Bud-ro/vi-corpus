# Arc-TDM (Test Data Management)

## About

Arc is a local-first workspace for hardware and data review. It gives you a web UI for files,
assets, test runs, workbooks, charts, reports, and optional agent-assisted analysis.

The app is designed around one simple idea: keep project artifacts in a visible workspace on disk,
then use the UI as the control layer over that workspace.

Use Arc to upload project data, connect it to assets and test runs, build repeatable Python-backed
workbooks, and keep the resulting workspace versioned with git.

## What You Can Do

- Upload CSV, TSV, JSON, Parquet, TDMS, HTML, and other project files.
- Browse, preview, query, and organize workspace data.
- Track physical assets and time-bounded test runs.
- Build workbooks with editable Python-backed analysis steps.
- Compute workbook steps into durable logs, checks, charts, and reports.
- Commit or discard workspace changes through the UI.
- Use optional Chat when an OpenAI API key is configured.
- Use optional Clerk auth for multi-user hosted deployments.

## Current Shape

Arc is a pre-1.0 application. The core source repo contains the app code and docs. Runtime data is
created locally and ignored by git.

```text
backend/       FastAPI API and workspace logic
frontend/      React, Vite, and TypeScript UI
data/          Local runtime state, created on first run and ignored by git
*.md           Product, architecture, and design notes
```

The main UI routes are Chat, Assets, Workbooks, Data, and Settings.

## Prerequisites

- macOS or Linux
- Python 3.11+
- Node.js 20+ and npm
- Git
- Make, optional but recommended

Chat requires an OpenAI API key. Everything else can run without one.

## Quick Start

From a fresh clone:

```bash
cp .env.example .env
make install
```

Start the backend:

```bash
make dev-api
```

Start the frontend in another terminal:

```bash
make dev-ui
```

Open:

```text
http://localhost:5173
```

The Vite dev server proxies `/api` and `/health` to the FastAPI server on port `8000`.

### First End-to-End Session

Use your own project file, or make a tiny CSV so you can test the full loop right away:

```bash
cat > /tmp/arc-sample.csv <<'CSV'
timestamp,temp_c,current_a
2026-06-01T10:00:00Z,22.1,1.8
2026-06-01T10:01:00Z,23.4,1.9
2026-06-01T10:02:00Z,25.2,2.4
2026-06-01T10:03:00Z,28.0,3.1
CSV
```

Then walk through the app:

1. Open Arc at `http://localhost:5173` and use the default workspace.
2. Go to Data, click Upload, choose the sample CSV or your own file, leave Destination on Local,
   and click Create. Select the uploaded file in the file tree to preview the rows.
3. Go to Assets, click New asset, add a simple asset name, and save it. Open the asset and click
   New Run if you want to capture a specific test window.
4. Go to Workbooks, click New workbook, choose the default workbook template, link the asset you
   just created, and save it.
5. Open the workbook, find Workbook Data, click Add data, and attach the uploaded CSV or dataset.
6. Add or generate a workbook step. A good first step is a small Python analysis that reads the
   workbook data, summarizes row counts and numeric columns, and writes a Plotly chart or HTML
   report under the execution outputs.
7. Click Run workbook. Watch the Executions table for status, open the execution row to see logs,
   and review any checks, charts, or reports that the step produced.
8. Go to Chat if `OPENAI_API_KEY` is set. Try asking: `Inspect the uploaded CSV and suggest a
   useful workbook step.` You can also mention uploaded files from the composer.
9. Use the Git panel to commit or discard workspace changes when the workspace is in a good state.

If `OPENAI_API_KEY` is blank, Chat and AI-generated steps show a missing-key message. Uploads,
assets, runs, workbook editing, and workbook execution still work.

## Manual Setup Without Make

Backend:

```bash
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm ci
npm run dev
```

## Environment

Copy `.env.example` to `.env` before running the app.

```bash
cp .env.example .env
```

All variables are optional for local development unless you need the feature they enable.

| Variable | Used by | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | Backend | Enables Chat and generated workbook steps. |
| `VITE_CLERK_PUBLISHABLE_KEY` | Frontend | Enables Clerk sign-in in the React app. |
| `CLERK_SECRET_KEY` | Backend | Verifies Clerk sessions on API requests. |
| `RESEND_API_KEY` | Backend | Enables email delivery from workbook step code that uses Arc email helpers. |
| `ARC_ALLOWED_ORIGINS` | Backend | Adds comma-separated production frontend origins for CORS. |

If Clerk variables are blank, Arc uses one local development user and one local default workspace.

If `OPENAI_API_KEY` is blank, Chat returns a clear missing-key message, but the rest of the app
continues to work.

## First Run Data

You do not need the local `data/`, `workspace/`, or `workspaces/` folders from another machine.

On first backend startup, Arc creates fresh runtime state:

```text
data/
  var/
    app.sqlite
  workspaces/
    default/
      .git/
      .gitignore
      project.json
      workspace.duckdb
      assets/
      runs/
      workbook_templates/
      workbooks/
      executions/
      charts/
      reports/
      files/
```

Important details:

- `data/` is required while the app is running, but it is generated runtime state.
- Deleting `data/` resets the local app to a fresh empty workspace.
- `data/var/app.sqlite` stores app control state such as users, workspaces, chats, and executions.
- `data/workspaces/<slug>/` stores project artifacts for that workspace.
- Each workspace is also its own git repo.
- Uploaded source files under `files/local/` and `files/shared/` are ignored inside the workspace repo.
- The root repo ignores `data/`, `var/`, `workspace/`, and `workspaces/`.

For open-source publishing, commit the source repo. Do not publish local runtime folders or `.env`.

## Basic Product Loop

1. Open the app and choose the default workspace.
2. Go to Data and upload source files.
3. Create an asset for the physical thing being tested.
4. Create a run when you have a real test window to review.
5. Create a workbook for the asset and attach run-specific data when needed.
6. Attach workbook data.
7. Add or edit workbook steps.
8. Click Run workbook.
9. Review generated logs, checks, charts, and reports.
10. Commit or discard workspace changes from the Git panel.

Workbook steps are normal Python scripts. They run with the backend Python environment and receive:

```text
--workspace   Path to the workspace root
--execution   Path to the current execution directory
--duckdb      Path to the workspace DuckDB database
```

Step outputs are written under the execution directory. Arc recognizes these output shapes:

- `*.figure.json` for Plotly figures
- `*.html` for report previews and downloads
- `outputs/checks/*.json` for check results
- plain logs streamed from stdout and stderr

Charts and reports point back to execution outputs instead of copying them.

## Git Model

Arc has two separate git layers:

1. The root repo versions app source code, docs, config, and tests.
2. Each workspace repo under `data/workspaces/<slug>/` versions that workspace's project artifacts.

This keeps product code separate from user/project data.

The UI can show workspace git status, commit workspace changes, and discard selected workspace
changes. These actions affect the selected workspace repo, not the root Arc source repo.

## Checks

Run the smoke test:

```bash
make smoke
```

Run the full local check:

```bash
make check
```

`make check` runs backend lint, backend tests, and the frontend production build.

Tests should create their own temporary workspaces and runtime state. They should not depend on your
local `data/` folder, uploaded files, or previous runs.

## Component Catalog

The frontend includes a standalone development-only component catalog:

```text
http://localhost:5173/component-library.html
```

It is not linked from the product router or sidebar. The page exists to preview shared React
components and CSS patterns in one place.

Catalog sections:

- Foundations
- Buttons
- Forms
- Icons and status
- Navigation
- Tables
- Dialogs
- Loading and preview states
- Data and files
- Assets and runs
- Workbooks and reports
- Interface examples
- Chat
- Miscellaneous utility patterns

This developer catalog page does not indicate hidden private product components.

## Deployment

A simple hosted setup is:

- one Python web service for the backend
- one static frontend build
- one persistent disk mounted at the repo `data/` path for backend runtime state

Backend service:

```text
Build command: cd backend && python -m pip install -e .
Start command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health check: /health
Persistent disk mount: /path/to/Arc/data
```

Backend environment:

```text
ARC_ALLOWED_ORIGINS=https://your-frontend.example.com
CLERK_SECRET_KEY=your_clerk_secret_key
OPENAI_API_KEY=your_openai_api_key
RESEND_API_KEY=your_resend_api_key
```

Frontend static site:

```text
Root directory: frontend
Build command: npm ci && npm run build
Publish directory: dist
```

Frontend environment:

```text
VITE_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
```

Frontend rewrites:

```text
/api/*  -> https://your-backend.example.com/api/*
/*      -> /index.html
```

For production auth, configure both Clerk variables and add the frontend domain as an allowed
application origin in Clerk.

## Troubleshooting

Backend fails to start:

- Confirm Python is 3.11 or newer.
- Re-run `make install`.
- Check that port `8000` is free.

Frontend cannot reach the API:

- Make sure `make dev-api` is running.
- Open `http://localhost:8000/health`.
- Make sure the frontend is running on `http://localhost:5173`.

Chat does not answer:

- Add `OPENAI_API_KEY` to `.env`.
- Restart the backend.
- Check the Chat response body for the explicit backend error.

You want a fresh local app:

```bash
rm -rf data
make dev-api
```

This removes local runtime state and creates a new empty workspace on startup.

## More Context

- [ARCHITECTURE.md](ARCHITECTURE.md) gives a system map.
- [DESIGN.md](DESIGN.md) captures durable UI direction.
- [LICENSE](LICENSE) contains the license.
