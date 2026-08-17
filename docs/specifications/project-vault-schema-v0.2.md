# Project Vault Schema v0.2

**Status:** candidate  
**Imports:** `INV-DATA-001`, `INV-REC-001`, Canonicality Matrix, identifier and revision contracts

## Vault law

The writer owns the project files. The application can reconstruct operational state from canonical and logged files.

## Proposed structure

```text
project.yml
manuscripts/
sheets/
meta/sheets/
annotations/
materials/
assets/
sources/
compile/
compendium/
patches/
snapshots/
migrations/
.workbench/
```

## Integrated changes from v0.1

- Cursor, scroll, pane state, and recent context move out of canonical sidecars into `.workbench/user-state/`.
- Annotations receive their own canonical append-oriented store rather than expanding Sheet metadata indefinitely.
- `.workbench/` contains only derived or ephemeral state and may be deleted.
- Multi-file canonical changes use the Mutation Envelope and recovery bundles.
- Archives distinguish private full backup from editor handoff and publication records.

## Canonical files

- `project.yml`
- Sheet Markdown files and canonical sidecars
- manuscript manifests
- annotations
- compile profiles and style maps
- Compendium records
- source and asset manifests
- mutation, migration, conflict, and snapshot records

## Derived state

SQLite, FTS, graph, embeddings, previews, thumbnails, validation caches, and local UI state.

## Required assay

Delete `.workbench/`, reopen the project, rebuild catalog and indexes, preserve identity/order/text/metadata, and compile equivalent output.
