# Reference Output

## Gate Result

- Both projects use one workflow core with mode-specific UI presentation.
- Resolved plans, raw dimensions, saved CSV axes, averaging, partial stop, and
  fail-closed cleanup have dedicated evidence.
- SDK manifests prove inventory only; real driver communication remains blocked.
- Source UI requires fresh Industrial and LabVIEW screenshots with real
  interactions and independent human review.
- Packaging is not authorized until each source gate is approved.

## Status Labels

- `simulator_verification_pending_current_logic_evidence`
- `source_ui_verification_pending_fresh_screenshots`
- `packaged_exe_verification_pending_source_approval`
- `real_hardware_unvalidated_blocked`
- `phase_chopper_blocked_unverified`

## Supervision Decision

Keep hard per-project write boundaries. Reuse stable execution tasks, preserve
failed gates as diagnostics, and issue exact blocker lists rather than replacing
writers or rushing SDK study.
