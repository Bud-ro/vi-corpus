# Reference Output

## Root Cause

The dominant slowdown was verifier-induced: repeated `QTest.qWait` polling held
the GIL and starved the worker. Replacing worker waits with `processEvents()` plus
a short sleep restored sub-second full-profile execution without changing sample
counts or outputs. QTest remains in use for actual clicks and pointer movement.

## Data Verdict

- Full display source is 50 by 1024 for the selected delay.
- Workflow, disk readback, and displayed image are compared independently.
- Pixel-edge/center registration and hover z are checked at first, middle, and
  last coordinates.
- Target-derived reconstruction is labeled
  `target_derived_roundtrip_simulator_fixture`.
- `independent_labview_algorithm_parity_blocked_no_raw_fixture` remains.

## UI Verdict

Fresh full-window screenshots are still required for every tab. White scroll
backgrounds, clipped path buttons, incomplete wrapped state text, and checkbox
indicator misses remain blocking even when automated JSON says pass.
