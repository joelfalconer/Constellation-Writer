# Platform Limitation Log

Status: pre-run baseline

## Automated Windows/macOS hosted-runner scope

The workflow is designed to measure build/package success, package bytes, native process launch where the hosted runner permits a GUI session, time to the shared renderer's ready signal, 50k CodeMirror initialization, and best-effort process-tree RSS. It also executes deterministic path-boundary negative controls.

## Veto-capable behavior not established by hosted CI

The following require a manual physical or appropriately virtualized interactive platform pass before they can be claimed as validated:

- real IME candidate-window composition for Japanese, Chinese, Korean, and other input methods;
- screen-reader traversal using VoiceOver and Windows Narrator/NVDA;
- OS accessibility-tree quality beyond DOM semantics;
- high-contrast theme fidelity under real Windows settings;
- native menu discoverability and keyboard conventions with a human operator;
- file drag/drop behavior from Finder and Explorer, including security-scoped cases;
- six-hour or professional writing fatigue;
- signing, notarization, SmartScreen, and Gatekeeper behavior with real certificates.

Synthetic composition events are explicitly excluded as IME evidence.

## Decision rule

If automated evidence passes but the manual veto matrix is unrun, ADR-0004 may select a scaffold candidate only with these vetoes carried forward into F2/F4. It may not claim accessibility or IME validation.
