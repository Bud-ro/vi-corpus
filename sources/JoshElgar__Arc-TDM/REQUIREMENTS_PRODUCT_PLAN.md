# Git-Native Engineering Requirements Product

## Purpose of this document

This is the product and architecture brief for a new, standalone engineering requirements and traceability product.

The new product should be created in its own repository. It should not import from, share runtime state with, or depend on Arc. Arc is only a useful architectural and design reference.

This document is intended to be given directly to Codex when starting the new project.

---

# 1. Product intent

Build a modern, minimal requirements and traceability tool for engineering teams working on physical products and other complex systems.

Comparable products and references include:

- Flow Engineering
- Stell
- Trace.Space
- Jama Connect
- IBM DOORS
- Polarion
- Codebeamer
- Doorstop

The product should not attempt to match the breadth of those platforms. It should implement the smallest useful version of each important product area while preserving a complete engineering value loop.

The goal is not merely to store requirements. The product should help a team answer:

- What must the product do?
- What could go wrong?
- How are those risks controlled?
- How will each requirement or control be verified?
- What evidence proves the verification result?
- Who reviewed or approved it?
- What became stale when something changed?
- Can the team reconstruct this history from durable project state?

The central value is traceability and change awareness.

---

# 2. Core mental model

Engineering organizations have two related problems:

1. Building a product.
2. Proving that the product was built correctly.

Tools such as CAD, GitHub, Jira, LabVIEW, and TestStand primarily help build or test the product.

Requirements and traceability tools preserve the reasoning and evidence around the work:

```text
Requirement
    ↓
Risk
    ↓
Risk control
    ↓
Verification
    ↓
Evidence and result
    ↓
Review or approval
```

Example:

```text
Requirement:
The machine shall maintain pressure within 5%.

Risk:
Pressure instability may damage the product.

Risk control:
Closed-loop pressure monitoring.

Verification:
Run the machine for 1,000 pressure cycles.

Acceptance criteria:
Pressure remains within 5% during every cycle.

Evidence:
evidence/pressure-cycles.csv

Result:
Pass.

Approval:
Reviewed and approved by the responsible engineer.
```

The product should make this chain easy to create, inspect, maintain, and audit.

---

# 3. Product principles

## 3.1 Keep the model explicit

Requirements, risks, and verification are distinct engineering concepts. They should be separate first-class records and separate product surfaces.

Do not collapse the entire domain into one large requirement record merely to reduce code.

The system should still avoid unnecessary object types. A risk control can remain a field on a risk until a real need emerges for controls to become independently managed records.

## 3.2 Git is the version backbone

Git should be a core product primitive, not an implementation detail.

Use Git for:

- Durable history
- Authorship
- Diffs
- Rollback
- Branches
- Tags and baselines
- External collaboration
- Audit evidence

Do not create an application-specific versioning system that duplicates Git.

## 3.3 Files are the source of truth

The engineering project should remain understandable without the application.

Records should live in ordinary files inside an ordinary Git repository. The web application should be a structured editor and reader for those files.

If the product disappeared, a team should still retain:

- Its requirements
- Its risks
- Its verification records
- Its evidence
- Its links
- Its complete Git history

## 3.4 Prefer mature tools over owned subsystems

Before building any subsystem, ask:

1. Does this need to exist?
2. Does the standard library already solve it?
3. Does the platform already solve it?
4. Does an existing mature tool solve it?
5. Can the requirement be handled with a small explicit function?
6. Only then, build the minimum custom system.

Examples:

- Use Git rather than creating version history.
- Use native GitHub or GitLab pull requests rather than immediately creating a full team review platform.
- Use the filesystem rather than creating a database-backed artifact store.
- Use JSON and Python's standard library rather than adding a document parser without a concrete need.
- Use native HTML controls rather than elaborate custom form systems.

Open-source products such as Doorstop should be studied for good domain ideas. They should not be adopted blindly, copied wholesale, or treated as required dependencies.

## 3.5 Minimize surfaces, not domain concepts

Avoid creating pages for every possible activity, but do not hide materially different workflows inside one generic screen.

The initial product should have:

- Requirements
- Risks
- Verification
- Coverage
- Agent

It should not have separate dashboards, reports, review inboxes, evidence libraries, graph explorers, document editors, or workflow builders.

## 3.6 Derive state wherever possible

Avoid storing state that can be calculated from records and Git.

Examples:

- Coverage is derived from links.
- Stale review status is derived from a content hash.
- Stale verification is derived from the hashes of linked records.
- Project health is derived from missing, failed, stale, and unreviewed records.

## 3.7 AI proposes; normal product rules execute

AI should operate through the same domain model, permissions, validation, and Git history as human changes.

AI should not create hidden state or bypass application validation.

## 3.8 Optimize for maintainability

Prefer:

- Fewer files
- Fewer layers
- Fewer abstractions
- Fewer first-class object types
- Explicit functions
- Mechanically traceable state
- Simple unit tests

Avoid:

- Generic repositories and service layers with one implementation
- Schema-driven form engines
- Event buses
- Plugin architectures
- Code generation
- Graph databases
- Background orchestration
- Custom workflow builders
- Compatibility layers for speculative future formats

---

# 4. Product vocabulary

## Requirement

A precise statement describing what the product or system must do.

Example:

> The scanner shall detect tumors larger than 2 mm.

## Risk

Something undesirable that could happen or prevent the product from meeting its goals.

Example:

> The scanner fails to detect a tumor.

## Risk control

A design feature, requirement, or process that reduces a risk.

Example:

> Perform a secondary validation scan.

The initial product stores the control as part of the risk record.

## Verification

The planned activity that proves a requirement or risk control was implemented correctly.

Common methods:

- Test
- Analysis
- Inspection
- Demonstration

## Acceptance criteria

The objective condition that determines whether verification passed.

## Evidence

A file, URL, report, measurement, or external record supporting a verification result.

## Validation

Proof that the product solves the user's real problem. This is distinct from verification, which proves that the product meets its written requirements.

Full validation management is outside the first version.

## Traceability

The ability to move between related requirements, risks, controls, verification records, evidence, and approvals.

## Coverage

A derived view showing which parts of the traceability chain exist, are missing, have failed, or have become stale.

## Review

A recorded human confirmation that an item's current meaningful content has been checked.

## Stale

A previously reviewed or verified record whose relevant content or dependencies have since changed.

---

# 5. Competitor and market context

## Traditional platforms

Products such as Jama, DOORS, Polarion, and Codebeamer primarily act as systems of record for:

- Requirements
- Risks
- Verification
- Reviews
- Traceability
- Compliance reporting

Their main weakness is often operational overhead, complexity, and manual relationship maintenance.

## Flow Engineering

Flow's current AI direction centers on a connected system graph.

Its public model is:

```text
Connected engineering system
        ↓
Agents continuously inspect changes
        ↓
Agents identify and update affected artifacts
        ↓
Humans make architectural judgments
```

Flow emphasizes:

- System-wide connected context
- Impact analysis
- Continuous alignment
- Agents performing engineering work
- Requirements, interfaces, tests, budgets, decisions, and evidence in one connected model

The important lesson is not that this product needs a graph database or autonomous agents immediately. The lesson is that AI becomes more useful when the underlying engineering relationships are explicit.

## Stell

Stell's AI agent, Zelda, is a controlled operator inside its requirements product.

It supports:

- Natural-language queries
- Gap and compliance analysis
- Version comparisons
- Traceability suggestions and edits
- Requirement authoring
- Evidence creation
- Verification updates
- Risk register operations

Stell is explicit that:

- Read actions are lower risk.
- Write actions require explicit user approval.
- AI uses normal user permissions.
- Changes are diffed, logged, and attributed.
- AI should amplify engineering judgment rather than replace it.

This is the more appropriate initial AI posture for this product.

## Trace.Space

Trace.Space emphasizes importing fragmented engineering information and automatically creating or maintaining traceability.

Flow and Trace.Space appear to be converging:

- Flow starts with a connected native model and adds agents.
- Trace.Space starts with ingestion and AI-created traceability and grows toward a connected system model.

The product described in this document should not begin with broad ingestion, automatic extraction, or a generalized engineering graph.

## Doorstop

Doorstop is a useful reference for:

- File-backed engineering records
- Stable IDs
- Explicit links
- Link fingerprints
- Suspect relationship detection
- Review fingerprints
- Validation
- Git-friendly workflows

Doorstop is inspiration only.

Do not use Doorstop as the engine unless future investigation shows that adopting it is clearly simpler than owning the small required model. Do not inherit its complete document model merely because it exists.

---

# 6. File format decision

## What is PyYAML?

PyYAML is a Python package for parsing and writing YAML.

It does not provide:

- A schema
- Requirements management
- Traceability
- Validation rules
- Git integration
- Stale detection
- Review workflows

It only converts between YAML text and Python values.

## YAML evaluation

### Strongest argument for YAML

- Human-readable
- Supports comments
- Supports multiline text
- Familiar in configuration-heavy engineering environments

### Strongest argument against YAML

- Whitespace-sensitive
- Has surprising implicit type behavior
- Has more parser edge cases than JSON
- PyYAML does not preserve comments or formatting when rewriting
- Programmatic round-tripping can create noisy Git diffs
- The product UI, not hand editing, is intended to be the main editing surface

## Decision: use JSON

Use one deterministic JSON file per record.

Reasons:

- Python supports JSON without another dependency.
- Pydantic validates JSON directly.
- Types are strict and predictable.
- AI tools reliably produce and consume JSON.
- Deterministic serialization is easy.
- One record per file keeps Git diffs small.
- Files remain understandable and manually editable.

Use:

```python
json.dumps(data, indent=2, sort_keys=True)
```

or another single deterministic serialization rule used everywhere.

Do not add:

- YAML
- JSON5
- TOML
- Markdown frontmatter
- A custom domain language

Revisit the format only if real users demonstrate that direct file authoring is a primary workflow.

---

# 7. Engineering project structure

Each engineering project is its own Git repository.

```text
engineering-project/
├── project.json
├── requirements/
│   ├── REQ-001.json
│   └── REQ-002.json
├── risks/
│   └── RISK-001.json
├── verifications/
│   └── VER-001.json
└── evidence/
    └── pressure-test.csv
```

## project.json

Keep this small:

```json
{
  "name": "Example Engineering Project",
  "description": "",
  "version": 1
}
```

Do not create configurable schemas, custom item types, workflow definitions, or large project settings.

---

# 8. Core records

## 8.1 Requirement

Suggested shape:

```json
{
  "id": "REQ-001",
  "title": "Pressure stability",
  "statement": "The system shall maintain pressure within 5%.",
  "system": "Machine/Pressure Control",
  "parent_id": null,
  "owner": "Engineering",
  "status": "active",
  "review": null,
  "updated_at": "2026-06-24T12:00:00Z"
}
```

Fields:

- `id`: Stable human-readable identifier.
- `title`: Short scanning label.
- `statement`: The actual requirement.
- `system`: Slash-separated system path.
- `parent_id`: Optional parent requirement.
- `owner`: Responsible person or team as plain text.
- `status`: `draft`, `active`, or `retired`.
- `review`: Review metadata or `null`.
- `updated_at`: Machine-written timestamp.

Do not add:

- Arbitrary custom fields
- Requirement subtypes
- Configurable statuses
- Rich text
- Attachments directly on requirements
- Multiple workflow states

## 8.2 Risk

Suggested shape:

```json
{
  "id": "RISK-001",
  "title": "Pressure instability",
  "description": "Pressure instability may damage the product.",
  "requirement_ids": [
    "REQ-001"
  ],
  "severity": "high",
  "likelihood": "medium",
  "control": "Use closed-loop pressure monitoring.",
  "owner": "Engineering",
  "status": "open",
  "review": null,
  "updated_at": "2026-06-24T12:00:00Z"
}
```

Fields:

- `id`
- `title`
- `description`
- `requirement_ids`
- `severity`: `low`, `medium`, or `high`
- `likelihood`: `low`, `medium`, or `high`
- `control`
- `owner`
- `status`: `open`, `controlled`, or `accepted`
- `review`
- `updated_at`

The first version should not implement:

- FMEA tables
- Hazard trees
- Custom scoring formulas
- Residual-risk calculations
- Separate risk-control objects
- Multiple risk frameworks

## 8.3 Verification

Suggested shape:

```json
{
  "id": "VER-001",
  "title": "Pressure cycle test",
  "requirement_ids": [
    "REQ-001"
  ],
  "risk_ids": [
    "RISK-001"
  ],
  "method": "test",
  "procedure": "Run the machine for 1,000 pressure cycles.",
  "acceptance_criteria": "Pressure remains within 5% for every cycle.",
  "result": "pass",
  "evidence": [
    "evidence/pressure-test.csv"
  ],
  "owner": "Test Team",
  "verified_against": {
    "REQ-001": "sha256:...",
    "RISK-001": "sha256:..."
  },
  "review": null,
  "updated_at": "2026-06-24T12:00:00Z"
}
```

Fields:

- `id`
- `title`
- `requirement_ids`
- `risk_ids`
- `method`: `test`, `analysis`, `inspection`, or `demonstration`
- `procedure`
- `acceptance_criteria`
- `result`: `pending`, `pass`, or `fail`
- `evidence`: Workspace-relative paths or URLs
- `owner`
- `verified_against`: Content hashes recorded when a pass result is saved
- `review`
- `updated_at`

The product records verification. It does not need to execute tests.

Do not add:

- A test runner
- Test automation orchestration
- Test suites and campaigns
- Evidence extraction
- Evidence parsing
- A separate evidence database

---

# 9. Links and traceability

Use explicit stable IDs in record fields.

Examples:

- Risk links to requirements through `requirement_ids`.
- Verification links to requirements through `requirement_ids`.
- Verification links to risks through `risk_ids`.
- Requirement hierarchy uses `parent_id`.

Do not begin with:

- A generic link object
- An edge table
- A graph database
- Arbitrary user-defined relationship types

The initial relationships are known and few. Model them directly.

Validation must check:

- IDs are unique.
- File names match record IDs.
- Every referenced ID exists.
- Parent links do not form cycles.
- Evidence paths remain inside the project when they are local paths.
- Required fields are present.
- Enum values are valid.
- Verification records with `pass` include evidence.
- Review and verification hashes use the current hashing format.

---

# 10. Review and stale detection

## Review model

A review stores:

```json
{
  "by": "Reviewer",
  "at": "2026-06-24T12:00:00Z",
  "content_hash": "sha256:..."
}
```

The content hash excludes:

- `review`
- `updated_at`
- Other machine-written fields that should not invalidate review

If meaningful content changes, the current content hash no longer matches the stored review hash and the item is stale.

## Verification stale detection

When a verification result is set to `pass`, store hashes of the linked requirements and risks in `verified_against`.

The verification becomes stale if:

- A linked requirement changes.
- A linked risk changes.
- The verification procedure changes.
- The acceptance criteria change.
- Evidence is removed or changed.

The initial implementation should be conservative. It is better to ask for re-review too often than silently treat changed engineering evidence as current.

## Why use hashes as well as Git?

Git provides authoritative history and authorship.

Hashes provide a fast deterministic answer to:

> Does this review or verification still apply to the current content?

Do not create a separate approval-history database.

---

# 11. Derived coverage model

Coverage is a read-only derived view.

It should answer:

```text
Requirement
    → linked risks
    → risk controls
    → linked verification
    → result
    → evidence
    → review state
```

Useful derived statuses:

- `missing-risk`: No linked risk has been considered.
- `uncontrolled-risk`: A linked open risk has no control.
- `missing-verification`: No linked verification exists.
- `planned`: Verification exists but remains pending.
- `failed`: At least one required verification failed.
- `missing-evidence`: Verification passed without valid evidence.
- `awaiting-review`: Current records have not been reviewed.
- `stale`: Review or verification hashes no longer match current content.
- `verified`: Required verification passed, evidence exists, and relevant records are current.

Do not persist these statuses. Calculate them from current files.

Coverage replaces:

- A dashboard
- A traceability report page
- A review inbox
- A project health page

Filters and counts inside Coverage are enough initially.

---

# 12. Git behavior

## Two Git repositories

There are two independent repositories:

```text
Product source repository
    contains frontend, backend, docs, and tests

Engineering project repository
    contains requirements, risks, verification, and evidence
```

## Application writes

Every successful user mutation should become one small Git commit:

```text
Create requirement REQ-014
Update risk RISK-003
Record verification VER-009 result
Review requirement REQ-014
Accept agent proposal for REQ-014
```

Write sequence:

1. Check repository state.
2. Write changed files atomically.
3. Validate the entire project.
4. Commit the exact changed paths if validation passes.
5. Restore those paths if validation fails.

## Dirty repositories

Manual file editing must remain supported.

If the application finds uncommitted external changes:

- Continue allowing reads.
- Show the changed paths and diff.
- Pause normal application writes.
- Let the user commit or discard the changes.

Do not attempt automatic merging in the first version.

## Native Git concepts

- Baseline = Git tag
- Release = Git commit or tag
- Undo = Git revert
- Comparison = Git diff
- History = Git log
- Authorship = Git commit author
- Collaboration = branch and pull request

Do not rename these into application-specific equivalents unless the UI needs a simpler label.

## Validation CLI

The same validation used by FastAPI should be callable without the web application:

```bash
python -m app.cli validate /path/to/engineering-project
```

This supports:

- Local checks
- Pre-commit hooks
- GitHub Actions
- External editors

Do not build a separate CI service.

---

# 13. Product surfaces

Use five primary routes:

```text
/requirements
/risks
/verification
/coverage
/agent
```

A Git changes panel should be globally accessible but does not need its own route.

## 13.1 Requirements

Purpose:

- Create and manage requirements.
- Inspect hierarchy.
- See linked risks and verification.
- Review current content.

Layout:

```text
Toolbar
────────────────────────────────────────────────────────
Requirements table                 Selected requirement
                                   inspector
```

Table columns:

- ID
- Requirement
- System
- Owner
- Status
- Risks
- Verification
- Review
- Updated

Inspector sections:

- Requirement
- Hierarchy
- Linked risks
- Linked verification
- Review
- Git history

Use a slash-separated system path:

```text
Vehicle
Vehicle/Battery
Vehicle/Battery/Controller
```

Derive hierarchy and filters from existing values. Do not create separate System records initially.

## 13.2 Risks

Purpose:

- Maintain a compact risk register.
- Connect risks to requirements.
- Record controls.
- Review risk state.

Table columns:

- ID
- Risk
- Requirements
- Severity
- Likelihood
- Control
- Status
- Review
- Updated

Inspector sections:

- Risk
- Assessment
- Control
- Linked requirements
- Linked verification
- Review
- Git history

## 13.3 Verification

Purpose:

- Plan how requirements and controls will be proven.
- Record results.
- Attach evidence references.
- Detect stale results.

Table columns:

- ID
- Verification
- Method
- Requirements
- Risks
- Result
- Evidence
- Stale
- Review
- Updated

Inspector sections:

- Verification plan
- Acceptance criteria
- Linked requirements and risks
- Result
- Evidence
- Review
- Git history

## 13.4 Coverage

Purpose:

- Provide the traceability matrix.
- Show missing, failed, stale, and complete chains.

This is a table, not a dashboard.

Suggested columns:

- Requirement
- Risks
- Controls
- Verification
- Result
- Evidence
- Review
- Overall state

Useful filters:

- All
- Missing risk
- Uncontrolled risk
- Missing verification
- Failed
- Missing evidence
- Awaiting review
- Stale
- Verified

Coverage rows should link back to the relevant item inspectors.

## 13.5 Agent

Purpose:

- Query the engineering project.
- Analyze gaps and impact.
- Propose structured changes.

The Agent should not replace the register interfaces.

Users should be able to reference records by ID:

```text
Why is REQ-014 stale?
Show high-severity risks without passing verification.
Suggest verification for REQ-008.
Improve the wording of REQ-021.
```

---

# 14. Shared UI pattern

Requirements, Risks, and Verification should use the same broad shell:

```text
┌──────────────────────────────────────────────────────────────┐
│ Page title   Search   Filters   New                          │
├──────────────────────────────────┬───────────────────────────┤
│ Table                            │ Selected item inspector   │
│                                  │                           │
│ Click a row to select it         │ Explicit form fields      │
│                                  │ Relationships             │
│                                  │ Review                    │
│                                  │ History                   │
└──────────────────────────────────┴───────────────────────────┘
```

Share layout and table primitives.

Keep forms explicit:

- `RequirementForm`
- `RiskForm`
- `VerificationForm`

Do not create a generic schema-driven form renderer.

Selection should be reflected in the URL:

```text
/requirements?selected=REQ-014
```

Filters should also be URL state where useful.

---

# 15. UI direction

Take design inspiration from Arc, especially:

- Sparse operational screens
- Table-first layouts
- Strong information hierarchy
- Thin dividers
- Restrained borders
- Compact controls
- Square corners
- Clear semantic status icons
- Crisp light and dark themes
- Minimal chrome

Avoid:

- Decorative dashboards
- Marketing-style layouts
- Card grids
- Nested cards
- Large empty hero areas
- Gradient-heavy AI styling
- Graph-first interfaces
- Rich animation
- Drag and drop
- Dense configuration screens

Use status colors only when they improve scanning:

- Pass or current: emerald
- Failed: red
- Pending: muted
- Stale: orange or yellow
- Running AI action: blue

---

# 16. Greenfield application architecture

The new product should live in a completely new repository:

```text
requirements-tool/
├── frontend/
├── backend/
├── example-project/
├── AGENTS.md
├── ARCHITECTURE.md
├── DESIGN.md
├── Makefile
└── README.md
```

## Overall shape

```text
Browser UI
    React + TypeScript
        ↓
FastAPI control plane
        ↓
Pydantic models
Filesystem helpers
Git CLI
        ↓
Engineering project repository
```

No application database initially.

## Architectural approach

Follow the useful shape of Arc:

- Browser UI is the control panel.
- FastAPI is the control plane.
- Files are durable project state.
- Git versions the project.
- Pydantic defines trust-boundary schemas.
- Core modules remain small and direct.
- API routes call explicit core functions.
- Agent tools call the same core functions.

Do not copy Arc's domain model or code.

---

# 17. Frontend stack

Use:

- React 19
- TypeScript
- Vite
- TanStack Router
- TanStack Query
- TanStack Table
- Base UI
- Iconify
- Proicons icon set
- Plain CSS with semantic variables
- React Markdown for Agent responses only

Ponytail should be included as a development dependency or installed Codex skill to reinforce minimal implementation choices. It is not shipped application functionality.

Do not add initially:

- Clerk
- Zustand
- Redux
- Tailwind
- Form libraries
- Rich-text editors
- Graph visualization libraries
- Drag-and-drop libraries
- Component generators
- Large design systems
- Playwright browser checks

Prefer native controls when sufficient:

- Text inputs
- Textareas
- Checkboxes
- Date or datetime inputs
- Tables
- File inputs

Use Base UI for:

- Dialogs
- Menus
- Selects
- Tooltips
- Other interactions where accessible primitives materially reduce work

---

# 18. Backend stack

Use:

- Python 3.11 or newer
- FastAPI
- Uvicorn
- Pydantic
- Python standard-library JSON
- Python standard-library filesystem functions
- Git CLI through `subprocess`
- `python-multipart` only if evidence upload is included
- Pytest
- Ruff

Add only when needed:

- `openai-agents`
- `python-dotenv`
- Resend

Do not add initially:

- PyYAML
- SQLite
- PostgreSQL
- DuckDB
- Pandas
- NumPy
- Plotly
- Celery
- Redis
- Background schedulers
- ORM layers
- Repository abstractions

## Resend

Do not include Resend in the first product slice.

Email only becomes useful when the product has:

- Real users
- Trusted identities
- Assignments
- Review requests
- Notifications

Without authentication, email workflows lack a reliable identity and permission model.

---

# 19. Suggested backend modules

Keep the backend small:

```text
backend/app/
├── main.py
├── config.py
├── api/
│   └── routes.py
├── schemas/
│   └── domain.py
└── core/
    ├── project.py
    ├── requirements.py
    ├── risks.py
    ├── verifications.py
    ├── coverage.py
    ├── validation.py
    ├── hashes.py
    ├── git_service.py
    └── agent.py
```

This is a guide, not a requirement to create every file immediately.

Ponytail rule:

> Start with fewer files. Split only when one file contains clearly separate responsibilities and has become hard to read.

Do not create:

- Controllers
- Services
- Repositories
- Domain interfaces
- Dependency-injection containers
- Factories

FastAPI route:

```text
Route
    → Pydantic validation
    → one explicit core function
    → filesystem and Git
```

---

# 20. Suggested API surface

Keep endpoints conventional.

```text
GET    /api/project
GET    /api/requirements
PUT    /api/requirements/{id}
DELETE /api/requirements/{id}

GET    /api/risks
PUT    /api/risks/{id}
DELETE /api/risks/{id}

GET    /api/verifications
PUT    /api/verifications/{id}
DELETE /api/verifications/{id}

GET    /api/coverage

POST   /api/reviews/{kind}/{id}

GET    /api/git/status
GET    /api/git/diff
POST   /api/git/commit
POST   /api/git/discard

POST   /api/agent
POST   /api/agent/proposals/{id}/apply
```

Do not add bulk endpoints until the UI needs them.

Creating and updating can use the same `PUT` operation with a stable ID, as Arc does for file-backed records.

---

# 21. AI strategy

## Initial posture

Use Stell's controlled operator model before considering Flow's autonomous-agent model.

Start with:

- Natural-language queries
- Gap analysis
- Impact explanations
- Requirement-quality suggestions
- Risk and verification suggestions
- Structured proposed edits

Do not start with:

- Continuous background agents
- Autonomous multi-record rewrites
- Automatic evidence ingestion
- Automatic link maintenance
- A generalized systems graph
- Embeddings
- A vector database
- Multiple specialized agents

## Deterministic work remains deterministic

The following should be calculated by code:

- Missing links
- Broken links
- Coverage
- Stale reviews
- Stale verification
- Invalid evidence paths
- Failed verification

Do not ask a language model questions the product can answer exactly.

## Agent tools

If `openai-agents` is added, give the agent narrow function tools:

- `list_requirements`
- `get_requirement`
- `list_risks`
- `get_risk`
- `list_verifications`
- `get_verification`
- `get_coverage`
- `get_git_diff`
- `propose_changes`

The agent should not initially receive a raw filesystem write tool.

## Proposal model

AI returns a structured proposal validated with Pydantic:

```json
{
  "summary": "Improve REQ-014 and add missing acceptance criteria.",
  "changes": [
    {
      "kind": "requirement",
      "id": "REQ-014",
      "before": {},
      "after": {}
    }
  ]
}
```

The UI shows:

- Summary
- Before and after values
- Validation result
- Files that will change

The user explicitly accepts or rejects the proposal.

Accepted proposals use the same:

- Core save functions
- Validation
- Git commit path
- Audit history

as human edits.

## SandboxAgent decision

Do not use a filesystem SandboxAgent for the first AI implementation.

Narrow tools are simpler and ensure that AI cannot bypass the domain model.

A sandbox-style agent becomes justified when the product needs broad work over:

- Arbitrary project files
- External documents
- Scripts
- Test artifacts
- Large multi-file proposals

At that point:

1. Create an isolated Git worktree and branch.
2. Scope the sandbox to that worktree.
3. Let the agent make changes there.
4. Run project validation.
5. Show the Git diff.
6. Require explicit human approval before merge.

The OpenAI Agents SDK is suitable for function tools, approval flows, traces, and later sandbox-backed workflows. Use it only when those capabilities reduce code relative to a direct Responses API call.

References:

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Agents SDK tools](https://openai.github.io/openai-agents-python/tools/)

---

# 22. Authentication and collaboration

Do not implement user authentication initially.

Assume:

- One local operator
- One configured engineering project repository
- Git author configuration identifies commits

This is enough to validate the product model and core workflow.

Later, when remote teams become a real requirement, consider:

- Clerk or another auth provider
- Project-level roles
- Remote Git hosting integration
- Pull-request-based review
- Resend notifications

Do not create placeholders or abstractions for these systems now.

---

# 23. Evidence handling

Initial evidence support should be deliberately basic.

Allow verification records to contain:

- Workspace-relative file paths
- HTTPS URLs

If upload is implemented, files go directly into:

```text
evidence/
```

Do not build:

- Evidence extraction
- Evidence classification
- PDF parsing
- Document preview
- File conversion
- Automatic test result analysis
- An object-storage layer

Large binary evidence can use Git LFS later if normal Git becomes a real problem.

---

# 24. Explicitly out of scope

Do not implement in the first product:

- Document view
- Rich-text specifications
- PDF import
- Assisted extraction
- Office document import
- Graph view
- Generic relationship types
- Graph database
- Configurable schemas
- Custom fields
- Configurable workflows
- Notifications
- Supplier portal
- Standards library
- Interface management
- Baseline management UI
- Report builder
- Full risk matrices
- FMEA
- Hazard trees
- Test execution
- Real-time collaboration
- Presence
- Comments
- Mobile-specific UI
- Offline synchronization
- Automatic merging
- Background agents
- Vector search
- Embeddings
- Multiple AI agents
- Analytics dashboards
- Marketing-style metrics
- Backwards-compatibility shims

Add one of these only after a concrete user workflow demonstrates that the simpler product is insufficient.

---

# 25. Build sequence

## Phase 1: project engine

Implement:

- Engineering project initialization
- JSON models
- Deterministic serialization
- Requirements CRUD
- Risks CRUD
- Verification CRUD
- Link validation
- Content hashes
- Review hashes
- Verification stale detection
- Git commits
- Validation CLI

Deliverable:

An engineering project can be managed through Python and Git without the frontend.

Verification:

- Small unit tests
- One end-to-end backend test for the closed loop

## Phase 2: core registers

Implement:

- Application shell
- Requirements route
- Risks route
- Verification route
- Shared table and inspector layout
- Search and simple filters
- URL-backed selection
- Create, edit, delete, and review actions

Deliverable:

The full engineering chain can be created and maintained through the UI.

## Phase 3: coverage

Implement:

- Derived coverage calculation
- Coverage table
- Missing, failed, stale, and verified filters
- Links back to source records

Deliverable:

The user can see where the traceability chain is incomplete or no longer valid.

## Phase 4: Git changes

Implement:

- Global repository status
- Changed path list
- Diff view
- Manual commit
- Safe discard
- Read-only behavior while unresolved external changes exist

Deliverable:

Manual file editing and application editing coexist predictably.

## Phase 5: controlled Agent

Implement:

- Agent route
- Narrow read tools
- Coverage and impact queries
- Structured proposals
- Proposal diff
- Explicit apply action
- Normal validation and Git commit

Deliverable:

AI helps understand and modify the engineering project without bypassing the product model.

## Later only when justified

- Authentication
- Remote project repositories
- Pull request integration
- Review notifications
- Resend
- Git LFS
- Sandbox-backed broad agent work

---

# 26. Complexity expectations

The non-AI initial product is a medium build.

Rough scope:

- 20-30 source files
- Approximately 2,000-3,500 lines across frontend, backend, styles, and tests

The controlled AI layer is a small-to-medium addition.

Rough scope:

- 3-6 additional or changed files
- Approximately 300-600 lines

These are scope estimates, not targets. Fewer files and fewer lines are preferable when the same behavior remains clear.

---

# 27. Codex implementation instructions

When using this brief to build the product:

1. Create a clean, standalone repository.
2. Write `AGENTS.md`, `ARCHITECTURE.md`, and `DESIGN.md` from the durable principles in this document.
3. Build the filesystem and Git engine before the UI.
4. Keep JSON records as the source of truth.
5. Validate all reads at the Pydantic boundary.
6. Use Git for all project history.
7. Keep requirements, risks, and verification separate.
8. Derive coverage and stale state.
9. Avoid adding dependencies unless they remove more code and maintenance than they add.
10. Use simple unit tests rather than browser tests unless explicitly requested.
11. Do not build speculative extension points.
12. Do not silently expand the scope.
13. If a simpler design can close the same engineering loop, prefer it.
14. If a simplification removes a real domain workflow, reject the simplification.
15. Keep AI read-only or proposal-based until the normal product loop is reliable.

The closed loop that must work before adding long-tail features is:

```text
Create requirement
    ↓
Link risk and control
    ↓
Plan verification
    ↓
Attach evidence and record result
    ↓
Review records
    ↓
Change upstream content
    ↓
See downstream verification become stale
    ↓
Re-verify and review
```

If that loop is clear, reliable, Git-backed, and pleasant to use, the product has achieved its first meaningful version.
