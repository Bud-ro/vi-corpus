# Performance And Displayed-Data Parity

## Separate Profiles

Use explicit profiles and never mix their claims:

| Profile | Purpose | May prove |
| --- | --- | --- |
| `quick_preview` | fast interaction and failure checks | UI behavior only |
| `full_parity` | production dimensions and persistence | shape/axis/save/display parity |
| `target_derived_roundtrip_simulator_fixture` | reproduce a known output | pipeline lineage, not independent algorithm parity |
| independent synthetic raw | exercise processing math | algorithm behavior for defined inputs |
| real hardware raw fixture | compare old and new processing | independent LabVIEW-to-Python parity |

A reduced preview must state its power, delay, wavelength, repeat, and acquisition
counts in the screenshot and JSON.

## Measure The User Path

Benchmark from the real Scan click to the terminal UI state. Record:

- core and UI wall-clock time;
- UI overhead ratio;
- total acquisition and semantic event counts;
- progress, plot, and log render counts;
- save, load, flush, parsing, array-copy, and simulation-sleep timings;
- runtime, Qt, verifier, polling method, source hash, and profile.

Keep a comparable accepted baseline. If configurations differ, state that the
numbers are diagnostic rather than a direct regression comparison.

Do not improve a benchmark by reducing sample count, dropping raw output,
coalescing semantic events, bypassing the UI signal path, or skipping persistence.

## Diagnose Before Optimizing

Run the smallest A/B that distinguishes product cost from verifier cost:

1. same profile headless;
2. same profile through Qt using `processEvents + sleep`;
3. only then isolate logging, rendering, saving, loading, and simulation delay.

`QTest.qWait` in a polling loop may hold the GIL and create a false per-point
slowdown. Keep QTest for actual input events, not worker waiting.

Buffering may reduce physical opens/writes, but the final report must show that
ordered semantic events before and after are equal. Flush on pause, stop, error,
and final close so diagnostics survive important boundaries.

Throttle progress before cross-thread signal emission when every point need not
be rendered. Throttling only in the receiving UI still queues every signal and can
hide Pause or Stop behind stale progress events. Never throttle acquisition or
semantic logging merely because rendering is throttled.

## Prove The Data Chain

Compare three distinct values from the same run:

1. workflow result;
2. persisted file readback;
3. plot curve or `ImageItem.image` data.

Then compare each with the expected fixture. Record shape, axes, dtype, selected
slice, tolerance, RMSE, maximum absolute error, and representative first/middle/
last points. Never compare the target fixture with itself.

For a power-dependent map, a full-parity selected-delay image should record the
source cube shape, selected delay index/value, displayed power-by-wavelength
shape, pixel transform, color lookup table, and colorbar range.

## Coordinate Registration

Define whether image rectangles use pixel edges or centers. Map the visible mouse
position through the view box to explicit axis coordinates, then use a consistent
index rule such as floor against edge coordinates or nearest search against center
coordinates. Test first, middle, and last rows/columns and assert that the hover z
equals both the displayed image pixel and the processed matrix element.

Do not use undocumented interpolation or downsampling to make a heatmap look
smoother. Scientific resolution is a data property, not a styling choice.

## Control Responsiveness

On the full profile, measure pause-to-paused, resume-to-progress, and stop-to-
terminal latency. Ensure the worker does not pre-emit enough queued progress to
hide control requests. A fast scan may require clicking Pause immediately or
using a full profile; do not add artificial product delay merely to make a test
easier.
