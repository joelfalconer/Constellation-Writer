# Sprint One: Technology Spikes and Durable Substrate Entry

## Objective

Convert the architecture package into measured technology decisions and begin the first executable file-owned writing loop.

## Work packages

### SP1-A Shell spike

Issue #3. Compare Tauri 2 and Electron on platform behavior, security boundary, IME/accessibility, startup, memory, and development complexity.

### SP1-B Editor spike

Issue #4. Test CodeMirror 6 and a bounded rival on prose fidelity, long documents, overlays, selection, IME, bidi, screen readers, and six-hour ergonomics.

### SP1-C Compile spike

Issue #5. Resolve the reference manifest into a Workbench AST, render direct Markdown/HTML, test a pinned Pandoc DOCX/EPUB adapter, and emit source maps.

### SP1-D Substrate harness

Issue #6. Implement project scan, Sheet read/write, atomic replace, recovery buffer, catalog rebuild, manifest order, conflict preservation, snapshot, and restore.

## Acceptance

- ADR-0004, 0005, and 0006 updated with measurements and decisions.
- Validator and negative tests green in CI.
- At least one executable path reads and writes the reference project without SQLite-owned truth.
- Forced failure preserves acknowledged text.
- Sprint receipt records failures, not only successes.
