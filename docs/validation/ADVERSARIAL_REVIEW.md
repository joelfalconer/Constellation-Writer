# Adversarial Architecture Review v0.1

## Serious rivals

### Rival A: SQLite as canonical project store

**Advantage:** transactional consistency, simpler indexing, fewer sidecars.  
**Failure against doctrine:** app death and external inspection become harder; database corruption has greater consequence; file-sync interoperability degrades.  
**Falsifier for current choice:** file-owned canonical state cannot meet acceptable performance or transaction safety after prototype testing.

### Rival B: One canonical document per manuscript

**Advantage:** simple external compatibility and fewer identity problems.  
**Failure:** structural manipulation, alternate assembly, partial loading, and reuse become brittle at professional scale.  
**Falsifier:** chunked Sheets impose materially worse writing and compile workflows than a whole-document model.

### Rival C: ProseMirror/block-based editor

**Advantage:** rich structured editing and annotations.  
**Failure:** risks making block identity and serialized structure foundational, weakening plain-text sovereignty and native prose behavior.  
**Falsifier:** CodeMirror cannot meet required screenplay, comment, accessibility, and revision-overlay behaviors.

### Rival D: Electron instead of Tauri

**Advantage:** mature Chromium consistency and Node ecosystem.  
**Failure:** larger runtime and different security/resource posture.  
**Falsifier:** platform WebView variation or Rust integration cost prevents reliable editor behavior or delivery.

### Rival E: custom compiler without Pandoc adapter

**Advantage:** complete control and smaller dependency surface.  
**Failure:** expensive format support and risk of low-quality DOCX/EPUB output.  
**Current position:** own the compile plan and semantic AST; use Pandoc as a versioned output adapter where it passes golden tests.

## Negative controls

- Validate a project after deleting every derived file.
- Run compile with intentionally stale SQLite mirrors.
- Feed AI candidate claims with no evidence and ensure canon remains unchanged.
- Attempt a mutation against an outdated revision.
- Open the reference project in a generic Markdown editor.

## Principal unresolved risks

- WebView differences may affect editor fidelity and IME/accessibility behavior.
- Text anchors may become stale under large revision.
- Sidecar count may create sync and repository noise.
- Pandoc conversion can be lossy for formats more expressive than the internal AST.
- Event/history retention may expose private deleted text.

## Route

Retain the current architecture as a candidate. Do not promote until the reference vertical slice and failure suite test the rivals’ strongest objections.
