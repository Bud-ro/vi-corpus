# Industrial Laboratory UI And Visual QA

## Design Contract

- Prefer Apple-like clarity in hierarchy, spacing, typography, and restraint;
  keep the density and explicit state needed by industrial software.
- Use high-contrast, low-saturation surfaces. Avoid decorative gradients,
  AI-like purple/blue palettes, nested cards, and text that explains the UI.
- Keep common operating controls visible. Put advanced, simulator-only, or rare
  parameters in real functional tabs, not empty note pages.
- Do not duplicate command-rail actions inside tabs.
- Represent hardware as `device name + LED`: green connected, red failed or
  fail-closed, gray simulated/optional/unconnected.
- Make shutter text and color reflect the adapter-reported state.
- Use timestamps, severity, point/step, message, and separators in logs.

## Layout Rules

- Align label and field edges; left-align values and hover readouts.
- Reserve stable width for buttons and combo arrows; let long path fields shrink
  or elide with a complete tooltip.
- Use a scroll area for a fixed LabVIEW-style panel at constrained resolutions.
  Scrolling is acceptable; overlap, clipping, or compressed controls are not.
- Capture both top and bottom states when scrolling separates controls from the
  final status, result, or event log.
- Give scroll-area viewport, page, and wrapper an explicit theme background to
  prevent white regions.
- Verify text baselines, glyph clipping, blank first rows, hidden layers, panel
  titles, button margins, and complete multi-line status text.

## Plot And Heatmap Rules

- Show titles, axis names, units, readable ticks, and trace identity.
- Hover must originate from a real mouse event on the visible canvas/scene and
  change the readout from its default. A setter or simulated helper is diagnostic
  only; `fallback_used=true` fails the gate.
- Map view coordinates through the actual view box and graphics view after any
  scrolling. Test first, middle, and last data points.
- Heatmap source shape, displayed image shape, axis order, pixel-edge transform,
  selected slice, LUT, and colorbar range must be recorded.
- Use explicit floor/coordinate mapping consistent with pixel centers; avoid
  `round()` against edge-based image rectangles.
- Do not interpolate or downsample full-parity evidence without a documented
  scientific reason.

## Runtime Verification Sequence

1. Execute the original user workflow in the target application.
2. Use real clicks, typing, combo popups, checkboxes, scrolling, pause/resume,
   stop, and plot movement.
3. Capture target-window or control screenshots, not the full desktop and not a
   modal screenshot that interrupts the operator.
4. Run automated image checks for window identity, nonblank content, clipping,
   bounds, contrast, and large theme discontinuities.
5. Perform a separate human visual review of every full screenshot and dense
   crop. Automated `layout_issues=[]` is not a visual approval.
6. Audit whether the screenshot proves the requested result rather than a setup,
   loading, idle, or typed-prompt state.

## Required Coverage

- every main and nested tab at 1920x1080 and 1366x768 or project equivalents;
- long output path, combo popup, checkbox states, and all command states;
- Initialize, scan, pause, paused, resume, completed, stop-partial, and failure;
- source and packaged EXE screenshots generated after their respective build;
- plot hover for every trace class and heatmap x/y/z plus contextual dimensions;
- complete and partial result/status/log areas;
- driver status and real/simulated hardware distinction.

Do not claim UI verification from source inspection, process state, JSON alone,
or screenshots from an earlier gate.
