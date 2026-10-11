# Completed Interface Showcase

This case shows two sanitized Python interfaces produced during real
LabVIEW-to-Python migration verification. Both screenshots capture terminal
simulator states with populated results rather than empty launch windows.

## Pump-probe workflow

<img src="assets/pump-probe-industrial-ui.png" width="100%" alt="Completed pump-probe industrial Python UI">

Visible evidence includes:

- completed scan and step state;
- transient and recent-spectrum plots;
- simulator versus blocked real-hardware indicators;
- exposure, DAQ, shutter, scan-plan, and result metadata;
- progress, result summary, timestamps, and event log.

## Spectroscopy and TCSPC workflow

<img src="assets/spectroscopy-tcspc-ui.png" width="100%" alt="Completed spectroscopy and TCSPC Python UI">

Visible evidence includes:

- TCSPC decay and integrated spectral-count heatmap;
- scan controls and user-defined acquisition parameters;
- simulation inputs, device summary, result monitor, and wavelength table;
- explicit completed state and saved-run identifier.

## Evidence boundary

The screenshots demonstrate the layout and visible simulator completion states.
They do not independently prove LabVIEW algorithm equivalence, current packaged
EXE lineage, vendor-driver communication, calibration, or real hardware safety.
Those claims require the structured and runtime gates defined by the canonical
[skill](../../skills/labview-to-python-industrial/SKILL.md).

The images contain no private filesystem paths, credentials, raw laboratory
data, vendor SDK binaries, or instrument serial numbers.
