# Module Boundary Map

| Package | Owns | Inputs | Outputs | Degraded mode |
|---|---|---|---|---|
| editor | text interaction, selection, local undo, presentation | Sheet text, local user state | editor transactions | plain text editing without analysis overlays |
| vault | scan, parse, atomic canonical I/O | project path, contracts | canonical objects, file events | open read-only or repair mode |
| mutation | operation plans, preconditions, apply and inverse | proposed changes, base revisions | committed revisions, audit events | proposal-only mode |
| recovery | buffers, snapshots, conflicts, restore | mutation events, canonical files | restored state, recovery receipts | preserve and export files manually |
| catalog | SQLite mirrors, FTS, recent context | canonical objects/events | fast query APIs | rebuild or direct scan |
| compiler | resolve, validate, transform, render, source map | manifests, Sheets, profiles | artifacts, QA, source maps | Markdown-only export |
| search | literal and structural retrieval | catalog and canonical fallbacks | ranked results with explanations | direct grep/file scan |
| compendium | entities, claims, evidence, conflict records | canonical records and Sheet anchors | inspector/query results | manual records only |

## Rule

No package may acquire canonical authority outside this map without an ADR and authority-matrix update.
