# LabVIEW To Python Industrial Rule

Rule version: 2.1.0

This is a derived standalone policy excerpt for rule-based agents. The canonical
operational source is `skills/labview-to-python-industrial/SKILL.md`; if wording
conflicts, follow the skill.

Apply this rule whenever work converts, audits, optimizes, validates, or packages
LabVIEW laboratory or industrial measurement software in Python.

## Non-Negotiable Rules

1. Preserve measurement and data-processing semantics before visual polish.
2. Use one workflow/state machine for industrial UI, LabVIEW-style UI, simulator,
   and real adapters.
3. Resolve and persist one scan plan. Visible parameters must match executed axes,
   counts, units, output root, and estimated workload.
4. Preserve hardware call order, per-repeat meaning, safety limits, and fail-closed
   cleanup. Performance work may reduce physical writes, not semantic evidence.
5. Treat reduced-point runs as `quick_preview`; they cannot prove full data parity.
6. Treat target-derived simulator reconstruction as a roundtrip fixture; it cannot
   prove independent LabVIEW algorithm parity without independent raw input.
7. Compare workflow result, persisted readback, and displayed plot/image data from
   the same run. A target compared with itself is invalid proof.
8. UI verification requires real user events, fresh target-window screenshots,
   automated image checks, and human review. Internal setters, source searches,
   process existence, or JSON alone cannot pass a UI gate.
9. Measure performance through the real UI path with the same profile. A verifier
   may not drop points, raw files, event semantics, or saving to pass.
10. Keep inventory, simulator, source UI, packaged EXE, real hardware, and blocked
    subsystems as separate verdicts.
11. Rebuild EXEs after relevant source or verifier edits; record source/build/hash
    lineage and launch the exact distributable and public shortcuts.
12. Verify process ownership by command line and project/gate path before stopping
    a process.
13. Preserve failed gates as diagnostics and create fresh non-destructive evidence
    for every new acceptance claim.
14. Real hardware remains `unvalidated_blocked` until an operator-approved,
    fail-closed dry run on the actual devices succeeds.

When this rule conflicts with a newer explicit user instruction, follow the newer
instruction and record the deviation. Never weaken evidence silently.
