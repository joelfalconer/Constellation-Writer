# ADR-0002: File-Owned Canonical State

**Status:** proposed

## Decision

Readable project files own canonical and logged truth. SQLite and other indexes are rebuildable projections.

## Rationale

The project promises writer ownership, app-death resilience, migration, inspectability, and recoverability. These promises fail if essential state exists only in an embedded database.

## Consequences

- Every cached field names a canonical rebuild source.
- Deleting `.workbench/` is a required acceptance test.
- Cursor, scroll, and pane layout remain local user state rather than canonical sidecar data.

## Revisit trigger

A future feature may request database-only state only if loss is harmless, exportable, and explicitly classified as noncanonical.
