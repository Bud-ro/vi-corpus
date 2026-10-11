# Pump-Probe Migration Lessons

This case study distills three real task histories: a two-project supervisor, a
regular delay-map migration, and a power-dependent nested-map migration. Paths,
device identifiers, and outputs are generalized for public reuse.

## What Initially Looked Correct But Was Not

- Visible scan inputs were not the axes actually executed because a parity CSV or
  hard-coded plan silently won.
- Stop produced full-size zero-filled outputs and a Completed-looking UI.
- Buttons existed but only changed text; verifier inventories counted them as
  functional.
- Hover checks called internal setters instead of moving a pointer.
- Heatmap checks compared a target row with the same target row and searched
  source code for UI behavior.
- A target CSV was injected into simulated raw data, then recovered with tiny
  numerical error and misreported as independent LabVIEW parity.
- A multi-scan partial stop truncated all scans to the shortest scan.
- Per-repeat logs were compressed into point summaries, losing call order and
  single-repeat failure localization.
- A Qt verifier used `QTest.qWait` in worker polling and made a sub-second scan
  appear to take tens of seconds.
- A one-file EXE bootloader ran without reaching Python entry; process existence
  was mistaken for startup progress.
- Aggressive PyInstaller `collect_all` created an oversized, stalled build.
- A process was terminated based on start time and was later shown to belong to
  the sibling project.

## Corrections That Generalize

- Resolve and display one immutable scan plan; fail closed when its source is
  missing or invalid.
- Preserve semantic event order while buffering physical writes.
- Keep validity masks and NaN unacquired regions for partial output.
- Compare workflow, disk readback, and displayed arrays separately.
- Label target-derived fixtures and keep independent algorithm parity blocked
  without raw LabVIEW input.
- Use real canvas events and coordinate transforms for hover acceptance.
- Measure both headless core and real UI wall-clock with the same profile.
- Keep one canonical source verifier and share criteria with the EXE verifier.
- Require full-window human screenshot review in addition to OpenCV checks.
- Build only after source approval, prove current-source lineage, then launch the
  exact root binary and public shortcuts.
- Confirm process ownership from command line and gate path before termination.

## UI Details That Required Human Review

- overlapping LabVIEW-style scan rows at 1366x768;
- bottom status hidden after introducing scrolling;
- output paths showing only their tail;
- a Browse button clipped to `Brow...`;
- a scroll page turning white inside a dark theme;
- multi-line control state clipped in the real window despite a standalone
  control capture showing the full text;
- checkbox clicks missing the native indicator rectangle;
- plot hover coordinates becoming wrong after scrolling;
- quick-preview heatmaps being presented as full-resolution evidence.

These are why a JSON pass cannot replace screenshot review.
