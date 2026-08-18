# ADR-0004: Select Electron as the F2 desktop shell scaffold

- Status: accepted
- Accepted scope: F2 desktop scaffold, subject to explicit veto/revisit conditions
- Decision class: high reversal cost
- Review gate: F1 technology review
- Evidence issue: #3
- Evidence run: `32085957984`
- Evidence report: `spikes/desktop-shell/results/SHELL_SPIKE_REPORT-2026-08-18.md`

## Context

Constellation Writer needs cross-platform desktop packaging, local filesystem access, native dialogs and menus, a web-capable professional editor surface, and a systems layer capable of atomic writes, SQLite, hashing, recovery, and deterministic compile operations.

The original candidate was Tauri 2 because its Rust backend, explicit capability model, and use of operating-system WebViews fit the local-first systems architecture. F1 required that candidate to survive an equivalent Electron control rather than becoming architecture by preference.

## Decision

Use **Electron 43.2.0 as the F2 desktop shell scaffold**.

The renderer remains sandboxed and must not own canonical filesystem state. Use:

- one web frontend shared with browser-level tests;
- `contextIsolation: true`, renderer sandboxing, and no Node integration in the renderer;
- a narrow typed preload/IPC bridge rather than generic IPC exposure;
- native project operations in the main/native service layer;
- no local HTTP server requirement;
- no renderer-visible unrestricted project paths or filesystem primitives;
- shell-neutral interfaces around vault, mutation, recovery, hashing, catalog, compile, and search services so a later shell reversal does not migrate project formats.

Tauri 2 remains the principal fallback shell, not a discarded technology.

## Evidence

A bounded spike used the same CodeMirror renderer and deterministic 50,000-word fixture in Electron and Tauri controls on GitHub-hosted Windows and macOS runners. Final workflow `32085957984` passed all four shell/platform matrix jobs. Foundation validation at the same head also passed in run `32085957973`.

Both controls:

- built and packaged on Windows and macOS;
- launched far enough to return a renderer-ready runtime report;
- used a narrow native bridge;
- implemented native dialogs, menu/shortcut, clipboard, watch plumbing, drag/drop plumbing, crash/restart markers, and an atomic-write placeholder;
- passed lexical and symlink-escape project-root negative controls;
- rendered the same 50,000-word CodeMirror fixture.

Measured hosted-runner shell-to-renderer-ready times were:

- macOS Electron: 1,889.843 ms
- macOS Tauri: 4,884.459 ms
- Windows Electron: 971.012 ms
- Windows Tauri: 12,525.568 ms

Those are single hosted-runner observations, not product SLOs. They are retained because the direction was consistent across both measured targets, not because one sample is sufficient to establish a final performance budget.

Tauri produced much smaller distribution-output measurements, but the Windows outputs were not packaging-equivalent and package size was explicitly a secondary criterion. Process-tree memory was also not safely comparable because OS-managed WebView process ownership differs by platform.

## Why Electron won this gate

### 1. Professional editor consistency has unusually high leverage

Electron ships one Chromium generation across the target desktop platforms. Tauri deliberately uses different operating-system WebViews. Because the editor is the sovereign surface, reducing engine variance is more important here than it would be for a conventional dashboard application.

### 2. The measured shell-ready direction favored Electron

In the bounded runner evidence, Electron reached the shared renderer materially sooner on both platforms. The result requires real-hardware replication but is enough to reject package size as a reason to select Tauri by default.

### 3. Electron survived the security-boundary test

The control demonstrated that Electron does not require renderer Node access or renderer-owned filesystem mutation. Canonical writes can remain behind a small validated native boundary.

### 4. Tauri's footprint advantage remains real but not decision-dominant

The smaller app-distribution footprint is desirable, but writer experience, security boundary, cross-platform editor behavior, recovery reliability, and time-to-first-word outrank binary size.

## Hard veto state

No automated hard veto was observed for either shell in file-boundary, build, package, or 50k rendering smoke tests.

Two hard veto categories remain **unmeasured rather than passed**:

- real IME composition/candidate-window behavior;
- assistive-technology/accessibility-tree behavior under VoiceOver, Narrator/NVDA, high contrast, keyboard-only use, and 200% zoom.

The shared fixture includes mixed Japanese, Arabic, and Hebrew text, but synthetic insertion is not accepted as IME evidence.

## Consequences

Positive:

- one browser-engine generation across Windows and macOS reduces renderer variability;
- the web editor can be tested against a stable Chromium baseline;
- F2 can proceed without making Rust a mandatory part of shell integration;
- security remains explicit if the preload/IPC surface stays narrow.

Costs:

- larger application distribution footprint;
- Chromium/Node update responsibility moves into the application release cadence;
- Electron process memory may be material on real writer hardware;
- the team must actively prevent capability creep in preload and IPC.

## Rejected alternative

Tauri 2 is rejected as the primary F2 scaffold for now. It remains the fallback if Electron later fails an explicit veto or real-hardware budget.

The Tauri spike should remain in the repository as a reproducible rival/negative control until after F3 Trust Proven.

## Mandatory revisit triggers

Reopen this ADR if:

1. physical IME or accessibility testing finds a critical Electron-specific failure;
2. issue #4 finds editor behavior materially superior or more correct in the native OS WebView path;
3. F2 startup or memory measurements on representative writer hardware exceed accepted budgets;
4. Electron requires broad renderer privileges or renderer-owned canonical filesystem mutation;
5. signing, distribution, updates, or native integration impose materially worse operational risk than Tauri;
6. a future collaboration/sync architecture requires a native capability model not safely reproduced by the selected bridge.

## Rollback

The shell choice may change without migrating canonical project files. Keep native/domain services behind shell-neutral interfaces and preserve the shared renderer contract. A later reversal should replace adapters and packaging, not writer-owned data.

## References

Primary technical source notes are recorded at `spikes/desktop-shell/results/OFFICIAL_SOURCE_NOTES.md`.
