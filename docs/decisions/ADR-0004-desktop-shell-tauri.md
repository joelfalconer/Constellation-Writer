# ADR-0004: Use Tauri 2 as the candidate desktop shell

- Status: proposed
- Decision class: high reversal cost
- Review gate: F1 technology review

## Context

Constellation Writer needs cross-platform desktop packaging, local filesystem access, native dialogs and menus, a web-capable editor surface, and a systems layer capable of atomic writes, SQLite, hashing, and recovery operations.

Tauri 2 combines an HTML/JavaScript frontend in the operating system WebView with a Rust application backend connected through message passing. Its architecture supports Windows, macOS, and Linux packaging without bundling a Chromium runtime.

## Decision

Prototype the desktop shell using Tauri 2 with:

- TypeScript frontend;
- Rust-owned vault, mutation, recovery, hashing, and catalog operations;
- a narrow typed command/event bridge;
- no local HTTP server requirement;
- capability permissions restricted to project operations.

## Reasons

- Strong fit for a local-first systems backend.
- Rust supports safe low-level file and transaction work.
- Web frontend permits CodeMirror and high-fidelity interface iteration.
- Smaller packaged runtime than an Electron baseline.

## Risks

- OS WebView variation can create rendering, IME, accessibility, and testing differences.
- Rust and frontend bridge complexity increases implementation cost.
- Tauri plugin/capability configuration requires careful security review.

## Required spike

Build the same editor shell on Windows and macOS, test IME, accessibility tree, clipboard, drag/drop, large document rendering, native menus, file watching, and crash recovery. Compare against an Electron control build before acceptance.

## References

- https://v2.tauri.app/concept/architecture/
- https://github.com/tauri-apps/tauri/blob/dev/ARCHITECTURE.md
