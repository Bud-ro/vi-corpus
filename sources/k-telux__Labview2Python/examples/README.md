# Examples

These examples are sanitized from real LabVIEW-to-Python migration histories.
They preserve engineering decisions and acceptance boundaries while removing
private paths, licensed vendor material, instrument identifiers, and raw chat
transcripts.

## Visual showcase

[Open the completed-interface showcase](showcase/README.md).

| Pump-probe | Spectroscopy / TCSPC |
|---|---|
| <img src="showcase/assets/pump-probe-industrial-ui.png" width="100%" alt="Completed pump-probe Python UI"> | <img src="showcase/assets/spectroscopy-tcspc-ui.png" width="100%" alt="Completed spectroscopy and TCSPC Python UI"> |

## Input/output cases

| Case | Input | Reference output | Focus |
|---|---|---|---|
| Dual-project orchestration | [input](01-dual-project-orchestration/input.md) | [output](01-dual-project-orchestration/output.md) | Ownership and phase gates |
| Performance and heatmap gate | [input](02-performance-heatmap-gate/input.md) | [output](02-performance-heatmap-gate/output.md) | Timing, data lineage, real hover |
| Packaged EXE gate | [input](03-packaged-exe-gate/input.md) | [output](03-packaged-exe-gate/output.md) | Build lineage and runtime proof |

Reference outputs demonstrate the expected reasoning shape, not a claim that
every adapter, EXE, or physical instrument in another project has passed.
