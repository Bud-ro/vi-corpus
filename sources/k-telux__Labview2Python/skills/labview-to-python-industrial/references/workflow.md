# Migration And Data Workflow

## 1. Freeze The Source Of Truth

Inventory the main VI, subVIs, ctl/type definitions, project files, event
structures, queues, timed loops, property nodes, DAQ/VISA/GPIB/.NET/DLL calls,
front-panel images, experiment notes, calibration constants, known outputs, and
driver versions. Mark archives and obsolete variants so they cannot become an
accidental baseline.

Create a parity matrix with these columns:

| LabVIEW behavior | Python owner | Simulator behavior | Evidence | Status |
| --- | --- | --- | --- | --- |
| control/default/unit | model or UI | same accepted values | test/screenshot | status |
| call order/timing | workflow/adapter | ordered event trace | run log | status |
| processing/save | processing/data | same shape/axes/schema | readback | status |

## 2. Resolve One Scan Plan

Parse and validate user input once before starting a worker. Produce an immutable
resolved plan containing axes, units, point counts, repeats, hardware targets,
expected acquisition count, output size, and estimated duration. Display this
plan in the UI and persist it with the run.

Never let a visible parameter disagree with the executed axis. Never silently
fall back to a fixed CSV or synthetic plan when an explicit parity profile is
required. Fail closed with an in-window error before starting hardware.

## 3. Preserve Measurement Semantics

Document and test:

- initialization and delay order;
- nested delay/power/scan loops;
- LightField, DAQ, shutter, stage, meter, and actuator call order;
- wavelength-to-pixel and stage/delay conversions;
- averaging, transient extraction, map assembly, axis direction, and units;
- pause, resume, repeat-stop, partial stop, failure, and exit cleanup;
- file names, headers, metadata, raw arrays, logs, and final screenshots.

Do not optimize logging by dropping per-repeat meaning. Buffer physical writes if
needed, but preserve ordered events with scan index, target, operation, status,
and timestamp so the hardware sequence can be reconstructed.

## 4. Keep Partial Results Honest

Initialize unacquired values as `NaN` or use an explicit validity mask. A partial
stop must not show `Completed` or `100%`, and it must not fill unmeasured points
with plausible zeros. For multiple scans, preserve every acquired sample; do not
truncate earlier complete scans to the shortest later scan.

Write a terminal manifest last. It must distinguish complete, stopped-partial,
failed, and cleanup-failed runs and list which output files were committed.
Single-file temporary replacement is not an atomic transaction for a file group.

## 5. Simulate Through The Production Path

Use deterministic profiles for normal, quick preview, full parity, slow device,
timeout, failed initialization, failed acquisition, failed save, and failed
cleanup. Keep real dimensions, units, metadata, call order, and save schema.

Label target-derived fixtures precisely. When LabVIEW raw input is unavailable,
add independent synthetic raw tests for processing math and keep independent
algorithm parity blocked.

## 6. Read Back What The User Receives

After each run, compare:

1. workflow result arrays;
2. persisted CSV/NPZ/HDF5 and metadata;
3. the arrays bound to plots or image items;
4. the expected fixture or LabVIEW output.

Report separate tolerances and errors for each edge. Do not infer disk or UI
correctness from the in-memory result.
