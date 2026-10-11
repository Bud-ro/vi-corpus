---
name: labview-to-python-industrial
description: Industrial workflow for converting, auditing, optimizing, or packaging LabVIEW measurement VIs as Python applications. Use for LabVIEW to Python, LabVIEW-to-Python, LabVIEW转Python, VI migration, pump-probe or laboratory control software, PyQt/PySide industrial UI, hardware driver and SDK migration, simulator/data parity, performance regressions, screenshot UI review, supervisory gatekeeping, or Windows EXE delivery.
---

# LabVIEW To Python Industrial

Treat a migration as an evidence-controlled replacement of an experiment, not a
front-panel rewrite. Preserve measurement semantics first; optimize UI and
packaging only after the preceding gate is approved.

## Establish Scope

1. State the role: implement, review/supervise, or package/verify only.
2. Record the writable subtree. Do not cross it or terminate unrelated processes.
3. Freeze the canonical VI, subVIs, type definitions, front-panel images, known
   outputs, vendor SDK versions, and one known-good run when available.
4. Separate verdicts for `inventory`, `simulator`, `source UI`, `packaged EXE`,
   `real hardware`, and any unresolved subsystem such as phase/chopper control.
5. Reuse existing workflow, adapters, verifier, and packaging scripts before
   creating another framework.

## Load The Right Reference

- Migration, parity inventory, scan plans, and saving: `references/workflow.md`
- Hardware, SDK manifests, safety, and EXE lineage: `references/hardware-packaging.md`
- UI design and screenshot acceptance: `references/ui-qa.md`
- Performance, heatmaps, plots, and anti-self-proof checks:
  `references/performance-data-parity.md`
- Multi-project supervision and phase gates: `references/supervision-gates.md`
- Pump-probe lessons from real migrations: `references/case-study-pumpprobe.md`
- Chinese operator summary: `references/i18n/zh-CN.md`
- Japanese operator summary: `references/i18n/ja-JP.md`

## Use One Runtime Core

Keep one state machine for initialization, scan planning, acquisition, pause,
resume, stop, saving, and cleanup. Both real and simulated adapters must execute
through it. UI callbacks render and command that workflow; they do not copy it.

Require each adapter to expose status, initialize, the commands used by the VI,
and fail-closed cleanup. A simulator must preserve shapes, axes, units, metadata,
event order, and save formats, including deterministic failure profiles.

## Enforce Gates In Order

1. **Inventory:** map every control, default, unit, limit, property node, event,
   driver call, save field, error path, and shutdown path.
2. **Logic/data:** prove the resolved scan plan, hardware call order, conversion,
   processing, partial-stop behavior, and persisted outputs.
3. **Simulator:** run normal, boundary, timeout, failed init/acquire/save/cleanup,
   pause/resume, and partial stop through the production workflow.
4. **Source UI:** use real clicks, typing, combo opening, scrolling, mouse hover,
   and screenshots at normal and constrained resolutions.
5. **Packaged EXE:** rebuild from the approved source, prove source/build/hash
   lineage, then repeat critical runtime scenarios from the distributable.
6. **Real hardware:** remain `unvalidated_blocked` until an operator-approved,
   fail-closed dry run is performed on the actual devices.

Do not enter the next gate without explicit evidence that the previous gate is
approved. Do not reuse stale screenshots or old binaries after relevant source
or verifier changes.

## Reject Invalid Proof

- A target CSV injected into a simulator and reconstructed is a
  `target_derived_roundtrip_simulator_fixture`, not independent LabVIEW algorithm
  parity.
- A verifier comparing a target array with itself, searching source strings, or
  calling a hover setter is self-proof and must fail.
- A process launch, a nonblank window, JSON `passed=true`, or a test count of zero
  is not sufficient runtime evidence.
- A quick preview with reduced points cannot prove full-resolution parity.
- An in-memory comparison cannot prove saved-file or displayed-image parity.
- Simulator success cannot prove vendor driver or real hardware compatibility.

## Produce Evidence

For each accepted gate, record commands, runtime versions, source and verifier
hashes, profile/axes/shapes, semantic event counts, wall-clock timings, output
readback, screenshots, and unresolved blockers. Use fresh non-destructive
artifact directories and preserve failed gates as diagnostics.

End with exact labels such as:

- `source_ui_verified`
- `simulator_verified`
- `packaged_exe_verified`
- `real_hardware_unvalidated_blocked`
- `independent_labview_algorithm_parity_blocked_no_raw_fixture`

If required evidence is absent, report `incomplete` or `blocked_unverified`.
