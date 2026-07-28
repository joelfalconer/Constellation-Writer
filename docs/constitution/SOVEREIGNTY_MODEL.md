# Sovereignty Model

## Purpose

This document defines who or what has final authority over each class of project action and state.

## Sovereignties

### Author sovereignty

The writer decides what enters canonical prose, structure, metadata, canon, and publication state. AI, scripts, imports, and analyses may propose. They do not silently decide.

### Editor sovereignty

The editor is the primary authorship surface. Navigation, metadata, continuity, compile, and AI are subordinate instruments with bounded jurisdictions.

### File sovereignty

Readable project files hold durable state. SQLite, FTS, graphs, embeddings, previews, and analytics are rebuildable projections.

### Manuscript sovereignty

A manuscript manifest owns assembly order and placement. Filesystem ordering, search ranking, and UI sorting cannot mutate manuscript order implicitly.

### Compile sovereignty

A compile profile and frozen compile plan own transformation into an output. Output behavior must not depend on hidden UI state or stale caches.

### Evidence sovereignty

A Compendium claim is not supported merely because it exists. Evidence records and locators govern what the manuscript or a source actually supports.

### Recovery sovereignty

A failed write, conflict, restore, migration, or high-consequence mutation must preserve a path back to a known state.

## Conflict resolution order

When authorities disagree:

1. Protect the latest acknowledged human work from loss.
2. Preserve both versions if a conflict cannot be resolved safely.
3. Prefer canonical files over derived mirrors.
4. Prefer stable IDs over titles, paths, or UI placement.
5. Prefer explicit manifest/profile decisions over inferred defaults.
6. Require review before changing locked canon or publication state.

## Acceptance

- No subsystem can grant itself canonical write authority.
- Every canonical write route passes through a declared mutation policy.
- Derived stores can be removed without changing canonical interpretation.
