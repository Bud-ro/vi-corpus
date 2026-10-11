# Supervision And Phase Gates

## Start From Disk State

Read the current project, latest accepted gate, latest failed gate, verifier,
tests, packaging scripts, and running processes before assigning work. Preserve
accepted baselines and failed diagnostics. Do not ask an execution task to redo
work already proved on disk.

## Bound Ownership

Give each worker one writable subtree and state the forbidden siblings. Keep UI,
logic, packaging, and real-hardware authority explicit. Do not create nested
threads or agents when the user forbids them. Do not rush SDK and VI study merely
to produce an early implementation; hidden behavior is cheaper to inventory than
to debug after packaging.

Allow at most one active writer, one verifier, and one build for a project
subtree. Check current tasks, processes, and artifact writes before replacing a
stalled operation or launching a second gate.

## Gate Handoff Contract

Every handoff must include:

- exact phase and allowed next phase;
- preserved behaviors that must not regress;
- canonical verifier and test command;
- runtime and dependency path;
- fresh artifact directory requirement;
- status labels that must remain blocked;
- stop condition and required reviewer approval.

Source approval is a hard gate into packaging. Once approved, stop polishing the
source checklist unless a new blocker appears. Conversely, do not enter EXE work
while source UI, data parity, or performance is still blocked.

## Independent Review

Use separate read-only reviews for:

1. logic, data, hardware boundaries, and SDK evidence;
2. UI screenshots, interaction evidence, and packaged runtime lineage.

Review raw screenshots and structured output, not only the executor's summary.
Send a concrete blocker list with a new non-destructive evidence directory.
Never overwrite a failed gate with `passed` or reuse its screenshots.

## Status Discipline

Keep these states separate in every summary:

- inventory and independent algorithm parity;
- simulator workflow;
- source UI;
- packaged EXE;
- real hardware;
- unresolved optional or phase/chopper subsystems.

An executor saying "done" is a request for review, not acceptance. A build that
exists is not a runtime pass. A usage limit, missing device, or missing raw fixture
is an explicit blocker, not a reason to weaken the gate.
