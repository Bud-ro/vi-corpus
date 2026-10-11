# Hardware, SDK, Process, And Packaging Gates

## Adapter Contract

Keep the surface small: `status`, `initialize`, commands actually used by the VI,
and `close`. Status must distinguish connected, simulated, optional, failed, and
blocked. Convert vendor errors into explicit timeout, limit, driver, and cleanup
failures without hiding the original diagnostic.

## Hardware Safety

- Motion devices require limits, units, calibration, and a checked zero/reference
  path.
- Shutters close on initialization failure, stop, scan failure, and app exit.
- DAQ outputs return to safe values on failure.
- Lasers and source meters require ramping and operator approval before output.
- Do not probe real hardware merely to satisfy a software gate.

## SDK Manifest

For each driver or SDK record vendor, product, purpose, source URL, version,
license/redistribution status, local file name, SHA256 when redistributable, Python
binding, architecture, runtime dependency, and blocker. Do not commit vendor
binaries or license files unless redistribution is explicitly allowed.

The manifest proves what was inventoried. It does not prove that a driver loaded
or communicated with real hardware.

## Process Ownership

Before stopping a hung verifier or packaged application, inspect PID, executable,
command line, working directory or artifact path, and start time. Terminate only
the process whose command line belongs to the current project/gate. Start time
alone is not ownership proof. Record any mistaken attribution in diagnostics.

## EXE Lineage

1. Require explicit source-gate approval.
2. Stop stale build and verifier processes that have confirmed ownership.
3. Build from current source after the last product, entry-point, packaging, or
   verifier edit.
4. Record source hashes/mtimes, build time, build command, tool versions, and the
   final root/dist hashes.
5. If root and dist are both deliverables, copy the same binary and prove hash
   identity. Do not accept an older nested dist artifact.
6. Verify shortcuts, arguments, working directory, icon, windowed behavior, and
   absence of an unintended console.
7. Launch the root executable and each public shortcut, then repeat the critical
   simulator and UI scenarios with target-window screenshots.

For one-file PyInstaller builds, a live bootloader or `_MEI*` directory does not
prove Python entry or UI startup. Add an early runtime marker and distinguish
bootloader, Python entry, Qt creation, and main-window states. Avoid broad
`collect_all` calls when native hooks already collect a large framework; excessive
collection can create huge, slow, or stalled one-file startup.

## Runtime Waits

Use real QTest events for clicks and pointer actions. In worker-wait loops, prefer
`app.processEvents()` plus a short `time.sleep()` so the worker thread can run.
Repeated `QTest.qWait()` can hold the GIL and create a verifier-induced
per-point slowdown that is not a product regression. Record the polling method.

## Verdicts

Keep these independent:

- `source_ui_verified`
- `packaged_exe_verified`
- `simulator_verified`
- `real_hardware_unvalidated_blocked`
- subsystem-specific `blocked_unverified`

A successful clean build is not a packaged runtime pass.
