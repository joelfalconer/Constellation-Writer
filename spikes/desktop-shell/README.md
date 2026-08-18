# Desktop Shell Decision Spike

This directory implements the bounded F1 shell comparison from issue #3. It is not a product scaffold.

## Controls

- `shared/`: one Vite + CodeMirror renderer used by both shells, including a deterministic 50,000-word fixture and mixed-script text.
- `electron/`: Electron 43 control with sandboxed renderer, context isolation, a narrow preload bridge, native dialogs/menu/clipboard, file watcher, project-root boundary, crash marker, and atomic-write placeholder.
- `tauri/`: Tauri 2 control with the same renderer and equivalent Rust commands, native dialogs/menu/clipboard, file watcher, project-root boundary, crash marker, and atomic-write placeholder.
- `scripts/`: cross-platform package and runtime measurement helpers.
- `results/`: evidence, limitations, and decision artifacts.

## What CI can prove

The spike workflow builds both controls on Windows and macOS, runs boundary tests, packages them, attempts a packaged runtime probe, records time-to-renderer-ready and the shared 50k editor initialization metric, and preserves machine-readable artifacts.

## What CI cannot honestly prove

Hosted runners are not a substitute for physical assistive-technology and human input testing. Real IME candidate windows, screen-reader traversal, OS high-contrast fidelity, platform-native keyboard expectations, and long-session writer comfort require manual hardware/OS sessions. Synthetic DOM events are not promoted as IME or accessibility evidence.

The ADR must retain those limitations as veto-capable revisit conditions.
